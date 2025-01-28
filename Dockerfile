FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    --no-install-recommends \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=devknowhow.settings
ENV PYTHONUNBUFFERED=1
ENV DEBUG=False

ENTRYPOINT ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn devknowhow.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
