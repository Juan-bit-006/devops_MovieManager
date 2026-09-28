
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

from app.database import listar_peliculas, obtener_pelicula, crear_pelicula, actualizar_pelicula, eliminar_pelicula


main = Blueprint("main", __name__)

# CONSULTAR PELÍCULAS
@main.route("/")
def index():

    peliculas = listar_peliculas()

    return render_template(
        "index.html",
        peliculas=peliculas
    )


# REGISTRAR PELÍCULA
@main.route("/peliculas/nueva", methods=["GET", "POST"])
def nueva_pelicula():

    if request.method == "POST":

        titulo = request.form.get("titulo", "").strip()
        director = request.form.get("director", "").strip()
        genero = request.form.get("genero", "").strip()
        anio = request.form.get("anio_estreno", "").strip()
        sinopsis = request.form.get("sinopsis", "").strip()

        if not titulo or not director or not genero or not anio:
            flash("Todos los campos obligatorios deben completarse.")
            return render_template(
                "formulario.html",
                pelicula=None
            ), 400

        try:
            anio = int(anio)
        except ValueError:
            flash("El año debe ser un número válido.")
            return render_template(
                "formulario.html",
                pelicula=None
            ), 400

        if not 1888 <= anio <= 2200:
            flash("El año debe estar entre 1888 y 2200.")
            return render_template(
                "formulario.html",
                pelicula=None
            ), 400

        crear_pelicula((
            titulo,
            director,
            genero,
            anio,
            sinopsis
        ))

        flash("Película registrada correctamente.")

        return redirect(url_for("main.index"))

    return render_template(
        "formulario.html",
        pelicula=None
    )


# MODIFICAR PELÍCULA
@main.route(
    "/peliculas/editar/<int:pelicula_id>",
    methods=["GET", "POST"]
)
def editar_pelicula(pelicula_id):

    pelicula = obtener_pelicula(pelicula_id)

    if pelicula is None:
        abort(404)

    if request.method == "POST":

        titulo = request.form.get("titulo", "").strip()
        director = request.form.get("director", "").strip()
        genero = request.form.get("genero", "").strip()
        anio = request.form.get("anio_estreno", "").strip()
        sinopsis = request.form.get("sinopsis", "").strip()

        if not titulo or not director or not genero or not anio:
            flash("Todos los campos obligatorios deben completarse.")
            return render_template(
                "formulario.html",
                pelicula=pelicula
            ), 400

        try:
            anio = int(anio)
        except ValueError:
            flash("El año debe ser un número válido.")
            return render_template(
                "formulario.html",
                pelicula=pelicula
            ), 400

        if not 1888 <= anio <= 2200:
            flash("El año debe estar entre 1888 y 2200.")
            return render_template(
                "formulario.html",
                pelicula=pelicula
            ), 400

        actualizado = actualizar_pelicula(
            pelicula_id,
            (
                titulo,
                director,
                genero,
                anio,
                sinopsis
            )
        )

        if not actualizado:
            abort(404)

        flash("Película modificada correctamente.")

        return redirect(url_for("main.index"))

    return render_template(
        "formulario.html",
        pelicula=pelicula
    )


# ELIMINAR PELÍCULA
@main.route(
    "/peliculas/eliminar/<int:pelicula_id>",
    methods=["POST"]
)
def borrar_pelicula(pelicula_id):

    eliminada = eliminar_pelicula(pelicula_id)

    if not eliminada:
        abort(404)

    flash("Película eliminada correctamente.")

    return redirect(url_for("main.index"))
