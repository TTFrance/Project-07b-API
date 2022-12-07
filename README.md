# Project-07b-API

# API
- created using FastAPI
- hosted on Heroku

# Requirements
- Connectez le référentiel à un projet Heroku, le procfile et requirements.txt sont les configurations

# Endpoints
## /getids/
- in: None
- out: une liste d'ID client qui peuvent ensuite être utilisés dans le point de terminaison de prédiction

## /predict/
- in: un identifiant client valide (de /getids/)
- out: un float de 0 à 1 indiquant la prédiction du modèle pour la probabilité de défaut
