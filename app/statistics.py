from flask import Blueprint, render_template

from app.database import db_cursor


statistics = Blueprint("statistics", __name__)


def obtener_estadisticas():
    with db_cursor() as cursor:
        cursor.execute("""
            SELECT lower(trim(genero)) AS genero, count(*) AS cantidad
            FROM peliculas
            GROUP BY lower(trim(genero))
            ORDER BY cantidad DESC, genero
        """)
        generos = cursor.fetchall()
    return {"total": sum(fila["cantidad"] for fila in generos), "generos": generos}


@statistics.route("/estadisticas")
def resumen():
    return render_template("estadisticas.html", **obtener_estadisticas())
