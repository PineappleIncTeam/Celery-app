FROM python:3.9-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY tasks.py .
ENV CELERY_BROKER_URL=redis://redis-service:6379/0
ENV CELERY_RESULT_BACKEND=redis://redis-service:6379/0
CMD ["celery -A FinanceBackend worker -n workerсurrancy@%h --pool=solo --loglevel=info & celery -A FinanceBackend beat --loglevel=info"]