# Exercise 1 — Deploy a public Docker Hub image

File naming and structure conventions aligned with Barbara's official
boilerplate (see also Exercise 2, which follows it more closely):
https://github.com/Barbaraedge/training_barbara_apps_development/tree/main/boilerplate_01_python

**Goal**: learn the simplest flow for deploying an already-published image
from a public registry on Barbara — no code required, just a
`docker-compose.yml`.

**What gets deployed**: [Grafana](https://hub.docker.com/r/grafana/grafana),
the dashboarding/visualization tool most commonly used in industrial
environments to represent sensor/PLC data.

## Docker Compose Files

* `docker-compose.yml`: for deploying on a **Barbara Edge Node** — no
  credentials included, Barbara injects them as Secrets at deploy time.
* `docker-compose_dev.yml`: for development/testing **on your local
  machine** — adds `env_file: barbarasecrets.env` to set the admin
  credentials without touching the compose file.

## Before the session

Have access ready to an active Barbara Core node (`ONLINE` in Panel) where
you can deploy Docker apps.

## Local development

```ShellSession
docker-compose -f docker-compose_dev.yml up
```

Access Grafana at `http://localhost:3000` with the credentials from
`barbarasecrets.env` (`admin` / `BarbaraTraining2026`).

## Deploying on Barbara

1. Zip this folder with `docker-compose.yml` at the root (**do not**
   include `docker-compose_dev.yml` or `barbarasecrets.env` — those are
   for local development only).
2. In Barbara Panel: **App Library → Upload App** → upload the zip.
3. Before deploying, add `GF_SECURITY_ADMIN_USER` and
   `GF_SECURITY_ADMIN_PASSWORD` as Secrets (same values as in
   `barbarasecrets.env`, or whatever you prefer for the real node).
4. Deploy the app on the test node.
5. Once the workload is `RUNNING`, access Grafana at
   `http://<NODE_IP>:3000`.

## What to notice (training takeaways)

- No Dockerfile or `build:`: the image (`grafana/grafana:11.3.0`) already
  exists on Docker Hub, Barbara just pulls and runs it.
- **Two compose files, same pattern as the official boilerplate**:
  production with no plaintext credentials (via Barbara Secrets) vs.
  development with an explicit `env_file` for a smooth local workflow.
- `grafana-data` is a Docker named volume (not a bind mount) — Docker
  manages its storage and ownership, avoiding host filesystem permission
  issues with Grafana's non-root container user.
- You can pin any public image tag (`grafana:11.3.0`, `grafana:latest`,
  etc.) — same as you would with `docker run` locally.
