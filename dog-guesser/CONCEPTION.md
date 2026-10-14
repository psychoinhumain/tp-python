# CONCEPTION - Dog Guesser

## Travail avec l'IA

- Demandé à l'IA : une structure globale pour l'application, l'intégration de l'API Dog API (cache, extraction de la race depuis l'URL) et des idées de règles de calcul du score.
- Refusé / modifié : le barème a été ajusté pour valoriser la prise de risque et la régularité sans pénaliser les erreurs, afin de garder un jeu dynamique et accessible.

## Choix de conception

- Interface : NiceGUI, pour construire une interface web dynamique en pur Python, sans JavaScript ni HTML à écrire.
- Format : 10 manches par partie, court et agréable.
- Barème (inspiré de Kahoot) :
  - 100 points par bonne réponse.
  - Bonus de rapidité : de +10 (réponse en 9 secondes) à +100 (réponse immédiate), dans la limite de 10 secondes.
  - Bonus de série : +25 par bonne réponse d'affilée, plafonné à +100.
  - Erreur : 0 point et série remise à 0.
- Sauvegarde : fichier `scores.json` côté serveur, sans base de données.
- Temps réel : le classement se met à jour chez tous les joueurs connectés à la fin de chaque partie, grâce au composant rafraîchissable de NiceGUI.
- Retour immédiat après chaque réponse, avec la race exacte (côté pédagogique), puis message de record personnel et rang au classement en fin de partie.

## Limites

- Les noms de races sont uniquement en anglais (limite de l'API).
- Les propositions fausses sont tirées au hasard : pas de niveaux de difficulté.
- Pas d'authentification : n'importe qui peut réutiliser un pseudo.
- Certaines photos de l'API sont ambiguës (plusieurs chiens, croisements, mauvais cadrage).
