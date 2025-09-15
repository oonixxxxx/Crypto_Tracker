# Crypto_Tracker

https://coinmarketcap.com/api/



Создание приложения

python -m venv venv

cd app cd backend 
python -m uvicorn src.main:app --reload



как запустить:

Бэкенд fastapi

в корне проекта: uvicorn app.backend.src.main:app --host 0.0.0.0 --port 8000

или через Docker 
docker build -t crypto-backend app
docker run -p 8000:8000 crypto-backend

2) Бот

Укажите TOKEN в app/bot/config.py
Запустите python app/bot/bot.py

Проверка в Telegram:
Отправьте /crypto — бот вернёт первую монету из списка.
Отправьте /crypto_id 1 — бот вернёт данные для монеты с ID 1.


Важно:
Убедитесь, что FastAPI запущен локально на http://localhost:8000, чтобы бот смог получить данные.
В app/backend/src/router.py идёт импорт from . import cmc_client — убедитесь, что модуль существует и экспортирует функции get_listings() и get_currency(id). Если его нет, нужно либо создать cmc_client с использованием CMCHTTPClient из http_client.py, либо заменить импорт на корректный.
Я добавил BACKEND_URL и обновил команды бота, чтобы брать данные из FastAPI. Теперь данные из FastAPI “передаются” в модуль бота через HTTP-запросы.