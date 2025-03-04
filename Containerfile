# Stage 1: Build dependencies
FROM python:3.10 AS builder

# Install dependencies for building psycopg2
RUN apt-get update && \
    apt-get install -y libpq-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies in a separate layer
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Create final lightweight image
FROM python:3.10-slim

WORKDIR /app

# Copy installed dependencies from the builder stage
COPY --from=builder /install /usr/local

# Copy application source code
COPY ./app .

# Set environment variables to avoid running as root
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 5000

# Start application
CMD ["python", "app.py"]