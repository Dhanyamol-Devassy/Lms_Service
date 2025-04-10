FROM python:3.11-slim

# Add non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Install mysql-client for wait-for.sh and other essentials
RUN apt-get update && apt-get install -y default-mysql-client && apt-get clean

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER appuser

CMD ["sh", "-c", "chmod +x wait-for.sh && ./wait-for.sh mysql uvicorn app.main:app --host=0.0.0.0 --port=5001 --reload"]
