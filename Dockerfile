# FROM python:3.11-slim
# Pin to a stable Debian base
FROM python:3.11-slim-bookworm

# --- System deps: Java (required for Spark) ---
RUN apt-get update \
  && apt-get install -y --no-install-recommends openjdk-17-jre-headless ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME dynamically (works on Apple Silicon/arm64 and Intel/amd64)
RUN set -eux; \
  JAVA_BIN="$(readlink -f "$(command -v java)")"; \
  JAVA_HOME_DIR="$(dirname "$(dirname "$JAVA_BIN")")"; \
  ln -s "$JAVA_HOME_DIR" /opt/java-home

ENV JAVA_HOME=/opt/java-home
ENV PATH="$JAVA_HOME/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# --- Python deps ---
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# --- App code ---
COPY pyproject.toml /app/pyproject.toml
COPY src/ /app/src/
RUN pip install --no-cache-dir -e .

# Default command (override in `docker run` if you want)
CMD ["python", "-m", "pyspark_ingestion.jobs.main_job", "--master", "local[*]", "--input", "data/lap_times.csv"]
