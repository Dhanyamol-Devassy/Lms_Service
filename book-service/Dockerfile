# Use official Python base image
FROM python:3.11-slim

# Create non-root user
RUN useradd -m appuser

# Install mysql-client for wait-for.sh and other essentials
RUN apt-get update && apt-get install -y default-mysql-client && apt-get clean

# Set working directory
WORKDIR /usr/src/app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Change ownership to the non-root user
RUN chown -R appuser:appuser /usr/src/app

# Switch to non-root user
USER appuser

# Expose FastAPI port
EXPOSE 5002

# Default command (also overridden by docker-compose)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5002"]
