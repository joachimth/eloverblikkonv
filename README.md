# Flask Docker Applikation

Dette repository indeholder en Flask-applikation, som er klar til at blive bygget og kørt i en Docker-container.

## Beskrivelse

Denne Flask-applikation tilbyder en simpel webgrænseflade til at uploade en CSV-fil, konvertere dataene og downloade det bearbejdede resultat. 

## Forudsætninger

For at bruge dette projekt skal du have følgende installeret:

- Docker
- Git (valgfrit, hvis du klone repository)

## Installation og Opsætning

1. **Klon repository (valgfrit):**

git clone https://github.com/ditbrugernavn/ditrepositorynavn.git
cd ditrepositorynavn

2. **Byg Docker Container:**

docker build -t ditbrugernavn/dinflaskapp .

3. **Kør Container:**

docker run -d -p 5000:5000 ditbrugernavn/dinflaskapp

Appen vil nu køre på `http://localhost:5000`.

## Brug

Åbn din webbrowser og gå til `http://localhost:5000`. Her kan du uploade en CSV-fil og modtage en konverteret fil baseret på dine specifikationer.

## Bidrag

Feedback og bidrag til projektet er velkomne. Du kan foreslå ændringer via pull requests.

## Licens

Angiv licensoplysninger her.
