import json
import os
import random
import time

import paho.mqtt.client as mqtt

# "Normal" baseline for the motor; the noise simulates realistic sensor variation.
BASE_TEMPERATURE_C = 65.0
BASE_VIBRATION_MM_S = 2.0
BASE_RPM = 1450


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


def read_sensors():
    """Simulates reading the sensors of an industrial motor."""
    temperature = round(BASE_TEMPERATURE_C + random.uniform(-3, 3), 1)
    vibration = round(BASE_VIBRATION_MM_S + random.uniform(-0.5, 0.5), 2)
    rpm = BASE_RPM + random.randint(-20, 20)
    return {
        "motor_id": "motor1",
        "temperature_c": temperature,
        "vibration_mm_s": vibration,
        "rpm": rpm,
        "timestamp": int(time.time()),
    }


def main():
    app_config = get_app_config()
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
    client.connect(mqtt_host, mqtt_port)
    client.loop_start()

    print(f"Plant: {plant_name}")
    print(f"Connecting to MQTT broker at {mqtt_host}:{mqtt_port}")
    print(f"Publishing telemetry to '{topic}' every {publish_interval}s...")
    try:
        while True:
            payload = read_sensors()
            client.publish(topic, json.dumps(payload))
            print(f"Published: {payload}")
            time.sleep(publish_interval)
    except KeyboardInterrupt:
        pass
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
