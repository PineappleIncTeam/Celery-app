FROM python:3.9-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["sh", "-c", "celery -A tasks worker -n workercurrency@%h --pool=solo --loglevel=info & celery -A tasks beat --loglevel=info"]