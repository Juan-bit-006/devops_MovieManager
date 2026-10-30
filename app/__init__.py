import os
from flask import Flask


def create_app(config=None):
    app = Flask(__name__)

    app.config.from_mapping(SECRET_KEY=os.environ.get("SECRET_KEY"), INIT_DB=True)
    if config:
        app.config.update(config)
    if not app.config["SECRET_KEY"]:
        raise RuntimeError("Define SECRET_KEY antes de iniciar la aplicacion.")

    # Inicializar PostgreSQL
    from app.database import init_db
    if app.config["INIT_DB"]:
        init_db()

    # Registrar rutas
    from app.routes import main
    app.register_blueprint(main)

    return app