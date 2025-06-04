FROM python:3.9-slim

WORKDIR /app

# Installer les dépendances système (libpq-dev si PostgreSQL est utilisé)
RUN apt-get update && apt-get install -y libpq-dev

# Copier le fichier requirements.txt
COPY requirement.txt .

RUN pip install --no-cache-dir -r requirement.txt

COPY . .

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

