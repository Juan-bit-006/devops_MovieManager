# MovieManager

Aplicación de **Carolina y Juan José** para gestionar películas con CRUD, búsqueda y estadísticas. Tecnologías: Python 3.12, Flask, PostgreSQL 16, Docker, Docker Compose, pytest, GitHub Actions y GitHub Container Registry (GHCR).

Repositorio: [MovieManager, rama prod](https://github.com/Juan-bit-006/devops_MovieManager/tree/prod).

## Obtener el proyecto

```powershell
git clone --branch prod https://github.com/Juan-bit-006/devops_MovieManager.git
cd devops_MovieManager
```

## Requisitos y ejecución con Docker

Docker Desktop iniciado en modo Linux y Compose 2.24.4 o superior para la etiqueta `!reset`. Comandos para PowerShell desde la raíz del repositorio.

```powershell
Copy-Item .env.example .env
python -c "import secrets; print(secrets.token_urlsafe(24))"
python -c "import secrets; print(secrets.token_hex(32))"
```

Poner el resultado del primer comando Python en `DB_PASSWORD` y el segundo en `SECRET_KEY` dentro de `.env`. Guardar valores, no comandos. No subir `.env` a Git.

```powershell
docker compose up --build -d --wait
```

Abrir http://localhost:8080. PostgreSQL usa internamente `db:5432`, sin puerto publicado al equipo. El volumen `postgres_data` conserva los datos. `docker compose down` detiene y elimina contenedores/red manteniendo el volumen. Cambiar la contraseña de `.env` no cambia automáticamente la de una base ya inicializada.

## Ejecutar desde Python

Se requiere PostgreSQL accesible con base y usuario previamente creados. La aplicación crea su tabla al iniciar. Esta modalidad no carga `.env` automáticamente.

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
$env:DB_HOST = 'localhost'
$env:DB_PORT = '5432'
$env:DB_NAME = 'moviemanager'
$env:DB_USER = 'moviemanager'
$env:DB_PASSWORD = '<contraseña real de PostgreSQL>'
$env:SECRET_KEY = '<valor aleatorio generado>'
.\.venv\Scripts\python run.py
```

Abrir http://localhost:5000.

## GitHub Container Registry (GHCR)

`.github/workflows/ci-cd.yml` se ejecuta en PR hacia `prod`, push a `prod` y ejecución manual. `tests` prepara Python 3.12 y PostgreSQL 16, instala dependencias, ejecuta pytest y conserva el informe JUnit incluso ante fallos.

`publish` depende de `tests` y publica solamente por push a `prod`. Si fallan pruebas no publica. PR y ejecución manual solo prueban. La publicación usa `GITHUB_TOKEN` con `packages: write` y construye la última etapa del Dockerfile (`runtime`).

Etiquetas configuradas:

- `ghcr.io/juan-bit-006/devops_moviemanager:latest`
- `ghcr.io/juan-bit-006/devops_moviemanager:sha-<SHA completo del commit>`

Confirmar su disponibilidad después de una ejecución real exitosa; el resumen del job muestra la etiqueta exacta. El nombre se adapta al repositorio automáticamente; actualizar estos ejemplos si cambia de propietario o nombre.

Para acceso público, revisar la visibilidad del paquete en GitHub. Si permanece privado, autenticarse con `docker login ghcr.io -u <usuario>` e introducir en el prompt un token de lectura de paquetes.

## Descargar y ejecutar el artefacto publicado

Preparar `.env` como arriba. Después de confirmar la publicación, sustituir preferiblemente `latest` por la etiqueta `sha-...` del resumen del job para reproducir una versión exacta:

```powershell
$env:MOVIEMANAGER_IMAGE = 'ghcr.io/juan-bit-006/devops_moviemanager:latest'
docker pull $env:MOVIEMANAGER_IMAGE
docker compose -f docker-compose.yml -f docker-compose.ghcr.yml up -d --no-build --wait
```

Abrir http://localhost:8080. El archivo adicional elimina `build` de `web` y utiliza la imagen descargada, manteniendo PostgreSQL, red y volumen.

```powershell
docker compose -f docker-compose.yml -f docker-compose.ghcr.yml down
```

| Parámetro | Uso |
|---|---|
| `DB_NAME`, `DB_USER`, `DB_PASSWORD` | Base, usuario y contraseña compartidos por servicios |
| `DB_HOST`, `DB_PORT` | Compose fija `db`, `5432`; Python directo usa el servidor configurado |
| `SECRET_KEY` | Clave requerida para firmar sesiones Flask |
| `MOVIEMANAGER_IMAGE` | Nombre y etiqueta GHCR |
| `8080:5000` | Puerto del equipo y puerto Flask en el contenedor |

## Actividad conceptual: CI, CD e IaC

### Integración continua (CI): propósito y aplicación

La integración continua consiste en verificar automáticamente los cambios del equipo para detectar errores antes de incorporarlos a la versión compartida. Su propósito es que cada cambio pueda revisarse con evidencia de que los comportamientos esperados siguen funcionando.

En MovieManager, un PR hacia `prod` o un push a esa rama activa GitHub Actions. El job `tests` instala las dependencias, prepara PostgreSQL y ejecuta pytest. Por ejemplo, si un cambio rompe la búsqueda o la validación del año, una prueba falla y la ejecución queda en rojo. El resultado se puede revisar junto con el informe de pruebas. Esto permite detectar el problema antes de publicar otra imagen.

### Entrega continua (CD): propósito y aplicación

La entrega continua prepara una versión distribuible después de superar las verificaciones. Su propósito es que otra persona pueda obtener y ejecutar un artefacto identificado, sin reconstruir manualmente el proyecto.

En MovieManager, después de un push a `prod`, el job `publish` depende de que `tests` termine correctamente. Construye la imagen Docker y la publica en GHCR con `latest` y una etiqueta asociada al SHA completo del commit. Así podemos relacionar una imagen con el código que la produjo y descargar esa versión siguiendo este README.

El flujo implementa entrega continua del artefacto. El arranque de la aplicación a partir de la imagen se realiza manualmente; no hay un despliegue automático a un servidor de producción. Esa distinción coincide con el alcance del parcial.

### Infraestructura como código (IaC): propósito y aplicación

La infraestructura como código consiste en describir los recursos y su configuración mediante archivos que se pueden versionar y revisar, en lugar de depender de configuraciones manuales difíciles de repetir. Su propósito es reproducir entornos y conocer qué cambió en su configuración.

En el entorno local de MovieManager aplicamos ese enfoque declarativo con `docker-compose.yml`: describe los servicios Flask y PostgreSQL, su red, las variables, el volumen persistente y la comprobación de disponibilidad de la base. `docker-compose.test.yml` define por separado el entorno temporal de pruebas. Estos archivos permiten reproducir la composición de contenedores, pero no aprovisionan servidores o redes de un proveedor de nube. El Dockerfile, por su parte, define cómo construir la imagen de la aplicación.

Si el proyecto creciera, podríamos usar Terraform para aprovisionar una máquina virtual, una red y una base de datos administrada. Esa sería una ampliación posible; no está implementada ni se exige para esta entrega.

### Diferencia entre los tres conceptos

| Concepto | Propósito | Ejemplo en MovieManager |
|---|---|---|
| CI | Comprobar automáticamente los cambios | Actions ejecuta pytest con PostgreSQL |
| CD | Preparar y publicar una versión distribuible validada | Publicación de la imagen Docker en GHCR después de aprobar pruebas |
| IaC | Describir entornos y recursos de forma reproducible | Compose define el entorno local; Terraform podría aprovisionar recursos de nube en una evolución futura |

CI verifica el cambio, CD prepara su artefacto e IaC describe el entorno donde puede ejecutarse.
