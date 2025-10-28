# 🚀 Django REST API — Docker Setup

Este proyecto utiliza **Django REST Framework** junto con **Docker Compose** para simplificar el despliegue y la ejecución en entornos locales o de desarrollo.

---

## 🧩 Requisitos previos

Asegúrate de tener instalado:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

Verifica la instalación ejecutando:

```bash
docker -v
docker compose version
```

Asegurate de crear el archivo .env en la raíz del proyecto y agregar las variables de entorno requeridas, para ello te puedes basar en el archivo .env-example. 

## Ejecutar el proyecto

Para ejecutar el proyecto con docker usar el siguiente comando 

```bash
docker compose up -d
```

Para detener la ejecuación puedes usar los siguientes comandos

```bash
docker compose stop
```

```bash
docker compose down
```