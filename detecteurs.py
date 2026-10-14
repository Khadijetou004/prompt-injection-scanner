import re
LONGUEUR_MIN_CANARI = 8

def normaliser(texte: str) -> str:
    """Met en majuscules et garde seulement les lettres A-Z et les chiffres."""
    return re.sub(r"[^A-Z0-9]", "", texte.upper())


def canari_detecte(reponse: str, canari: str) -> bool:
    """Vrai si le canari apparaît dans la réponse, même déguisé ou à l'envers."""
    r = normaliser(reponse)
    c = normaliser(canari)
    if len(c) < LONGUEUR_MIN_CANARI:
        raise ValueError(f"le canari doit contenir au moins {LONGUEUR_MIN_CANARI} lettres ou chiffres")
    return c in r or c[::-1] in r
