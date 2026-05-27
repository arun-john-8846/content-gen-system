# ADAP Content Gen Web — Dockerfile

FROM python:3.12-slim

# System deps for Playwright (used by serp_research.py — local research only)
# and python-docx (lxml)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libxkbcommon0 \
    libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 \
    libcairo2 libasound2 libxshmfence1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Create data directory for SQLite + output on persistent volume
RUN mkdir -p /data

# Default environment
ENV DATABASE_PATH=/data/adap.db \
    PORT=8080 \
    FLASK_SECRET_KEY=change-me-via-flyctl-secrets

EXPOSE 8080

# Use gunicorn with 1 worker (SQLite is not safe for concurrent writes with multiple workers)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "4", \
     "--timeout", "300", "--worker-class", "gthread", "app:app"]
