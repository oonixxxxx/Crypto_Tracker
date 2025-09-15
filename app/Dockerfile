FROM python:3.9-slim

#рабочая папка
WORKDIR /app

# Установка зависимостей для разработки
COPY backend/requirements.txt .
#установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt
#установка pytest и pytest-cov
RUN pip install pytest pytest-cov

# Копирование кода приложения
COPY backend .
#команда по умолчанию для продакшена
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]