FROM python:3.13-slim


# Установка зависимостей системы
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    wget \
    libpq-dev \
    pkg-config \
    postgresql-client \
  && rm -rf /var/lib/apt/lists/*

# Установка grpc_health_probe
RUN GRPC_HEALTH_PROBE_VERSION=v0.4.24 && \
    wget -qO/bin/grpc_health_probe https://github.com/grpc-ecosystem/grpc-health-probe/releases/download/${GRPC_HEALTH_PROBE_VERSION}/grpc_health_probe-linux-amd64 && \
    chmod +x /bin/grpc_health_probe

# Установка Poetry через pip
RUN pip install --no-cache-dir poetry

# Настройки Poetry
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Создание рабочей директории
WORKDIR /app

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod 755 /usr/local/bin/entrypoint.sh \
    && sed -i 's/\r$//' /usr/local/bin/entrypoint.sh

# Копирование файлов Poetry
COPY pyproject.toml poetry.lock* /app/

# Установка зависимостей проекта
RUN poetry install --only main --no-root

# Копирование исходного кода
COPY . /app

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
