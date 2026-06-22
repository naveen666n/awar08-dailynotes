# ── Stage 1: base image ──────────────────────────────────────────────────────
FROM python:3.12-slim

# Metadata
LABEL maintainer="vinod"
LABEL description="Live Weather Dashboard — AP & Telangana cities"
LABEL version="1.0"

# Set working directory
WORKDIR /app

# Copy requirements first (layer-cache friendly)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Flask port
EXPOSE 5000

# Non-root user for security
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/')" || exit 1

# Start the app
CMD ["python", "app.py"]
