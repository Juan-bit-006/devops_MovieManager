import pytest

from app.database import listar_peliculas, obtener_pelicula
from app.statistics import obtener_estadisticas

pytestmark = pytest.mark.integration


def pelicula(**cambios):
    form = dict(titulo="Matrix", director="Wachowski", genero="Drama",
                anio_estreno="1999", sinopsis="Una simulación")
    form.update(cambios)
    return form


def registrar(client, **cambios):
    assert client.post("/peliculas/nueva", data=pelicula(**cambios)).status_code == 302
    return listar_peliculas()[0]["id"]


def test_crud_persiste_y_conserva_comportamiento(client):
    assert client.get("/").status_code == 200
    assert client.get("/peliculas/nueva").status_code == 200
    identificador = registrar(client)
    assert obtener_pelicula(identificador)["titulo"] == "Matrix"
    assert b"Matrix" in client.get("/").data
    assert client.get(f"/peliculas/editar/{identificador}").status_code == 200
    assert client.post(f"/peliculas/editar/{identificador}",
                       data=pelicula(titulo="Matrix Reloaded")).status_code == 302
    assert obtener_pelicula(identificador)["titulo"] == "Matrix Reloaded"
    assert client.post(f"/peliculas/eliminar/{identificador}").status_code == 302
    assert obtener_pelicula(identificador) is None


def test_validacion_no_modifica_base_y_conserva_formulario(client):
    assert client.post("/peliculas/nueva", data=pelicula(titulo=" ")).status_code == 400
    assert listar_peliculas() == []
    identificador = registrar(client)
    response = client.post(f"/peliculas/editar/{identificador}",
                           data=pelicula(titulo="Intento", anio_estreno="abc"))
    assert response.status_code == 400
    assert b"Intento" in response.data
    assert obtener_pelicula(identificador)["titulo"] == "Matrix"


def test_inexistentes_y_eliminacion_solo_post(client):
    for metodo, ruta in [("get", "/peliculas/editar/999"),
                         ("post", "/peliculas/editar/999"),
                         ("post", "/peliculas/eliminar/999")]:
        assert getattr(client, metodo)(ruta).status_code == 404
    assert client.get("/peliculas/eliminar/999").status_code == 405


@pytest.mark.parametrize("termino,esperados", [
    ("aTr", ["Matrix"]), ("wach", ["Matrix"]), ("", ["Matrix", "Arrival"]),
    ("   ", ["Matrix", "Arrival"]), ("inexistente", []),
    ("%", []), ("_", []), ("' OR 1=1 --", []),
])
def test_busqueda_titulo_director_y_texto_literal(client, termino, esperados):
    registrar(client)
    registrar(client, titulo="Arrival", director="Denis Villeneuve")
    response = client.get("/", query_string={"q": termino})
    assert response.status_code == 200
    assert b'name="q"' in response.data
    for titulo in ("Matrix", "Arrival"):
        assert (titulo.encode() in response.data) == (titulo in esperados)
    if not esperados:
        assert b"No se encontraron resultados" in response.data


def test_estadisticas_vacias_y_actualizacion_tras_crud(client):
    assert obtener_estadisticas() == {"total": 0, "generos": []}
    assert "No hay películas" in client.get("/estadisticas").text
    primero = registrar(client, genero=" Drama ")
    segundo = registrar(client, titulo="Otra", genero="DRAMA")
    assert obtener_estadisticas() == {
        "total": 2, "generos": [{"genero": "drama", "cantidad": 2}]}
    assert client.post(f"/peliculas/editar/{primero}",
                       data=pelicula(genero="Comedia")).status_code == 302
    assert obtener_estadisticas() == {"total": 2, "generos": [
        {"genero": "comedia", "cantidad": 1}, {"genero": "drama", "cantidad": 1}]}
    assert b"comedia" in client.get("/estadisticas").data
    assert client.post(f"/peliculas/eliminar/{segundo}").status_code == 302
    assert obtener_estadisticas() == {
        "total": 1, "generos": [{"genero": "comedia", "cantidad": 1}]}
