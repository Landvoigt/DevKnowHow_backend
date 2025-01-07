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

ENV DJANGO_SETTINGS_MODULE=knowledge_base.settings
ENV PYTHONUNBUFFERED=1
ENV DEBUG=False

# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
RUN python3 manage.py collectstatic --noinput
CMD ["gunicorn", "knowledge_base.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]