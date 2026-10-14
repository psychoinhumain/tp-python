"""Accès à l'API dog.ceo et fabrication d'une question de quiz."""
import random

import requests

BASE_URL = "https://dog.ceo/api"
_breeds_cache = []


def format_breed(folder):
    """'hound-afghan' -> 'Afghan Hound', 'beagle' -> 'Beagle'."""
    main, _, sub = folder.partition("-")
    sub = sub.replace("-", " ")
    return f"{sub} {main}".strip().title()


def get_breeds():
    """Liste de toutes les races (mise en cache après le 1er appel)."""
    if not _breeds_cache:
        response = requests.get(f"{BASE_URL}/breeds/list/all", timeout=10)
        response.raise_for_status()
        for main, subs in response.json()["message"].items():
            if subs:
                _breeds_cache.extend(format_breed(f"{main}-{s}") for s in subs)
            else:
                _breeds_cache.append(format_breed(main))
    return _breeds_cache


def breed_from_url(image_url):
    """Extrait la race depuis l'URL de l'image (.../breeds/<race>/<fichier>)."""
    folder = image_url.split("/breeds/")[1].split("/")[0]
    return format_breed(folder)


def get_question():
    """Renvoie {'image', 'correct', 'choices'} avec 4 propositions mélangées."""
    breeds = get_breeds()
    response = requests.get(f"{BASE_URL}/breeds/image/random", timeout=10)
    response.raise_for_status()
    image = response.json()["message"]
    correct = breed_from_url(image)
    wrong = random.sample([b for b in breeds if b != correct], 3)
    choices = wrong + [correct]
    random.shuffle(choices)
    return {"image": image, "correct": correct, "choices": choices}
