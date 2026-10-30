
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

from app.database import listar_peliculas, obtener_pelicula, crear_pelicula, actualizar_pelicula, eliminar_pelicula


from app.validators import validar_pelicula


main = Blueprint("main", __name__)

# CONSULTAR PELÍCULAS
@main.route("/")
def index():

    busqueda = request.args.get("q", "").strip()
    peliculas = listar_peliculas(busqueda)

    return render_template(
        "index.html",
        peliculas=peliculas,
        busqueda=busqueda
    )


# REGISTRAR PELÍCULA
@main.route("/peliculas/nueva", methods=["GET", "POST"])
def nueva_pelicula():

    if request.method == "POST":

        try:
            datos = validar_pelicula(request.form)
        except ValueError as error:
            flash(str(error))
            return render_template("formulario.html", pelicula=None), 400

        crear_pelicula(datos)

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

        try:
            datos = validar_pelicula(request.form)
        except ValueError as error:
            flash(str(error))
            return render_template("formulario.html", pelicula=pelicula), 400

        actualizado = actualizar_pelicula(pelicula_id, datos)

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
