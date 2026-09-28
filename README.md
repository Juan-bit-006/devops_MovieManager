# 🎬 DevOps MovieManager

Proyecto para la gestión de películas desarrollado como parte del primer parcial de la asignatura **DevOps**.

## Descripción

MovieManager es una aplicación web para gestionar un catálogo de películas.

La aplicación permitirá realizar las operaciones básicas de:

- Crear películas.
- Consultar películas.
- Modificar películas.
- Eliminar películas.

## Tecnologías

El proyecto utilizará:

- Python
- Flask
- PostgreSQL
- Docker
- Docker Compose
- Git
- GitHub

## Estructura base de directorios y archivos de trabajo

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

## Distribución del trabajo

El desarrollo del proyecto se distribuirá entre los integrantes del equipo de la siguiente manera:

| Integrante | Responsabilidad |
|---|---|
| Juan | Flask, vistas y estructura base |
| Integrante 2 | PostgreSQL y `database.py` |
| Integrante 3 | Dockerfile e imagen Docker |
| Integrante 4 | Docker Compose, variables de entorno, volumen y red |

Cada integrante trabajará desde una branch independiente y los cambios serán integrados mediante Pull Requests.

## Estado del proyecto

🚧 Proyecto en desarrollo.

Se encuentra creada la estructura base de directorios y archivos sobre la cual se desarrollarán los diferentes componentes del proyecto.
