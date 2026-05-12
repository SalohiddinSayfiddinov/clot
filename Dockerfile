# Stage 1: Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies needed for building packages (like psycopg2)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies into a temporary location
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# Stage 2: Final Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Install only the runtime system libraries (libpq is needed for Postgres)
RUN apt-get update && apt-get install -y \
    libpq5 \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Copy installed python packages from the builder stage
COPY --from=builder /install /usr/local

# Copy the application code
COPY . .

# Create a non-privileged user to run the app (Security Best Practice)
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Expose the port FastAPI runs on
EXPOSE 8000

# Production command using Gunicorn with Uvicorn workers for stability/concurrency
CMD ["uvicorn", "app.main:app", "--bind", "0.0.0.0:8000"]