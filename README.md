# Workshop: App Development and Deployment on Barbara

Hands-on material for an online workshop on developing applications and
deploying them on [Barbara](https://www.barbara.tech) edge nodes. Includes
two guided exercises, each with step-by-step instructions to develop
locally and deploy on a Barbara Edge Node.

## Exercises

| # | Exercise | What you'll learn |
|---|---|---|
| 1 | [Deploy a public Docker Hub image](01-grafana-dockerhub/) | The simplest flow for bringing an already-published app (Grafana) to a node, no code required. |
| 2 | [Develop your own Python app (MQTT)](02-python-mqtt-app/) | The full development flow: custom code, `Dockerfile`, configuration (`appConfig`/`globalConfig`) and secrets, integrating with a Marketplace app already deployed on the node. |

Each folder has its own `README.md` with detailed instructions.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
  installed on your machine.
- Access to an active Barbara Core node (`ONLINE` in Barbara Panel) where
  you can deploy the exercise apps.

## Conventions used in this repo

Both exercises follow the structure of Barbara's
[official boilerplate](https://github.com/Barbaraedge/training_barbara_apps_development/tree/main/boilerplate_01_python):

- `docker-compose.yml` — for deploying on a Barbara Edge Node.
- `docker-compose_dev.yml` — for developing and testing on your local
  machine.
- `imageSource/` — the app's source code and `Dockerfile` (where
  applicable).
- `appconfigDev/` and `barbarasecrets.env` — example configuration and
  secrets, local development only.
