import json
import os
import random
import time

import paho.mqtt.client as mqtt

# Punto de partida "normal" del motor; el ruido simula variacion real de sensor.
BASE_TEMPERATURA_C = 65.0
BASE_VIBRACION_MM_S = 2.0
BASE_RPM = 1450


def get_app_config():
    """Config a nivel de app (appconfig.json) — igual que en el boilerplate."""
    with open("/appconfig/appconfig.json") as f:
        return json.load(f)


def get_global_config():
    """Config a nivel de dispositivo (global.json) — igual que en el boilerplate."""
    with open("/appconfig/global.json") as f:
        return json.load(f)


def get_mqtt_credentials():
    """Secrets inyectados por Barbara como variables de entorno."""
    return {
        "user": os.environ.get("MQTT_USER"),
        "password": os.environ.get("MQTT_PASSWORD"),
    }


def leer_sensores():
    """Simula la lectura de los sensores de un motor industrial."""
    temperatura = round(BASE_TEMPERATURA_C + random.uniform(-3, 3), 1)
    vibracion = round(BASE_VIBRACION_MM_S + random.uniform(-0.5, 0.5), 2)
    rpm = BASE_RPM + random.randint(-20, 20)
    return {
        "motor_id": "motor1",
        "temperatura_c": temperatura,
        "vibracion_mm_s": vibracion,
        "rpm": rpm,
        "timestamp": int(time.time()),
    }


def main():
    app_config = get_app_config()
    # El broker MQTT es la app "Broker MQTT Mosquitto" del Marketplace,
    # desplegada aparte en el mismo nodo (servicio Docker "mqttbbr").
    mqtt_host = app_config.get("mqttHost", "mqttbbr")
    mqtt_port = app_config.get("mqttPort", 1883)
    topic = app_config.get("mqttTopic", "planta/motor1/telemetria")
    publish_interval = app_config.get("publishIntervalSeconds", 5)

    global_config = get_global_config()
    plant_name = global_config.get("plantName", "planta-desconocida")

    credentials = get_mqtt_credentials()

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    if credentials["user"]:
        client.username_pw_set(credentials["user"], credentials["password"])
    client.connect(mqtt_host, mqtt_port)
    client.loop_start()

    print(f"Planta: {plant_name}")
    print(f"Conectando a broker MQTT en {mqtt_host}:{mqtt_port}")
    print(f"Publicando telemetria en '{topic}' cada {publish_interval}s...")
    try:
        while True:
            payload = leer_sensores()
            client.publish(topic, json.dumps(payload))
            print(f"Publicado: {payload}")
            time.sleep(publish_interval)
    except KeyboardInterrupt:
        pass
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
