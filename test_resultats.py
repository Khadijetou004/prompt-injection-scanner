import json
import re
from pathlib import Path

import pytest

from corpus import charger_attaques
from scanner import juger, taux_de_reussite, taux_par_attaque, taux_par_categorie

DOSSIER = Path(__file__).parent
SCANS = sorted((DOSSIER / "resultats").glob("*.json"))
ATTAQUES = {a["id"]: a for a in charger_attaques(DOSSIER / "attaques.json")}


def charger(chemin):
    return json.loads(chemin.read_text(encoding="utf-8"))


def test_il_y_a_des_scans_publies():
    assert SCANS


@pytest.mark.parametrize("chemin", SCANS, ids=lambda c: c.name)
def test_les_taux_enregistres_correspondent_aux_resultats(chemin):
    scan = charger(chemin)
    resultats = scan["resultats"]
    assert scan["taux_global"] == taux_de_reussite(resultats)
    assert scan["taux_par_categorie"] == taux_par_categorie(resultats)
    assert scan["taux_par_attaque"] == taux_par_attaque(resultats)
    assert len(resultats) == scan["repetitions"] * len(ATTAQUES)


@pytest.mark.parametrize("chemin", SCANS, ids=lambda c: c.name)
def test_chaque_reponse_publiee_se_rejuge_a_l_identique(chemin):
    # Le canari est enregistré avec chaque réponse : le jugement doit être reproductible.
    for r in charger(chemin)["resultats"]:
        assert juger(r["reponse"], ATTAQUES[r["id"]], r["canari"]) == r["reussie"], r["id"]


def test_chaque_scan_cite_dans_le_readme_existe():
    readme = (DOSSIER / "README.md").read_text(encoding="utf-8")
    cites = set(re.findall(r"\(resultats/([^)]+\.json)\)", readme))
    assert cites
    assert cites <= {c.name for c in SCANS}
