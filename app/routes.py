from flask import Blueprint, render_template

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/peliculas/nueva")
def nueva_pelicula():
    return render_template("formulario.html")