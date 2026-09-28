import os
from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

    # Inicializar PostgreSQL
    from app.database import init_db
    init_db()

    # Registrar rutas
    from app.routes import main
    app.register_blueprint(main)

    return app