FROM python:3.10-slim

WORKDIR /app

RUN pip install uv

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY pyproject.toml .
COPY app.py .
COPY log_manager.py .
COPY static/ static/
COPY templates/ templates/

RUN uv pip install --system .

# Run the application
CMD ["gunicorn", "-b", "0.0.0.0:8080", "-w", "1", "--threads", "8", "-t", "0", "app:app"]
