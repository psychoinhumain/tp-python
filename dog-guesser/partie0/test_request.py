from io import BytesIO

import requests
from PIL import Image

BREEDS_URL = "https://dog.ceo/api/breeds/list/all"
RANDOM_URL = "https://dog.ceo/api/breeds/image/random"


def count_num_breeds():
    """Renvoie le nombre de races (clés principales) de l'API dog.ceo."""
    try:
        response = requests.get(BREEDS_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"Erreur réseau : {e}")
        return None
    if data.get("status") != "success":
        print("L'API a renvoyé une erreur.")
        return None
    return len(data["message"])


def display_random_dog():
    """Récupère une image de chien aléatoire et l'affiche."""
    try:
        response = requests.get(RANDOM_URL, timeout=10)
        response.raise_for_status()
        image_url = response.json()["message"]
        image_response = requests.get(image_url, timeout=10)
        image_response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur réseau : {e}")
        return
    Image.open(BytesIO(image_response.content)).show()
    print(f"Image affichée : {image_url}")


if __name__ == "__main__":
    print(f"Nombre de races : {count_num_breeds()}")
    display_random_dog()
