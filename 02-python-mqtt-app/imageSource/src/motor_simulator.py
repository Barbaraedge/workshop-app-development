import json
import logging
import os
import random
import time

import paho.mqtt.client as mqtt

# "Normal" baseline for the motor; the noise simulates realistic sensor variation.
BASE_TEMPERATURE_C = 65.0
BASE_VIBRATION_MM_S = 2.0
BASE_RPM = 1450

# Temperature above this threshold is logged as a warning (simulates a
# basic health check on the sensor reading).
HIGH_TEMPERATURE_THRESHOLD_C = 67.5

logger = logging.getLogger("motor-simulator")


def get_app_config():
    """App-level config (appconfig.json) — same pattern as the boilerplate."""
    with open("/appconfig/appconfig.json") as f:
        return json.load(f)


def get_global_config():
    """Device-level config (global.json) — same pattern as the boilerplate."""
    with open("/appconfig/global.json") as f:
        return json.load(f)


def get_mqtt_credentials():
    """Secrets injected by Barbara as environment variables."""
    return {
        "user": os.environ.get("MQTT_USER"),
        "password": os.environ.get("MQTT_PASSWORD"),
    }


def configure_logging(level_name):
    """Sets up logging with the minimum level read from appConfig."""
    level = getattr(logging, level_name.upper(), None)
    if not isinstance(level, int):
        logging.basicConfig(level=logging.INFO)
        logger.warning(
            "Unknown log level '%s' in appConfig, falling back to INFO", level_name
        )
        return
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
    )


def read_sensors():
    """Simulates reading the sensors of an industrial motor."""
    temperature = round(BASE_TEMPERATURE_C + random.uniform(-3, 3), 1)
    vibration = round(BASE_VIBRATION_MM_S + random.uniform(-0.5, 0.5), 2)
    rpm = BASE_RPM + random.randint(-20, 20)
    payload = {
        "motor_id": "motor1",
        "temperature_c": temperature,
        "vibration_mm_s": vibration,
        "rpm": rpm,
        "timestamp": int(time.time()),
    }
    logger.debug("Sensor reading: %s", payload)
    if temperature > HIGH_TEMPERATURE_THRESHOLD_C:
        logger.warning(
            "Motor temperature %.1fC is above the %.1fC threshold",
            temperature,
            HIGH_TEMPERATURE_THRESHOLD_C,
        )
    return payload


def main():
    app_config = get_app_config()
    configure_logging(app_config.get("logLevel", "INFO"))

    # The MQTT broker is the "Broker MQTT Mosquitto" Marketplace app,
    # deployed separately on the same node (Docker service "mqttbbr").
    mqtt_host = app_config.get("mqttHost", "mqttbbr")
    mqtt_port = app_config.get("mqttPort", 1883)
    topic = app_config.get("mqttTopic", "plant/motor1/telemetry")
    publish_interval = app_config.get("publishIntervalSeconds", 5)

    global_config = get_global_config()
    plant_name = global_config.get("plantName", "unknown-plant")

    credentials = get_mqtt_credentials()

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    if credentials["user"]:
        client.username_pw_set(credentials["user"], credentials["password"])

    try:
        client.connect(mqtt_host, mqtt_port)
    except (ConnectionRefusedError, OSError) as exc:
        logger.error("Could not connect to MQTT broker at %s:%s: %s", mqtt_host, mqtt_port, exc)
        raise
    client.loop_start()

    logger.info("Plant: %s", plant_name)
    logger.info("Connected to MQTT broker at %s:%s", mqtt_host, mqtt_port)
    logger.info("Publishing telemetry to '%s' every %ss...", topic, publish_interval)
    try:
        while True:
            payload = read_sensors()
            client.publish(topic, json.dumps(payload))
            logger.info("Published: %s", payload)
            time.sleep(publish_interval)
    except KeyboardInterrupt:
        logger.info("Shutting down (keyboard interrupt)")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
