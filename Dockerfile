# Brug et officielt Python runtime som base image
FROM python:3.10-slim

# Sæt arbejdsdirectory i containeren
WORKDIR /app

# Kopier requirements filen til containeren
COPY requirements.txt /app/

# Installer eventuelle nødvendige pakker
RUN pip install --no-cache-dir -r requirements.txt

# Kopier din applikationskildekode til containeren
COPY . /app

# Gør port 5000 tilgængelig uden for containeren
EXPOSE 5000

# Definer miljøvariabel
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the application
CMD ["flask", "run"]
