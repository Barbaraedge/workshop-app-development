# Ejercicio 2 — Simulador de motor industrial (Python + MQTT) para Barbara

Basado en el boilerplate oficial de Barbara:
https://github.com/Barbaraedge/training_barbara_apps_development/tree/main/boilerplate_01_python

Este proyecto simula un sensor de un motor industrial (`motor-simulator`)
que publica lecturas de temperatura, vibración y RPM cada pocos segundos a
un broker **MQTT**.

```
planta/motor1/telemetria → {"motor_id": "motor1", "temperatura_c": 66.2,
                             "vibracion_mm_s": 2.1, "rpm": 1462,
                             "timestamp": 1758800000}
```

> [!IMPORTANT]
> Este compose **no incluye un broker MQTT propio**. Usa la app **"Broker
> MQTT Mosquitto"** del Marketplace de Barbara, desplegada aparte en el
> mismo nodo (servicio Docker `mqttbbr`). Despliega primero esa app desde
> el Marketplace antes de este ejercicio.

Además de publicar telemetría, la app lee e imprime, siguiendo el mismo
patrón del boilerplate:

* `appConfig` (`appconfig.json`) — host/puerto del broker, topic MQTT e
  intervalo de publicación.
* `globalConfig` (`global.json`) — nombre de la planta.
* Secrets (`MQTT_USER` / `MQTT_PASSWORD`) — credenciales del broker
  Mosquitto de Marketplace (por defecto `bbruser`/`bbrpassword`, a
  cambiar en producción).

## Estructura

```
02-python-mqtt-app/
├── docker-compose.yml        # despliegue en un Barbara Edge Node
├── docker-compose_dev.yml    # desarrollo en tu maquina local
├── barbarasecrets.env        # secrets de ejemplo (solo para dev local)
├── appconfigDev/
│   ├── appconfig.json        # config de la app (dev local)
│   └── global.json           # config de dispositivo (dev local)
└── imageSource/
    ├── Dockerfile
    └── src/
        ├── motor_simulator.py
        └── requirements.txt
```

## Desarrollo local

Para probar en tu máquina necesitas un broker MQTT accesible en
`localhost:1883` — por ejemplo, uno rápido con Docker:

```ShellSession
docker run -d --name mosquitto-dev -p 1883:1883 eclipse-mosquitto:2.0 \
  sh -c "echo 'listener 1883' > /mosquitto/config/mosquitto.conf && \
         echo 'allow_anonymous true' >> /mosquitto/config/mosquitto.conf && \
         /docker-entrypoint.sh mosquitto -c /mosquitto/config/mosquitto.conf"
```

(Si usas este broker de prueba sin autenticación, deja `MQTT_USER`/
`MQTT_PASSWORD` vacíos en `barbarasecrets.env` para esta prueba local.)

Después, levanta la app:

```ShellSession
docker-compose -f docker-compose_dev.yml up --build
```

Deberías ver en los logs de `motor-simulator` algo como:

```
motor-simulator-1  | Planta: planta-demo-summan
motor-simulator-1  | Conectando a broker MQTT en localhost:1883
motor-simulator-1  | Publicando telemetria en 'planta/motor1/telemetria' cada 5s...
motor-simulator-1  | Publicado: {'motor_id': 'motor1', 'temperatura_c': 66.2, ...}
```

Puedes suscribirte al topic para verlo en tiempo real:

```ShellSession
docker exec -it mosquitto-dev mosquitto_sub -t "planta/motor1/telemetria"
```

## Despliegue en Barbara

1. Despliega primero la app **Broker MQTT Mosquitto** desde el Marketplace
   en el nodo (si no está ya desplegada).
2. Comprime esta carpeta (`docker-compose.yml` e `imageSource/` — **no**
   `docker-compose_dev.yml`, `appconfigDev/` ni `barbarasecrets.env`, que
   son solo para desarrollo local) en un `.zip`, con `docker-compose.yml`
   en la raíz.
3. Barbara Panel → **App Library → Upload App** → sube el zip.
4. Configura `appConfig` (`mqttHost: "mqttbbr"`, puerto, topic, intervalo),
   `globalConfig` y los secrets `MQTT_USER`/`MQTT_PASSWORD` (las
   credenciales del broker Mosquitto ya desplegado) antes de desplegar.
5. Despliega en el nodo de pruebas — Barbara construye la imagen a partir
   del `Dockerfile` de `imageSource/` automáticamente.
6. Verifica en los logs del workload `motor-simulator` que está publicando
   telemetría, y en los logs/consumidor del broker que la recibe.

> [!IMPORTANT]
> Mantén sincronizados `docker-compose.yml` y `docker-compose_dev.yml`
> (salvo en los elementos de configuración: `env_file`/`volumes` de
> `appconfig`, que Barbara gestiona por su cuenta en producción) para
> evitar diferencias entre tu entorno de desarrollo y el de despliegue.

## Qué fijarse (puntos de la formación)

- **Dos apps independientes en el mismo nodo**: el broker MQTT (Marketplace)
  y esta app propia se comunican por red Docker interna usando el nombre
  de servicio del broker (`mqttbbr`) — mismo patrón que verán al integrar
  cualquier app propia con conectores/brokers ya desplegados en Barbara.
- **Barbara compila el `Dockerfile` directamente** con `build:` en el
  compose — no hace falta publicar la imagen en ningún registry externo.
- **Dos compose, mismo patrón que el boilerplate oficial**:
  `docker-compose.yml` (minimal, para Barbara) vs. `docker-compose_dev.yml`
  (con `env_file` y `volumes` de `appconfig` montados a mano, simulando lo
  que Barbara inyecta automáticamente en producción).
- **`appConfig` vs `globalConfig`**: `appconfig.json` es específico de esta
  app (host/puerto del broker, topic, intervalo); `global.json` es a nivel
  de dispositivo/planta y se compartiría con otras apps del mismo nodo.
- **Secrets** (`MQTT_USER`/`MQTT_PASSWORD`) se leen como variables de
  entorno — en Barbara se gestionan cifrados desde Panel, nunca en texto
  plano en el compose.
- Restricciones del parser de Barbara aplicadas: sin `name:` ni `tty:` a
  nivel de servicio.
