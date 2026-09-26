# 🎬 DevOps MovieManager

Proyecto para la gestión de películas desarrollado como parte del primer parcial de la asignatura **DevOps**.

## Descripción

MovieManager es una aplicación web que permitirá gestionar un catálogo de películas mediante operaciones básicas de:

- Crear películas.
- Consultar películas.
- Modificar películas.
- Eliminar películas.

El proyecto utilizará una aplicación web desarrollada con **Python y Flask**, conectada a una base de datos **PostgreSQL**.

## Tecnologías

- Python
- Flask
- PostgreSQL
- Docker
- Docker Compose
- Git
- GitHub

## Estructura base del proyecto

```text
devops_MovieManager/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── database.py
│   ├── templates/
│   │   ├── index.html
│   │   └── formulario.html
│   └── static/
│       └── style.css
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── run.py
```

## Organización del proyecto

Los principales componentes del proyecto son:

- `app/`: contiene el código de la aplicación Flask.
- `templates/`: contiene las vistas HTML.
- `static/`: contiene los archivos de estilos.
- `database.py`: contendrá la conexión con PostgreSQL.
- `Dockerfile`: permitirá construir la imagen de la aplicación.
- `docker-compose.yml`: permitirá ejecutar la aplicación y la base de datos.
- `requirements.txt`: contiene las dependencias de Python.
- `.env.example`: contendrá las variables de entorno requeridas.
- `run.py`: punto de entrada de la aplicación.

## Trabajo colaborativo

El proyecto será desarrollado mediante diferentes branches para distribuir el trabajo entre los integrantes del equipo.

La integración de los cambios se realizará mediante Pull Requests hacia la rama `main`.

## Estado

🚧 Proyecto en desarrollo.

Actualmente se encuentra definida la estructura base del proyecto y se inició el desarrollo de la aplicación Flask.