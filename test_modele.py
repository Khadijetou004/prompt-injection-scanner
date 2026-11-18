import pytest
import requests

import modele


class FausseReponse:
    def __init__(self, contenu, statut=200):
        self.contenu = contenu
        self.statut = statut

    def raise_for_status(self):
        if self.statut >= 400:
            raise requests.HTTPError(f"erreur {self.statut}")

    def json(self):
        return {"choices": [{"message": {"content": self.contenu}}]}


def test_demander_envoie_la_requete_attendue(monkeypatch):
    # Aucun appel réseau : requests.post est remplacé par un espion.
    appels = []

    def faux_post(url, json, timeout):
        appels.append((url, json, timeout))
        return FausseReponse("Bonjour !")

    monkeypatch.setattr(modele.requests, "post", faux_post)
    messages = [{"role": "user", "content": "Bonjour"}]
    assert modele.demander(messages) == "Bonjour !"

    url, corps, delai = appels[0]
    assert url == modele.URL
    assert corps == {"model": modele.MODELE, "messages": messages, "temperature": 0,
                     "seed": 42, "max_tokens": modele.MAX_TOKENS}
    assert delai == modele.DELAI


def test_demander_signale_une_erreur_du_serveur(monkeypatch):
    monkeypatch.setattr(modele.requests, "post", lambda *a, **k: FausseReponse("", statut=500))
    with pytest.raises(requests.HTTPError):
        modele.demander([{"role": "user", "content": "Bonjour"}])
