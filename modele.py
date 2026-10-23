import requests

URL = "http://localhost:11434/v1/chat/completions"
MODELE = "llama3.2:3b"   # remplace par le modèle que tu as téléchargé
# Plafond de longueur des réponses. Sans lui, un modèle qui part en boucle
# génère jusqu'au délai d'attente et fait planter le scan. La plus longue
# réponse du scan de référence fait environ 800 caractères, bien en dessous.
MAX_TOKENS = 1024
# Délai d'attente par requête, en secondes. Sur processeur, un prompt long
# (celui du spotlighting par exemple) peut dépasser 120 secondes.
DELAI = 300


def demander(messages: list[dict]) -> str:
    reponse = requests.post(
        URL,
        json={
            "model": MODELE,
            "messages": messages,
            "temperature": 0,
            "seed": 42,
            "max_tokens": MAX_TOKENS,
        },
        timeout=DELAI,
    )
    reponse.raise_for_status()
    return reponse.json()["choices"][0]["message"]["content"]
