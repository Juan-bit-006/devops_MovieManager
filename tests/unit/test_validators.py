import pytest
from app import create_app
from app.validators import validar_pelicula


def datos(**cambios):
    form = dict(titulo=" Matrix ", director=" Wachowski ", genero=" Drama ",
                anio_estreno="1999", sinopsis=" Sinopsis ")
    form.update(cambios)
    return form


def test_normaliza_datos():
    assert validar_pelicula(datos()) == ("Matrix", "Wachowski", "Drama", 1999, "Sinopsis")


@pytest.mark.parametrize("campo,valor", [
    ("titulo", " "), ("director", ""), ("genero", ""), ("anio_estreno", ""),
    ("anio_estreno", "abc"), ("anio_estreno", "1999.5"),
    ("anio_estreno", "1887"), ("anio_estreno", "2201"),
    ("titulo", "x" * 151), ("director", "x" * 101), ("genero", "x" * 51),
])
def test_rechaza_datos_invalidos(campo, valor):
    with pytest.raises(ValueError):
        validar_pelicula(datos(**{campo: valor}))


@pytest.mark.parametrize("anio", ["1888", "2200"])
def test_acepta_limites_del_anio(anio):
    assert validar_pelicula(datos(anio_estreno=anio))[3] == int(anio)


def test_app_sin_base_para_pruebas_unitarias():
    app = create_app({"TESTING": True, "SECRET_KEY": "unit-test", "INIT_DB": False})
    assert app.test_client().get("/ruta-inexistente").status_code == 404
