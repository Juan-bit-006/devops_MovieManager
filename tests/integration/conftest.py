import os

import pytest

from app import create_app
from app.database import db_cursor


@pytest.fixture
def client():
    if not os.environ.get("DB_NAME", "").endswith("_test"):
        pytest.fail("DB_NAME debe terminar en _test. Usa docker-compose.test.yml.")
    app = create_app({"TESTING": True, "SECRET_KEY": "integration-test"})
    with db_cursor() as cursor:
        cursor.execute("TRUNCATE peliculas RESTART IDENTITY")
    try:
        yield app.test_client()
    finally:
        with db_cursor() as cursor:
            cursor.execute("TRUNCATE peliculas RESTART IDENTITY")
