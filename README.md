# Workshop: Desarrollo y despliegue de apps en Barbara

Material práctico para un workshop online sobre desarrollo de aplicaciones
y despliegue en nodos edge de [Barbara](https://www.barbara.tech). Incluye
dos ejercicios guiados, cada uno con instrucciones paso a paso para
desarrollar en local y desplegar en un Barbara Edge Node.

## Ejercicios

| # | Ejercicio | Qué aprenderás |
|---|---|---|
| 1 | [Desplegar una imagen pública de Docker Hub](01-grafana-dockerhub/) | El flujo más simple para llevar una app ya publicada (Grafana) a un nodo, sin escribir código. |
| 2 | [Desarrollar una app propia en Python (MQTT)](02-python-mqtt-app/) | El flujo completo de desarrollo: código propio, `Dockerfile`, configuración (`appConfig`/`globalConfig`) y secrets, integrándose con una app del Marketplace ya desplegada en el nodo. |

Cada carpeta tiene su propio `README.md` con instrucciones detalladas.

## Requisitos previos

- [Docker](https://docs.docker.com/get-docker/) y Docker Compose
  instalados en tu máquina.
- Acceso a un nodo Barbara Core activo (`ONLINE` en Barbara Panel) donde
  desplegar las apps de los ejercicios.

## Convenciones usadas en este repo

Ambos ejercicios siguen la estructura del
[boilerplate oficial de Barbara](https://github.com/Barbaraedge/training_barbara_apps_development/tree/main/boilerplate_01_python):

- `docker-compose.yml` — para desplegar en un Barbara Edge Node.
- `docker-compose_dev.yml` — para desarrollar y probar en tu máquina local.
- `imageSource/` — código fuente y `Dockerfile` de la app (cuando aplica).
- `appconfigDev/` y `barbarasecrets.env` — configuración y secretos de
  ejemplo, solo para desarrollo local.
