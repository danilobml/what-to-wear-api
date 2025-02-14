# Stage 1: Builder
FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev python3-dev build-essential

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.in-project true

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root --without dev

# Stage 2: Runner
FROM python:3.12-slim AS runner

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/.venv /app/.venv

COPY . .

ENV PYTHONPATH=/app
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "what_to_wear.main:app", "--host", "0.0.0.0", "--port", "8000"]
