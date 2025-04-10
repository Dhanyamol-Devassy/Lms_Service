# Use official Python image (non-root user base)
FROM python:3.11-slim

# Add non-root user
RUN adduser --disabled-password --gecos '' appuser

# Install dependencies
RUN apt-get update && apt-get install -y default-mysql-client && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /usr/src/app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Change ownership to the non-root user
RUN chown -R appuser:appuser /usr/src/app

# Change to non-root user
USER appuser

# Expose port
EXPOSE 5003

# Default command (this is overridden by docker-compose)
CMD ["flask", "--app", "app.main:create_app", "run", "--host=0.0.0.0", "--port=5003"]


