FROM python:3.9-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["celery -A FinanceBackend worker -n workerсurrancy@%h --pool=solo --loglevel=info & celery -A FinanceBackend beat --loglevel=info"]