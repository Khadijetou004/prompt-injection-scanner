import requests

URL = "http://localhost:11434/v1/chat/completions"
MODELE = "llama3.2:3b"   # remplace par le modèle que tu as téléchargé


def demander(messages: list[dict]) -> str:
    reponse = requests.post(
        URL,
        json={
            "model": MODELE,
            "messages": messages,
            "temperature": 0,
            "seed": 42,
        },
        timeout=120,
    )
    reponse.raise_for_status()
    return reponse.json()["choices"][0]["message"]["content"]
