import json
from pathlib import Path

from detecteurs import verifier_longueur

CHAMPS = ["id", "categorie", "type", "description", "question", "document_piege", "detection"]
CATEGORIES = {"LLM01", "LLM02", "LLM05", "LLM07"}
TYPES = {"directe", "indirecte"}
METHODES = {"canari", "marqueur", "empreinte"}
METHODES_AVEC_VALEUR = {"marqueur", "empreinte"}


def _verifier_attaque(attaque):
    """Lève une ValueError si l'attaque ne respecte pas le format du corpus."""
    for champ in CHAMPS:
        if champ not in attaque:
            raise ValueError(f"champ manquant : {champ}")

    nom = attaque["id"]
    for champ in ("id", "description", "question"):
        if not isinstance(attaque[champ], str):
            raise ValueError(f"{nom} : le champ {champ} doit être un texte")
    if attaque["categorie"] not in CATEGORIES:
        raise ValueError(f"{nom} : catégorie hors périmètre : {attaque['categorie']}")
    if attaque["type"] not in TYPES:
        raise ValueError(f"{nom} : type inconnu : {attaque['type']}")

    piege = attaque["document_piege"]
    if attaque["type"] == "directe" and piege is not None:
        raise ValueError(f"{nom} : une attaque directe n'a pas de document piégé")
    if attaque["type"] == "indirecte":
        if not isinstance(piege, dict) or "nom" not in piege or "contenu" not in piege:
            raise ValueError(f"{nom} : document piégé absent ou incomplet")
        if not isinstance(piege["nom"], str) or not isinstance(piege["contenu"], str):
            raise ValueError(f"{nom} : le nom et le contenu du piège doivent être des textes")

    detection = attaque["detection"]
    if not isinstance(detection, dict):
        raise ValueError(f"{nom} : detection doit être un objet")
    methode = detection.get("methode")
    if methode not in METHODES:
        raise ValueError(f"{nom} : méthode de détection inconnue : {methode}")
    if methode in METHODES_AVEC_VALEUR:
        valeur = detection.get("valeur")
        if not isinstance(valeur, str):
            raise ValueError(f"{nom} : la méthode {methode} demande une valeur texte")
        verifier_longueur(valeur, f"{nom} : la valeur de {methode}")


def charger_attaques(chemin):
    """Lit le corpus JSON, vérifie chaque attaque et renvoie la liste."""
    attaques = json.loads(Path(chemin).read_text(encoding="utf-8"))
    deja_vus = set()
    for attaque in attaques:
        _verifier_attaque(attaque)
        if attaque["id"] in deja_vus:
            raise ValueError(f"identifiant en double : {attaque['id']}")
        deja_vus.add(attaque["id"])
    return attaques
