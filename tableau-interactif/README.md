# Tableau interactif

Tableau de dessin partagé en temps réel : un serveur Python (HTTP + WebSocket), une page web (canvas) et un client en ligne de commande.

## Installation

```
pip install -r requirements.txt
```

## Lancement

1. Serveur : `python server.py`
2. Tableau : ouvrir http://localhost:8080 dans un ou plusieurs navigateurs
3. Client : `python client.py` (adresse du serveur en argument optionnel : `python client.py http://localhost:8080`)

## API

`POST /draw` avec un corps JSON (point, line, circle, rectangle, square, couleur au format [r, g, b]). Le corps peut aussi être une liste de formes pour une forme composée. `POST /clear` efface le tableau.
