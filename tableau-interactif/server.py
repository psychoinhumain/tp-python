"""Serveur du tableau interactif : API HTTP (/draw, /clear) + WebSocket (/ws)."""
from pathlib import Path

from aiohttp import web, WSMsgType

BASE_DIR = Path(__file__).parent
HOST, PORT = "0.0.0.0", 8080
MAX_BATCH = 100  # formes par requête (forme composée)

# Champs numériques obligatoires pour chaque forme
REQUIRED_FIELDS = {
    "point": ("x", "y"),
    "line": ("x1", "y1", "x2", "y2"),
    "circle": ("x", "y", "radius"),
    "rectangle": ("x", "y", "width", "height"),
    "square": ("x", "y", "cote"),
}

shapes = []        # historique, rejoué à chaque nouveau tableau connecté
clients = set()    # tableaux actuellement connectés


def validate_shape(data):
    """Vérifie le corps JSON et renvoie une forme normalisée (ValueError sinon)."""
    if not isinstance(data, dict):
        raise ValueError("Le corps doit être un objet JSON.")
    shape = data.get("shape")
    if shape not in REQUIRED_FIELDS:
        raise ValueError(f"Forme inconnue : {shape!r}. Valeurs possibles : {', '.join(REQUIRED_FIELDS)}.")
    clean = {"shape": shape}
    for field in REQUIRED_FIELDS[shape]:
        value = data.get(field)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"Le champ '{field}' est requis et doit être un nombre.")
        clean[field] = value
    color = data.get("color", [0, 0, 0])
    if not (isinstance(color, (list, tuple)) and len(color) == 3
            and all(isinstance(c, int) and not isinstance(c, bool) and 0 <= c <= 255 for c in color)):
        raise ValueError("Le champ 'color' doit contenir 3 entiers entre 0 et 255.")
    clean["color"] = list(color)
    return clean


async def broadcast(message):
    """Envoie un message à tous les tableaux connectés."""
    for ws in list(clients):
        try:
            await ws.send_json(message)
        except ConnectionError:
            clients.discard(ws)


async def draw(request):
    """Accepte une forme (objet JSON) ou une forme composée (liste d'objets)."""
    try:
        data = await request.json()
        items = data if isinstance(data, list) else [data]
        if not items:
            raise ValueError("La liste de formes est vide.")
        if len(items) > MAX_BATCH:
            raise ValueError(f"Maximum {MAX_BATCH} formes par requête.")
        new_shapes = []
        for i, item in enumerate(items, 1):
            try:
                new_shapes.append(validate_shape(item))
            except ValueError as err:
                prefix = f"Forme {i} : " if isinstance(data, list) else ""
                raise ValueError(prefix + str(err))
    except ValueError as err:  # inclut JSONDecodeError
        return web.json_response({"status": "error", "message": str(err)}, status=400)
    shapes.extend(new_shapes)
    for shape in new_shapes:
        await broadcast({"type": "shape", "shape": shape})
    return web.json_response({"status": "success", "count": len(new_shapes), "clients": len(clients)})


async def clear(request):
    shapes.clear()
    await broadcast({"type": "clear"})
    return web.json_response({"status": "success"})


async def websocket(request):
    ws = web.WebSocketResponse(heartbeat=20)
    await ws.prepare(request)
    clients.add(ws)
    print(f"Tableau connecté ({len(clients)} au total)")
    await ws.send_json({"type": "init", "shapes": shapes})
    try:
        async for msg in ws:
            if msg.type == WSMsgType.ERROR:
                break
    finally:
        clients.discard(ws)
        print(f"Tableau déconnecté ({len(clients)} restant(s))")
    return ws


async def index(request):
    return web.FileResponse(BASE_DIR / "static" / "index.html")


app = web.Application()
app.add_routes([
    web.get("/", index),
    web.get("/ws", websocket),
    web.post("/draw", draw),
    web.post("/clear", clear),
])

if __name__ == "__main__":
    print(f"Tableau disponible sur http://localhost:{PORT}")
    web.run_app(app, host=HOST, port=PORT, print=None)
