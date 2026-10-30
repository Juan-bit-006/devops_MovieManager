def validar_pelicula(form):
    """Normaliza campos y devuelve datos listos para persistir."""
    titulo, director, genero, anio, sinopsis = (
        form.get(campo, "").strip()
        for campo in ("titulo", "director", "genero", "anio_estreno", "sinopsis")
    )
    if not all((titulo, director, genero, anio)):
        raise ValueError("Todos los campos obligatorios deben completarse.")
    if len(titulo) > 150 or len(director) > 100 or len(genero) > 50:
        raise ValueError("Longitud máxima: título 150, director 100 y género 50 caracteres.")
    try:
        anio = int(anio)
    except ValueError:
        raise ValueError("El año debe ser un número válido.") from None
    if not 1888 <= anio <= 2200:
        raise ValueError("El año debe estar entre 1888 y 2200.")
    return titulo, director, genero, anio, sinopsis
