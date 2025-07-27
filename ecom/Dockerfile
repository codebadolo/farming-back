# Dockerfile pour l'application Django E-commerce

FROM python:3.11-slim

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Répertoire de travail
WORKDIR /app

# Installation des dépendances système
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        default-libmysqlclient-dev \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Installation des dépendances Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . /app/

# Création des répertoires pour les médias et statiques
RUN mkdir -p /app/media /app/static

# Collection des fichiers statiques
RUN python manage.py collectstatic --noinput

# Exposition du port
EXPOSE 8000

# Commande par défaut
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "source.wsgi:application"]