# Organización de la entrega

Documento de apoyo para Carolina y Juan José. Las instrucciones de instalación, uso de GHCR y respuestas de CI, CD e IaC están en [README.md](README.md).

## Funcionalidades

- CRUD: crear, consultar, editar y eliminar películas con título, director, género, año y sinopsis.
- **Búsqueda:** formulario del catálogo y `/?q=texto`, por coincidencia parcial en título/director sin distinguir mayúsculas. Vacío muestra todo; `%` y `_` se buscan literalmente. Conserva el término y muestra un mensaje si no hay resultados.
- **Estadísticas:** `/estadisticas`, total y cantidades por género, agrupadas quitando espacios externos y convirtiendo a minúsculas. Se recalculan al consultar después de crear, editar o eliminar. Catálogo vacío muestra cero y un mensaje.

## Pruebas

Toda la suite con PostgreSQL temporal, sin usar los datos normales:

```powershell
docker compose -p moviemanager-check -f docker-compose.test.yml up --build --abort-on-container-exit --exit-code-from tests
docker compose -p moviemanager-check -f docker-compose.test.yml down
```

El primer comando devuelve el código de salida de pytest. El servidor temporal no publica puertos ni comparte volumen con la aplicación.

Para unitarias con Python:

```powershell
.\.venv\Scripts\python -m pip install -r requirements-dev.txt
.\.venv\Scripts\python -m pytest tests/unit -v
```

Para toda la suite sin Docker, crear una base exclusiva `moviemanager_test` y configurar `DB_HOST`, `DB_PORT`, `DB_USER` y `DB_PASSWORD` para ese PostgreSQL:

```powershell
$env:DB_NAME = 'moviemanager_test'
.\.venv\Scripts\python -m pytest -v --junitxml=test-results/pytest.xml
```

Las pruebas de integración vacían la tabla antes y después de cada caso. Rechazan nombres de base que no terminen en `_test` y fallan si falta conexión.

| Categoría | Qué verifica |
|---|---|
| Unitarias | Campos obligatorios, normalización, longitudes, límites del año y configuración de app sin base |
| Integración | CRUD HTTP y PostgreSQL real, errores 400/404/405, búsqueda, formulario y estadísticas después de modificar datos |
| Regresión | La suite se repite tras modificar código para detectar errores en comportamientos anteriores; no requiere categoría independiente |

## Pruebas de regresión

Una regresión ocurre cuando un cambio introduce un error en una funcionalidad que antes funcionaba. Las pruebas de regresión buscan detectar esos errores al volver a ejecutar comportamientos conocidos después de modificar el código.

En este proyecto, las pruebas del CRUD comprueban que crear, consultar, editar y eliminar películas siga funcionando al incorporar búsqueda y estadísticas. Por ejemplo, si al agregar estadísticas se rompe la edición de una película, la prueba del CRUD puede detectarlo. Las pruebas de búsqueda y estadísticas también quedan como protección frente a cambios posteriores.

No necesitamos una carpeta independiente de regresión: las pruebas unitarias y de integración existentes cumplen esa función al repetirse. La suite protege los casos que cubre; pasar las pruebas no garantiza que no exista ningún otro error.

## Flujo DevOps y participación manual

| Paso | Tipo | Resultado esperado |
|---|---|---|
| Modificar código, hacer commit y push, abrir PR hacia `prod` | Manual | Cambio disponible para revisión |
| Preparar Python/PostgreSQL y ejecutar pytest | Automático | Resultado de CI e informe JUnit |
| Revisar y fusionar el PR | Manual | Cambio incorporado a `prod` |
| Volver a ejecutar pruebas por el push a `prod` | Automático | Verificación de la versión integrada |
| Construir y publicar en GHCR si las pruebas pasan | Automático | Imagen con etiquetas `latest` y `sha-...` |
| Descargar la imagen, configurar variables y arrancar Compose | Manual | Aplicación ejecutándose desde el artefacto publicado |

Los PR y las ejecuciones manuales del workflow solo ejecutan pruebas. La publicación requiere el evento `push` sobre `prod` y que el job `tests` haya aprobado. El workflow impide publicar si falla ese job; impedir además el merge de un PR fallido requiere configurar la comprobación como obligatoria en las reglas de protección de la rama.

## Evidencias y checklist final de entrega

Los espacios pendientes deben completarse con enlaces y resultados reales. La configuración local no confirma una publicación remota ni la accesibilidad del paquete.

| Evidencia | Enlace o dato que debe registrarse | Estado documental |
|---|---|---|
| Repositorio actualizado | [Rama prod](https://github.com/Juan-bit-006/devops_MovieManager/tree/prod) | Enlace definido; comprobar que contiene la versión final |
| CI exitoso | URL de una ejecución real con la suite completa | Pendiente de registrar |
| CI fallido por una prueba | URL de ejecución y nombre de la prueba que falló | Pendiente de registrar |
| CI corregido | URL de nueva ejecución exitosa después de corregir | Pendiente de registrar |
| Publicación GHCR | URL del job exitoso y del paquete | Pendiente de registrar |
| Artefacto de entrega | Etiqueta exacta `sha-...` publicada y digest de imagen | Pendiente de registrar |
| Descarga y ejecución | Evidencia de `docker pull` y aplicación ejecutada desde esa imagen | Pendiente de registrar |

Para la evidencia de fallo, usar una rama de demostración: cambiar deliberadamente una expectativa de una prueba, abrir PR hacia `prod`, guardar la ejecución fallida, corregir la expectativa y guardar la nueva ejecución exitosa. No fusionar una versión deliberadamente rota. El fallo anterior por falta de pytest demuestra un problema de dependencias; el parcial pide además un fallo provocado por una prueba.

- [ ] Integrar en `prod` los cambios finales y comprobar que no se subió `.env`.
- [ ] Verificar el CRUD y las dos funcionalidades nuevas desde la versión entregada.
- [ ] Ejecutar toda la suite localmente y en GitHub Actions.
- [ ] Registrar evidencias reales de CI exitoso, fallo por prueba y corrección.
- [ ] Confirmar que la publicación depende de las pruebas y guardar una publicación exitosa.
- [ ] Copiar una etiqueta GHCR disponible y probar su descarga y ejecución.
- [ ] Hacer que el otro integrante reproduzca las instrucciones del README.

- [ ] Comprobar el acceso del evaluador al repositorio y al paquete.
- [ ] Completar los enlaces pendientes de las evidencias técnicas.
