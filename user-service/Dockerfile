# Use official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /usr/src/app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . .

# Expose port for the FastAPI application
EXPOSE 5001

# Command to run FastAPI with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5001"]
