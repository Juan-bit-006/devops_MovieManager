
FROM python:3.12-slim AS base

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

FROM base AS test
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt
COPY app/ ./app/
COPY tests/ ./tests/
COPY pytest.ini .
CMD ["python", "-m", "pytest", "-v"]

FROM base AS runtime
COPY app/ ./app/
COPY run.py .

EXPOSE 5000

CMD ["python", "run.py"]
