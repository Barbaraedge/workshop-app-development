# Ejercicio 1 — Desplegar una imagen pública de Docker Hub

Convenciones de nombre de archivo y estructura alineadas con el
boilerplate oficial de Barbara (ver también el Ejercicio 2, que lo sigue
más de cerca):
https://github.com/Barbaraedge/training_barbara_apps_development/tree/main/boilerplate_01_python

**Objetivo**: aprender el flujo más simple para desplegar en Barbara una
aplicación ya publicada en un registry público — sin escribir código, solo
empaquetando un `docker-compose.yml`.

**Qué se despliega**: [Grafana](https://hub.docker.com/r/grafana/grafana),
la herramienta de visualización de dashboards más usada en entornos
industriales para representar datos de sensores/PLCs.

## Docker Compose Files

* `docker-compose.yml`: para desplegar en un **Barbara Edge Node** — no
  incluye credenciales, Barbara las inyecta como Secrets en el deploy.
* `docker-compose_dev.yml`: para desarrollo/pruebas **en tu máquina
  local** — añade `env_file: barbarasecrets.env` para fijar las
  credenciales de admin sin tocar el compose.

## Antes de la sesión

Ten a mano acceso a un nodo Barbara Core activo (ONLINE en Panel) donde
puedas desplegar apps Docker.

## Desarrollo local

```ShellSession
docker-compose -f docker-compose_dev.yml up
```

Accede a Grafana en `http://localhost:3000` con las credenciales de
`barbarasecrets.env` (`admin` / `BarbaraTraining2026`).

## Despliegue en Barbara

1. Comprime esta carpeta en un `.zip` con `docker-compose.yml` en la raíz
   (**no** incluyas `docker-compose_dev.yml` ni `barbarasecrets.env`, son
   solo para desarrollo local).
2. En Barbara Panel: **App Library → Upload App** → sube el zip.
3. Antes de desplegar, añade como Secrets `GF_SECURITY_ADMIN_USER` y
   `GF_SECURITY_ADMIN_PASSWORD` (mismos valores que en
   `barbarasecrets.env`, o los que prefieras para el nodo real).
4. Despliega la app en el nodo de pruebas.
5. Una vez el workload esté `RUNNING`, accede a Grafana en
   `http://<IP_DEL_NODO>:3000`.

## Qué fijarse (puntos de la formación)

- No hay Dockerfile ni `build:`: la imagen (`grafana/grafana:11.3.0`) ya
  existe en Docker Hub, Barbara solo la descarga y la ejecuta.
- **Dos compose, mismo patrón que el boilerplate oficial**: producción sin
  credenciales en texto plano (via Secrets de Barbara) vs. desarrollo con
  `env_file` explícito para trabajar cómodo en local.
- El volumen `./persist/grafana-data` sigue la convención de Barbara para
  bind-mounts: solo se permite bajo `./persist/`, `./appconfig` o `./sys/`
  (ver restricciones del parser).
- Puedes fijar cualquier versión de imagen pública (`grafana:11.3.0`,
  `grafana:latest`, etc.) — igual que harías con `docker run` en local.
