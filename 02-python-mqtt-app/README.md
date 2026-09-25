# Exercise 2 — Industrial motor simulator (Python + MQTT) for Barbara

Based on Barbara's official boilerplate:
https://github.com/Barbaraedge/training_barbara_apps_development/tree/main/boilerplate_01_python

This project simulates a sensor on an industrial motor (`motor-simulator`)
that publishes temperature, vibration and RPM readings every few seconds
to an **MQTT** broker.

```
plant/motor1/telemetry → {"motor_id": "motor1", "temperature_c": 66.2,
                           "vibration_mm_s": 2.1, "rpm": 1462,
                           "timestamp": 1758800000}
```

> [!IMPORTANT]
> This compose **does not include its own MQTT broker**. It uses the
> **"Broker MQTT Mosquitto"** app from the Barbara Marketplace, deployed
> separately on the same node (Docker service `mqttbbr`). Deploy that app
> from the Marketplace first before running this exercise.

Besides publishing telemetry, the app reads and prints, following the same
pattern as the boilerplate:

* `appConfig` (`appconfig.json`) — broker host/port, MQTT topic and
  publish interval.
* `globalConfig` (`global.json`) — plant name.
* Secrets (`MQTT_USER` / `MQTT_PASSWORD`) — credentials for the Marketplace
  Mosquitto broker (defaults `bbruser`/`bbrpassword`, change for
  production).

## Structure

```
02-python-mqtt-app/
├── docker-compose.yml        # deployment on a Barbara Edge Node
├── docker-compose_dev.yml    # development on your local machine
├── barbarasecrets.env        # example secrets (local dev only)
├── appconfigDev/
│   ├── appconfig.json        # app config (local dev)
│   └── global.json           # device config (local dev)
└── imageSource/
    ├── Dockerfile
    └── src/
        ├── motor_simulator.py
        └── requirements.txt
```

## Local development

To test on your machine you need an MQTT broker reachable at
`localhost:1883` — for example, a quick one with Docker:

```ShellSession
docker run -d --name mosquitto-dev -p 1883:1883 eclipse-mosquitto:2.0 \
  sh -c "echo 'listener 1883' > /mosquitto/config/mosquitto.conf && \
         echo 'allow_anonymous true' >> /mosquitto/config/mosquitto.conf && \
         /docker-entrypoint.sh mosquitto -c /mosquitto/config/mosquitto.conf"
```

(If you use this unauthenticated test broker, leave `MQTT_USER`/
`MQTT_PASSWORD` empty in `barbarasecrets.env` for this local test.)

Then, start the app:

```ShellSession
docker-compose -f docker-compose_dev.yml up --build
```

You should see log lines from `motor-simulator` like:

```
motor-simulator-1  | Plant: demo-plant-workshop
motor-simulator-1  | Connecting to MQTT broker at localhost:1883
motor-simulator-1  | Publishing telemetry to 'plant/motor1/telemetry' every 5s...
motor-simulator-1  | Published: {'motor_id': 'motor1', 'temperature_c': 66.2, ...}
```

You can subscribe to the topic to see it live:

```ShellSession
docker exec -it mosquitto-dev mosquitto_sub -t "plant/motor1/telemetry"
```

## Deploying on Barbara

1. Deploy the **Broker MQTT Mosquitto** app from the Marketplace on the
   node first (if not already deployed).
2. Zip this folder (`docker-compose.yml` and `imageSource/` — **not**
   `docker-compose_dev.yml`, `appconfigDev/` or `barbarasecrets.env`,
   which are local development only) with `docker-compose.yml` at the
   root.
3. Barbara Panel → **App Library → Upload App** → upload the zip.
4. Configure `appConfig` (`mqttHost: "mqttbbr"`, port, topic, interval),
   `globalConfig` and the `MQTT_USER`/`MQTT_PASSWORD` secrets (credentials
   for the already-deployed Mosquitto broker) before deploying.
5. Deploy on the test node — Barbara builds the image from the
   `Dockerfile` in `imageSource/` automatically.
6. Check the `motor-simulator` workload logs to confirm it's publishing
   telemetry, and the broker's logs/a subscriber to confirm it's received.

> [!IMPORTANT]
> Keep `docker-compose.yml` and `docker-compose_dev.yml` in sync (except
> for configuration elements: the `env_file`/`volumes` for `appconfig`,
> which Barbara manages on its own in production) to avoid inconsistencies
> between your development and deployment environments.

## What to notice (training takeaways)

- **Two independent apps on the same node**: the MQTT broker (Marketplace)
  and this custom app talk to each other over the internal Docker network
  using the broker's service name (`mqttbbr`) — the same pattern you'll
  see when integrating any custom app with connectors/brokers already
  deployed on Barbara.
- **Barbara builds the `Dockerfile` directly** via `build:` in the
  compose — no need to publish the image to any external registry.
- **Two compose files, same pattern as the official boilerplate**:
  `docker-compose.yml` (minimal, for Barbara) vs. `docker-compose_dev.yml`
  (with `env_file` and `appconfig` volumes mounted by hand, simulating
  what Barbara injects automatically in production).
- **`appConfig` vs `globalConfig`**: `appconfig.json` is specific to this
  app (broker host/port, topic, interval); `global.json` is device/plant
  level and would be shared with other apps on the same node.
- **Secrets** (`MQTT_USER`/`MQTT_PASSWORD`) are read as environment
  variables — in Barbara these are managed encrypted from Panel, never in
  plaintext in the compose file.
- Barbara parser restrictions applied: no `name:` or `tty:` at the service
  level.
