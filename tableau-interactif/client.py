"""Client en ligne de commande : demande une forme et l'envoie au serveur."""
import random
import sys

import requests

URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080"

# nom API, libellé, [(champ, question posée à l'utilisateur)]
SHAPES = {
    "1": ("point", "Point", [
        ("x", "Position horizontale"),
        ("y", "Position verticale"),
    ]),
    "2": ("line", "Ligne", [
        ("x1", "Départ, position horizontale"),
        ("y1", "Départ, position verticale"),
        ("x2", "Arrivée, position horizontale"),
        ("y2", "Arrivée, position verticale"),
    ]),
    "3": ("circle", "Cercle", [
        ("x", "Position horizontale"),
        ("y", "Position verticale"),
        ("radius", "Rayon"),
    ]),
    "4": ("rectangle", "Rectangle", [
        ("x", "Position horizontale"),
        ("y", "Position verticale"),
        ("width", "Largeur"),
        ("height", "Hauteur"),
    ]),
    "5": ("square", "Carré", [
        ("x", "Position horizontale"),
        ("y", "Position verticale"),
        ("cote", "Côté"),
    ]),
}


def ask_number(question):
    while True:
        raw = input(f"  {question} : ").strip()
        try:
            return float(raw) if "." in raw else int(raw)
        except ValueError:
            print("  Valeur invalide, veuillez saisir un nombre.")


def ask_color():
    while True:
        raw = input("  Couleur RGB (vide = aléatoire) : ").strip()
        if not raw:
            return [random.randint(0, 255) for _ in range(3)]
        try:
            color = [int(c) for c in raw.split(",")]
            if len(color) == 3 and all(0 <= c <= 255 for c in color):
                return color
        except ValueError:
            pass
        print("  Format invalide, saisissez trois valeurs de 0 à 255, exemple : 120,200,102")


def send(path, body=None):
    try:
        resp = requests.post(f"{URL}{path}", json=body, timeout=5)
    except requests.exceptions.ConnectionError:
        print("Erreur : serveur injoignable. Vérifiez qu'il est lancé.")
        return
    except requests.exceptions.Timeout:
        print("Erreur : le serveur n'a pas répondu à temps.")
        return
    except requests.exceptions.RequestException as err:
        print(f"Erreur réseau : {err}")
        return
    if resp.ok:
        print(f"Envoyé ({resp.json().get('clients', 0)} tableau(x) connecté(s)).")
    else:
        try:
            print(f"Refusé par le serveur : {resp.json().get('message')}")
        except ValueError:
            print(f"Erreur HTTP {resp.status_code}")


def ask_shape(key):
    """Pose les questions d'une forme et renvoie le corps JSON."""
    name, label, fields = SHAPES[key]
    print(f"\n{label} :")
    body = {"shape": name}
    for field, question in fields:
        body[field] = ask_number(question)
    body["color"] = ask_color()
    return body


def recap(body):
    label = next(lbl for n, lbl, _ in SHAPES.values() if n == body["shape"])
    values = ", ".join(f"{k}={v}" for k, v in body.items() if k not in ("shape", "color"))
    return f"{label} ({values}), couleur {tuple(body['color'])}"


def ask_house():
    """Préréglage : une maison faite de 4 formes (mur, deux lignes de toit, porte)."""
    print("\nMaison :")
    x = ask_number("Position horizontale")
    y = ask_number("Position verticale")
    side = ask_number("Taille")
    color = ask_color()
    half = side // 2
    return [
        {"shape": "square", "x": x, "y": y, "cote": side, "color": color},
        {"shape": "line", "x1": x, "y1": y, "x2": x + half, "y2": y - half, "color": color},
        {"shape": "line", "x1": x + half, "y1": y - half, "x2": x + side, "y2": y, "color": color},
        {"shape": "rectangle", "x": x + side * 3 // 8, "y": y + half,
         "width": side // 4, "height": half, "color": [255, 255, 255]},
    ]


def compose():
    """Forme composée : plusieurs formes envoyées en une seule requête."""
    items = []
    print("\nForme composée : ajoutez des formes, puis envoyez-les d'un seul coup.")
    while True:
        print(f"\nForme composée ({len(items)} élément(s))")
        for key, (_, label, _) in SHAPES.items():
            print(f"  {key}  {label}")
        print("  m  Maison")
        print("  e  Envoyer")
        print("  a  Annuler")
        choice = input("Choix : ").strip().lower()
        if not choice:
            continue
        if choice == "a":
            print("Annulé.")
            return
        if choice == "e":
            if not items:
                print("Ajoutez au moins une forme.")
                continue
            send("/draw", items)
            return
        if choice == "m":
            items.extend(ask_house())
            print("Maison ajoutée.")
        elif choice in SHAPES:
            body = ask_shape(choice)
            items.append(body)
            print(f"Ajouté : {recap(body)}")
        else:
            print("Choix inconnu.")


def main():
    print(f"Serveur cible : {URL}")
    print("Tableau de 800 par 600, origine (0, 0) en haut à gauche.")
    while True:
        print("\nQue souhaitez-vous dessiner ?")
        for key, (_, label, _) in SHAPES.items():
            print(f"  {key}  {label}")
        print("  6  Forme composée")
        print("  c  Effacer le tableau")
        print("  q  Quitter")
        choice = input("Choix : ").strip().lower()
        if not choice:
            continue
        if choice == "q":
            break
        if choice == "c":
            send("/clear")
        elif choice == "6":
            compose()
        elif choice in SHAPES:
            body = ask_shape(choice)
            print(f"Envoi : {recap(body)}")
            send("/draw", body)
        else:
            print("Choix inconnu. Saisissez un chiffre de 1 à 6, c ou q.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print()
