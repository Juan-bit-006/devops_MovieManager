
import os
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor


def connect():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=int(os.environ.get("DB_PORT", "5432")),
        dbname=os.environ.get("DB_NAME", "moviemanager"),
        user=os.environ.get("DB_USER", "moviemanager"),
        password=os.environ.get("DB_PASSWORD", ""),
        connect_timeout=5
    )


@contextmanager
def db_cursor():
    conn = connect()

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            yield cursor

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def init_db():
    with db_cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS peliculas (
                id SERIAL PRIMARY KEY,
                titulo VARCHAR(150) NOT NULL,
                director VARCHAR(100) NOT NULL,
                genero VARCHAR(50) NOT NULL,
                anio_estreno INTEGER NOT NULL
                    CHECK (anio_estreno BETWEEN 1888 AND 2200),
                sinopsis TEXT
            )
        """)


def listar_peliculas():
    with db_cursor() as cursor:
        cursor.execute(
            "SELECT * FROM peliculas ORDER BY id DESC"
        )
        return cursor.fetchall()


def obtener_pelicula(pelicula_id):
    with db_cursor() as cursor:
        cursor.execute(
            "SELECT * FROM peliculas WHERE id = %s",
            (pelicula_id,)
        )
        return cursor.fetchone()


def crear_pelicula(datos):
    with db_cursor() as cursor:
        cursor.execute("""
            INSERT INTO peliculas
                (titulo, director, genero, anio_estreno, sinopsis)
            VALUES (%s, %s, %s, %s, %s)
        """, datos)


def actualizar_pelicula(pelicula_id, datos):
    with db_cursor() as cursor:
        cursor.execute("""
            UPDATE peliculas
            SET titulo = %s,
                director = %s,
                genero = %s,
                anio_estreno = %s,
                sinopsis = %s
            WHERE id = %s
        """, (*datos, pelicula_id))

        return cursor.rowcount > 0


def eliminar_pelicula(pelicula_id):
    with db_cursor() as cursor:
        cursor.execute(
            "DELETE FROM peliculas WHERE id = %s",
            (pelicula_id,)
        )

        return cursor.rowcount > 0