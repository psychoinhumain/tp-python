"""Dog Guesser : devine la race du chien !  Lancement : python main.py"""
import time

import requests
from nicegui import run, ui

import dog_api
import records

ROUNDS = 10

# ---------- thème : couleurs de robe de chien (brun chocolat, caramel), sobre ----------
THEME_HEAD = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700&family=Libre+Caslon+Text:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
<style>
:root {
  --bg: #1d1511;        /* brun chocolat */
  --panel: #2a1f18;
  --panel-2: #372a20;
  --line: #4d3b2d;
  --ivory: #f2e9dd;
  --muted: #bba995;
  --brass: #e0903a;     /* caramel */
  --ok: #8fc79a;
  --ko: #d1695a;
}
body, .q-btn, .q-field__native, .q-field__label, .q-field__control {
  font-family: 'Figtree', system-ui, sans-serif;
}
body {
  color: var(--ivory);
  min-height: 100vh;
  background: radial-gradient(90% 60% at 50% -10%, #3a2a1e 0%, var(--bg) 70%);
  background-attachment: fixed;
}
.dg-serif { font-family: 'Libre Caslon Text', Georgia, serif; }

/* en-tête */
.q-header.dg-header { background: var(--panel) !important; box-shadow: none !important; padding: 0; }
.dg-banner { position: relative; width: 100%; height: 150px; display: flex; gap: 2px; overflow: hidden; border-bottom: 1px solid var(--line); }
.dg-banner .q-img { flex: 1 1 0; min-width: 110px; height: 100%; filter: saturate(.9) brightness(.85); }
.dg-banner::after {
  content: ""; position: absolute; inset: 0; z-index: 1; pointer-events: none;
  background: linear-gradient(90deg, rgba(29,21,17,.8) 0%, rgba(29,21,17,.45) 30%, rgba(29,21,17,.05) 100%),
              linear-gradient(0deg, rgba(29,21,17,.7) 0%, transparent 50%);
}
.dg-banner-text { position: absolute; left: 32px; bottom: 16px; z-index: 2; }
.dg-logo { font-family: 'Libre Caslon Text', Georgia, serif; font-size: 2.1rem; font-weight: 700; color: var(--ivory); line-height: 1.1; text-shadow: 0 2px 12px rgba(0,0,0,.5); }
.dg-logo-sub { color: var(--ivory); opacity: .85; font-size: 1rem; }

/* cartes */
.q-card.dg-card {
  background: var(--panel); color: var(--ivory);
  border: 1px solid var(--line); border-radius: 12px; box-shadow: 0 12px 30px rgba(0,0,0,.25);
}
.dg-title { font-family: 'Libre Caslon Text', Georgia, serif; font-size: 1.9rem; font-weight: 700; line-height: 1.2; text-align: center; }
.dg-sub { color: var(--muted); text-align: center; max-width: 34ch; line-height: 1.45; }
.dg-meta { color: var(--muted); font-size: .95rem; }
.dg-stat { font-weight: 600; font-variant-numeric: tabular-nums; }
.dg-stat.accent { color: var(--brass); }

/* boutons */
.q-btn.dg-btn { border-radius: 8px; font-weight: 600; transition: background-color .15s, border-color .15s, transform .08s; }
.q-btn.dg-btn:active { transform: translateY(1px); }
.q-btn.dg-btn:focus-visible { outline: 2px solid var(--brass); outline-offset: 3px; }
.q-btn.dg-primary { background: var(--brass); color: #26160a; padding: 6px 28px; }
.q-btn.dg-primary:hover { background: #eca455; }
.q-btn.dg-answer {
  background: transparent; color: var(--ivory); border: 1px solid var(--line);
  min-height: 60px; font-size: 1.05rem; font-weight: 500;
}
.q-btn.dg-answer:hover { background: var(--panel-2); border-color: var(--brass); }
.q-btn.dg-answer .q-btn__content { white-space: normal; text-align: center; line-height: 1.2; }
.q-btn.dg-answer.dg-done { pointer-events: none; }
.q-btn.dg-answer.dg-dim { opacity: .45; }
.q-btn.dg-answer.dg-correct { background: var(--ok); border-color: var(--ok); color: #14251a; font-weight: 700; }
.q-btn.dg-answer.dg-wrong   { background: var(--ko); border-color: var(--ko); color: #fff; font-weight: 700; }

/* champ pseudo */
.q-field--outlined .q-field__control:before { border-color: var(--line); }
.q-field--outlined:hover .q-field__control:before { border-color: var(--muted); }
.q-field--focused .q-field__control:after { border-color: var(--brass); }
.q-field--focused .q-field__label { color: var(--brass); }

/* progression : une barre par manche */
.dg-seg { flex: 1; height: 4px; border-radius: 2px; background: var(--line); }
.dg-seg.done { background: var(--brass); }
.dg-seg.now  { background: var(--ivory); }

/* temps restant pour le bonus de rapidité (10 s) */
.dg-timer { width: 100%; height: 3px; background: var(--line); border-radius: 2px; overflow: hidden; }
.dg-timer > div { height: 100%; width: 100%; background: var(--brass); transform-origin: left; animation: dg-drain 10s linear forwards; }
@keyframes dg-drain {
  0%   { transform: scaleX(1); }
  85%  { background: var(--brass); }
  100% { transform: scaleX(0); background: var(--ko); }
}

.dg-photo-wrap { position: relative; width: 100%; height: 22rem; overflow: hidden; border-radius: 8px; border: 1px solid var(--line); background: #150f0b; }
.dg-photo-bg { position: absolute; inset: -20px; background-size: cover; background-position: center; filter: blur(22px) brightness(.55) saturate(1.1); }
.dg-photo-wrap .q-img { position: relative; z-index: 1; width: 100%; height: 100%; background: transparent; }

/* retours */
.dg-fb { width: 100%; padding: 10px 16px; border-radius: 8px; background: var(--panel-2); border-left: 4px solid var(--ok); font-weight: 500; }
.dg-fb.ko { border-left-color: var(--ko); }

/* classement */
.dg-row { padding: 9px 4px; border-bottom: 1px solid var(--line); }
.dg-row:last-child { border-bottom: none; }
.dg-rank { width: 1.6rem; color: var(--muted); font-variant-numeric: tabular-nums; }
.dg-row.podium .dg-rank { color: var(--brass); font-weight: 700; }
.dg-row .score { font-weight: 600; font-variant-numeric: tabular-nums; }
.dg-row.first .score { color: var(--brass); }

/* fin de partie */
.dg-bigscore { font-family: 'Libre Caslon Text', Georgia, serif; font-size: 5rem; font-weight: 700; line-height: 1; color: var(--brass); }
.dg-note { border: 1px solid var(--brass); color: var(--brass); border-radius: 8px; padding: 6px 16px; font-weight: 600; text-align: center; }

@media (prefers-reduced-motion: reduce) {
  .dg-timer > div { animation: none; }
  .q-btn.dg-btn { transition: none; }
}
</style>
"""


def fetch_banner_images(n=6):
    """Quelques photos de chiens au hasard pour le bandeau du haut."""
    response = requests.get(f"{dog_api.BASE_URL}/breeds/image/random/{n}", timeout=10)
    response.raise_for_status()
    return response.json()["message"]


def compute_points(seconds, streak):
    """100 pts + bonus de rapidité (max 100) + bonus de série (max 100)."""
    speed = max(0, 10 - int(seconds)) * 10
    series = min(streak, 4) * 25
    return 100 + speed + series, speed, series


@ui.refreshable
def leaderboard():
    """Classement partagé : refresh() le met à jour chez TOUS les joueurs."""
    top = records.top_scores(10)
    if not top:
        ui.label("Aucun record pour l'instant. Sois le premier à laisser ton nom.").classes("dg-meta")
    with ui.column().classes("w-full gap-0"):
        for i, game in enumerate(top, 1):
            cls = "dg-row w-full items-center no-wrap gap-2"
            if i <= 3:
                cls += " podium"
            if i == 1:
                cls += " first"
            with ui.row().classes(cls):
                ui.label(str(i)).classes("dg-rank")
                ui.label(game["name"]).classes("truncate grow")
                ui.label(str(game["score"])).classes("score")


@ui.page("/")
def index():
    state = {"name": "", "round": 0, "score": 0, "streak": 0, "correct": 0,
             "t0": 0.0, "answered": False}
    ui.colors(primary="#e0903a", positive="#8fc79a", negative="#d1695a")
    ui.add_head_html(THEME_HEAD)

    with ui.header(fixed=False).classes("dg-header"):
        with ui.element("div").classes("dg-banner") as banner:
            with ui.column().classes("dg-banner-text gap-0"):
                ui.label("Dog Guesser").classes("dg-logo")
                ui.label("Devine la race du chien").classes("dg-logo-sub")

    async def load_banner():
        try:
            urls = await run.io_bound(fetch_banner_images)
        except Exception:
            return  # pas d'images : le bandeau reste uni
        with banner:
            for url in urls:
                ui.image(url).props('fit=cover position="50% 25%"')

    with ui.row().classes("w-full justify-center items-start gap-6 p-4"):
        game_card = ui.card().classes("dg-card w-[620px] max-w-full items-center gap-4 p-6")
        with ui.card().classes("dg-card w-80 max-w-full gap-2 p-6"):
            ui.label("Records").classes("dg-serif text-2xl font-bold")
            leaderboard()

    # ---------- écrans ----------
    def show_start():
        game_card.clear()
        with game_card:
            ui.label("Quelle est la race de ce chien ?").classes("dg-title")
            ui.label(f"Le jeu se joue en {ROUNDS} manches.").classes("dg-sub")
            name_input = ui.input("Ton pseudo", value=state["name"]).props(
                "outlined dark maxlength=20").classes("w-64")

            async def start():
                name = name_input.value.strip()
                if not name:
                    ui.notify("Entre un pseudo pour jouer", type="warning")
                    return
                state.update(name=name, round=0, score=0, streak=0, correct=0)
                await next_round()

            name_input.on("keydown.enter", start)
            ui.button("Jouer", on_click=start, color=None).props(
                "unelevated no-caps size=lg").classes("dg-btn dg-primary")

    async def next_round():
        if state["round"] >= ROUNDS:
            finish()
            return
        game_card.clear()
        with game_card:
            ui.spinner("dots", size="xl", color="primary")
            ui.label("Chargement du chien…").classes("dg-meta")
        try:
            question = await run.io_bound(dog_api.get_question)
        except Exception:
            game_card.clear()
            with game_card:
                ui.label("Impossible de joindre l'API des chiens").classes("dg-title")
                ui.button("Réessayer", on_click=next_round, color=None).props(
                    "unelevated no-caps size=lg").classes("dg-btn dg-primary")
            return
        state["round"] += 1
        show_question(question)

    def show_question(q):
        game_card.clear()
        state["answered"] = False
        buttons = {}
        ui_refs = {}
        with game_card:
            with ui.row().classes("w-full items-center justify-between"):
                ui.label(f"Manche {state['round']} sur {ROUNDS}").classes("dg-meta")
                with ui.row().classes("items-center gap-4"):
                    ui_refs["streak"] = ui.label(f"Série ×{state['streak']}").classes("dg-stat accent")
                    ui_refs["streak"].set_visibility(state["streak"] >= 2)
                    ui_refs["score"] = ui.label(f"Score {state['score']}").classes("dg-stat")
            with ui.row().classes("w-full gap-1 no-wrap"):
                for n in range(1, ROUNDS + 1):
                    status = "done" if n < state["round"] else "now" if n == state["round"] else ""
                    ui.element("div").classes(f"dg-seg {status}")
            with ui.element("div").classes("dg-photo-wrap"):
                ui.element("div").classes("dg-photo-bg").style(f"background-image: url('{q['image']}')")
                ui.image(q["image"]).props("fit=contain")
            with ui.element("div").classes("dg-timer"):
                ui_refs["timer"] = ui.element("div")
            with ui.grid(columns=2).classes("w-full gap-3"):
                for choice in q["choices"]:
                    buttons[choice] = ui.button(
                        choice, color=None,
                        on_click=make_handler(q, buttons, choice, ui_refs, feedback_slot)
                    ).props("unelevated no-caps size=lg").classes("dg-btn dg-answer")
            feedback = ui.column().classes("w-full items-center gap-3")
        feedback_slot.append(feedback)
        state["t0"] = time.monotonic()

    feedback_slot = []

    def make_handler(q, buttons, choice, ui_refs, slot):
        async def handler():
            if state["answered"]:
                return
            state["answered"] = True
            seconds = time.monotonic() - state["t0"]
            ok = choice == q["correct"]
            ui_refs["timer"].style("animation-play-state: paused")
            for b in buttons.values():
                b.classes("dg-done dg-dim")
            buttons[q["correct"]].classes("dg-correct", remove="dg-dim")
            if ok:
                points, _speed, _series = compute_points(seconds, state["streak"])
                state["score"] += points
                state["streak"] += 1
                state["correct"] += 1
                text = "Bonne réponse !"
            else:
                buttons[choice].classes("dg-wrong", remove="dg-dim")
                state["streak"] = 0
                text = f"Mauvaise réponse ! C'était : {q['correct']}"
            ui_refs["score"].set_text(f"Score {state['score']}")
            ui_refs["streak"].set_text(f"Série ×{state['streak']}")
            ui_refs["streak"].set_visibility(state["streak"] >= 2)
            feedback = slot[-1]
            with feedback:
                ui.label(text).classes("dg-fb" + ("" if ok else " ko"))
                label = "Voir mon score" if state["round"] >= ROUNDS else "Suivant"
                ui.button(label, on_click=next_round, color=None).props(
                    "unelevated no-caps size=lg").classes("dg-btn dg-primary")
        return handler

    def finish():
        result = records.add_score(state["name"], state["score"])
        leaderboard.refresh()  # mise à jour en direct chez tous les joueurs
        game_card.clear()
        with game_card:
            ui.label("Partie terminée").classes("dg-title")
            ui.label(f"{state['score']}").classes("dg-bigscore")
            ui.label(f"{state['correct']}/{ROUNDS} bonnes réponses").classes("dg-meta")
            if result["absolute_record"]:
                ui.label("Nouveau record absolu").classes("dg-note text-lg")
            elif result["personal_best"]:
                ui.label("Nouveau record personnel").classes("dg-note")
            if result["rank"]:
                ui.label(f"Tu es n°{result['rank']} au classement").classes("text-lg font-semibold")
            ui.button("Rejouer", on_click=lambda: next_round_new(), color=None).props(
                "unelevated no-caps size=lg").classes("dg-btn dg-primary")

    async def next_round_new():
        state.update(round=0, score=0, streak=0, correct=0)
        await next_round()

    show_start()
    ui.timer(0.1, load_banner, once=True)


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="Dog Guesser", favicon="🐶")
