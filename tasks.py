import os
import requests
import redis
import json
from celery import Celery
from dotenv import load_dotenv
from currency_db import upsert_currency_data, get_all_currency_data

load_dotenv()

app = Celery('standalone_tasks', broker=os.getenv('CELERY_BROKER_URL'))
app.conf.broker_connection_retry_on_startup = True

# Redis клиент
redis_client = redis.Redis.from_url(os.getenv('REDIS_URL'))

# Расписание задач
app.conf.beat_schedule = {
    'fetch-currency-daily': {
        'task': 'tasks.fetch_currency_data',
        'schedule': 86400.0,  # 24 часа
    },
    'update-redis-hourly': {
        'task': 'tasks.update_redis',
        'schedule': 3600.0,   # 1 час
    },
}

@app.task
def fetch_currency_data():
    url = "https://api.apilayer.com/currency_data/live"
    api_key = os.getenv("CURRENCY_API_KEY")
    params_list = [
        {"source": "USD", "currencies": "RUB"},
        {"source": "EUR", "currencies": "RUB"},
        {"source": "BTC", "currencies": "RUB"},
    ]
    headers = {"apikey": api_key}

    for params in params_list:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json().get("quotes", {})
            for currency, rate in data.items():
                upsert_currency_data(currency, rate)
        else:
            print(f"Error {response.status_code}: {response.text}")

@app.task
def update_redis():
    data = get_all_currency_data()
    redis_client.set("currency_data", json.dumps(data), ex=4200)  # timeout 70 мин