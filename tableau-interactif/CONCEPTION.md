# CONCEPTION

## Démarche avec l'IA

1. Je lui ai fourni l'énoncé complet (Partie II) et demandé une première version du projet : serveur, page web, client.
2. J'ai lancé le résultat, observé ce qui s'affichait et identifié ce qui n'allait pas. Je suis ensuite revenu avec des demandes précises, une à la fois.
3. J'ai relu et validé chaque modification avant de passer à la suivante.

## Choix de conception

- **Un seul serveur** (aiohttp) pour l'API HTTP `/draw` et le canal WebSocket `/ws`. Cela évite de lancer deux programmes et de gérer deux ports.
- **API conforme au sujet** : mêmes formes, mêmes champs, couleur au format `[r, g, b]`.
- **Validation côté serveur** : une requête incorrecte reçoit une erreur 400 avec un message clair, au lieu d'envoyer une forme invalide aux tableaux.
- **Historique en mémoire** : un tableau qui se connecte en cours de route reçoit toutes les formes déjà dessinées.
- **Reconnexion automatique** de la page si la connexion WebSocket est perdue.
- **Formes composées** : `/draw` accepte aussi une liste de formes, validée en bloc (tout est accepté ou tout est refusé). Le client propose une option pour assembler plusieurs formes, avec un préréglage « maison ».
- **Route `/clear`** pour effacer le tableau chez tous les clients.

## Ce que j'ai impulsé

- **Coordonnées visibles** : je ne pouvais pas vérifier si les formes étaient bien créées. J'ai demandé d'afficher les coordonnées sur le tableau, la position de la souris, et une liste des formes reçues.
- **Questions du client simplifiées** : les libellés `x1`, `y2` étaient incompréhensibles. J'ai demandé de les remplacer par « Position horizontale » et « Position verticale », sans détails superflus.
- **Couleur** : libellé réduit à « Couleur RGB (vide = aléatoire) ».
- **Menu du client** : la ligne unique était peu lisible, je l'ai fait remplacer par une liste verticale.
- **Curseur** : j'ai refusé le réticule en pointillés sur le tableau, le curseur par défaut suffit.

## Limites

- Les formes ne sont pas sauvegardées sur disque : l'historique disparaît au redémarrage du serveur.
- On ne peut pas dessiner à la souris, uniquement via le client en ligne de commande.
- Le tableau a une taille fixe de 800 par 600.
