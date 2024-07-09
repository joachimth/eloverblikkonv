# Brug et officielt Python runtime som base image
FROM python:3.10

# Sæt arbejdsdirectory i containeren
WORKDIR /usr/src/app

# Kopier requirements filen til containeren
COPY requirements.txt ./

# Installer eventuelle nødvendige pakker
RUN pip install --no-cache-dir -r requirements.txt

# Kopier din applikationskildekode til containeren
COPY . .

# Gør port 5000 tilgængelig uden for containeren
EXPOSE 5000

# Definer miljøvariabel
ENV FLASK_ENV=production

# Kør applikationen, når containeren starter
CMD ["flask", "run", "--host=0.0.0.0"]
