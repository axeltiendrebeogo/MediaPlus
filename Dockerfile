# --------------------------------------------------------------------
# MediaPulse — Backend Django
# Image pour déploiement sur Render (service Docker)
# --------------------------------------------------------------------
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dépendances système :
# - build-essential / libpq-dev : compilation psycopg2 si besoin
# - libcairo2, libpango-1.0-0, libpangocairo-1.0-0, libgdk-pixbuf2.0-0,
#   libffi-dev, shared-mime-info, fonts-liberation : requis par WeasyPrint
#   pour générer les PDF des rapports
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn whitenoise

COPY . .

RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
