# 🎬 DevOps MovieManager

**Equipo:** MovieManager  
**Proyecto:** Primer parcial de DevOps — Gestión de películas

MovieManager es una aplicación web desarrollada con **Python y Flask**, conectada a **PostgreSQL** y ejecutada mediante **Docker Compose**. Permite registrar, consultar, modificar y eliminar películas.

## 1. Integrantes

- **Juan Jose Ortega** — Flask, vistas, rutas y estructura inicial.
- **Carolina Muñoz** — Implementacion PostgreSQL configuracion Dockerfile y archivo README. 


## 2. Funcionalidades

| Operación | Descripción |
|---|---|
| Crear | Registrar título, director, género, año de estreno y sinopsis. |
| Consultar | Mostrar películas guardadas en PostgreSQL. |
| Modificar | Actualizar los datos de una película existente. |
| Eliminar | Borrar una película tras confirmar la acción. |

## 3. Tecnologías y requisitos

- Python 3.12, Flask, HTML, CSS y Jinja2.
- PostgreSQL 16 y psycopg2.
- Docker Engine y Docker Compose v2.
- Git y GitHub.

**Requisitos para instalar:** Git, Docker con Compose v2, conexión a Internet para descargar las imágenes y el puerto local **8080** disponible. En Windows se puede utilizar Docker Desktop. No es necesario instalar Python ni PostgreSQL directamente en el equipo.

Verificar las herramientas:

```bash
git --version
docker --version
docker compose version
docker info
```

Si `docker info` falla, iniciar Docker Desktop o el servicio Docker.

## 4. Arquitectura

```text
           Navegador
                |
       http://localhost:8080
                |
                v
       +------------------+
       | web: Flask       |
       | Puerto 5000      |
       +--------+---------+
                |
       DB_HOST=db
       Red moviemanager_net
                |
                v
       +------------------+
       | db: PostgreSQL   |
       | Puerto 5432      |
       +--------+---------+
                |
                v
       Volumen postgres_data
```

Docker Compose administra `web` y `db`. Flask se conecta al servicio `db` por la red interna de Docker, no mediante `localhost`. El puerto `8080` del equipo se mapea al `5000` del contenedor Flask.

## 5. Estructura del proyecto

```text
devops_MovieManager/
├── app/
│   ├── __init__.py          # Inicialización de Flask y base de datos
│   ├── routes.py            # Rutas y operaciones CRUD
│   ├── database.py          # Conexión y consultas PostgreSQL
│   ├── templates/
│   │   ├── index.html       # Listado y acciones
│   │   └── formulario.html  # Registro y edición
│   └── static/
│       └── style.css        # Estilos
├── Dockerfile               # Construcción de imagen Flask
├── docker-compose.yml       # Servicios, red y volumen
├── requirements.txt         # Dependencias Python
├── .env.example             # Plantilla de variables
├── .gitignore               # Archivos excluidos de Git
├── README.md
└── run.py                   # Punto de entrada
```

## 6. Configuración y variables

Docker Compose utiliza un archivo `.env` local. **No subir `.env` a GitHub**; solo subir `.env.example` con valores de ejemplo.

| Variable | Función | Ejemplo |
|---|---|---|
| `DB_NAME` | Nombre de la base de datos | `moviemanager` |
| `DB_USER` | Usuario PostgreSQL | `moviemanager` |
| `DB_PASSWORD` | Contraseña PostgreSQL | Definir contraseña propia |
| `SECRET_KEY` | Clave secreta de Flask | Definir clave aleatoria |
| `DB_HOST` | Host de la base desde Flask | `db` (en Compose) |
| `DB_PORT` | Puerto interno PostgreSQL | `5432` (en Compose) |

Contenido esperado de `.env.example`:

```dotenv
DB_NAME=moviemanager
DB_USER=moviemanager
DB_PASSWORD=reemplazar_por_clave_segura
SECRET_KEY=reemplazar_por_clave_aleatoria
```

Generar una clave con Python, si está disponible:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Reemplazar las claves de ejemplo **en `.env`**, no en el repositorio. La configuración de Compose suministra `DB_HOST=db` y `DB_PORT=5432` al servicio web.

## 7. Instalación y ejecución desde cero

Estos pasos se ejecutan desde Git Bash, PowerShell o una terminal Linux/macOS.

### Paso 1: clonar el repositorio

Copiar la **URL HTTPS real** del botón *Code* en GitHub:

```bash
git clone https://github.com/Juan-bit-006/devops_MovieManager.git

cd devops_MovieManager

git switch prod

git pull origin prod
```

### Paso 2: configurar las variables

En Git Bash, Linux o macOS:

```bash
cp .env.example .env
```

Abrir `.env` y reemplazar `DB_PASSWORD` y `SECRET_KEY` por valores seguros. No subir el archivo a GitHub.

### Paso 3: validar la configuración

Con Docker iniciado:

```bash
docker compose config --quiet
```

Si aparecen errores de variables, revisar `.env`. Si aparecen errores de YAML, revisar `docker-compose.yml`.

### Paso 4: construir e iniciar

```bash
docker compose up --build -d
docker compose ps
```

La primera ejecución puede tardar mientras se descargan las imágenes. Se esperan los servicios `web` y `db` activos. Compose debe esperar a que PostgreSQL esté preparado mediante su `healthcheck`.

### Paso 5: abrir la aplicación

Visitar **http://localhost:8080**.

Registrar una película y comprobar que aparece en la tabla. Probar también las opciones Editar y Eliminar.


### Paso 6: detener o reiniciar

```bash
docker compose down
docker compose up -d
```

`down` conserva los volúmenes. **No usar `docker compose down -v`** si se desean conservar los registros.

## 7. Dockerfile e imagen

El Dockerfile utiliza `python:3.12-slim`, instala las dependencias de `requirements.txt`, copia el código Flask, expone el puerto interno `5000` y ejecuta `run.py`.

Construir una imagen de forma independiente:

```bash
docker build -t moviemanager:1.0 .
docker images
```

Para ejecutar la solución completa se recomienda Compose, ya que también levanta PostgreSQL.


## 8. Red y persistencia

Compose define una red `bridge` denominada `moviemanager_net` y un volumen `postgres_data`, montado en PostgreSQL en `/var/lib/postgresql/data`. Docker puede anteponer el nombre del proyecto al nombre efectivo de la red y del volumen.

**Prueba de persistencia:**

1. Iniciar la aplicación y registrar una película.
2. Verificarla en la tabla y en PostgreSQL.
3. Ejecutar `docker compose down`.
4. Ejecutar `docker compose up -d`.
5. Volver a `http://localhost:8080` y verificar que la película sigue registrada.


## 9. Git y trabajo colaborativo

El desarrollo utiliza ramas individuales, commits descriptivos, Pull Requests, revisión y merge hacia `main`.

| Rama | Uso |
|---|---|
| `main` | Código integrado |
| `dev_juan` | Desarrollo de Flask y vistas |
| `dev_carolina` | Desarrollo de Postgres y Dockerfile |
| `preproduccion` | Rama de Pruebas |
| `prod` | Rama de Produccion |


## 10. Solución de problemas

| Problema | Comprobación |
|---|---|
| Docker no responde | Iniciar Docker Desktop o Docker Engine; ejecutar `docker info`. |
| Puerto 8080 ocupado | Liberarlo para mantener la URL requerida. |
| Faltan variables | Revisar `.env` y `.env.example`. |
| PostgreSQL no conecta | Revisar `docker compose ps`, logs de `db` y `DB_HOST=db`. |
| No existe tabla `peliculas` | Revisar que `init_db()` se ejecute al arrancar Flask. |
| No aparecen películas | Revisar `listar_peliculas()` en la ruta `/` y el bucle de `index.html`. |
| Cambios de código no visibles | Ejecutar `docker compose up -d --build web`. |
| Error HTTP 500 | Revisar `docker compose logs --tail=100 web`. |




