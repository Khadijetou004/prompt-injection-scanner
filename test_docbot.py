from detecteurs import LONGUEUR_MIN_CANARI, canari_detecte, normaliser
from docbot import charger_documents, construire_messages, generer_canari, rechercher


# --- generer_canari ---

def test_generer_canari_commence_par_le_prefixe():
    canari = generer_canari()
    assert canari.startswith("CANARI-")
    assert len(canari) == len("CANARI-") + 8


def test_generer_canari_different_a_chaque_appel():
    assert generer_canari() != generer_canari()


def test_generer_canari_accepte_par_le_detecteur():
    canari = generer_canari()
    assert len(normaliser(canari)) >= LONGUEUR_MIN_CANARI
    assert canari_detecte(f"Voici le code : {canari}", canari)


# --- charger_documents ---

def test_charger_documents_lit_seulement_les_txt(tmp_path):
    (tmp_path / "horaires.txt").write_text("Ouvert du lundi au vendredi.", encoding="utf-8")
    (tmp_path / "notes.md").write_text("À ignorer.", encoding="utf-8")
    documents = charger_documents(tmp_path)
    assert documents == {"horaires.txt": "Ouvert du lundi au vendredi."}


# --- rechercher ---

DOCUMENTS = {
    "horaires.txt": "Le support est ouvert du lundi au vendredi. Horaires d'ouverture du support.",
    "factures.txt": "Les factures arrivent par courriel. Paiement par carte ou virement.",
    "motdepasse.txt": "Pour changer votre mot de passe, cliquez sur le lien envoyé par courriel.",
}


def test_rechercher_met_le_bon_document_en_premier():
    resultats = rechercher("Quand le support est ouvert le samedi ?", DOCUMENTS)
    assert resultats[0] == "horaires.txt"


def test_rechercher_renvoie_au_plus_k_documents():
    # chacun des 3 documents a au moins un mot en commun avec la question
    resultats = rechercher("support courriel paiement", DOCUMENTS, k=2)
    assert len(resultats) == 2


def test_rechercher_sans_rapport_renvoie_liste_vide():
    assert rechercher("recette crêpes bretonnes", DOCUMENTS) == []


# --- construire_messages ---

QUESTION = "Comment payer ma facture ?"
EXTRAITS = ["Les factures arrivent par courriel.", "Paiement par carte ou virement."]
CANARI = "CANARI-AB12CD34"


def test_messages_canari_dans_system():
    messages = construire_messages(QUESTION, EXTRAITS, CANARI)
    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert CANARI in messages[0]["content"]


def test_messages_canari_absent_de_user():
    messages = construire_messages(QUESTION, EXTRAITS, CANARI)
    assert messages[1]["role"] == "user"
    assert not canari_detecte(messages[1]["content"], CANARI)


def test_messages_question_et_extraits_dans_user():
    messages = construire_messages(QUESTION, EXTRAITS, CANARI)
    contenu = messages[1]["content"]
    assert QUESTION in contenu
    for extrait in EXTRAITS:
        assert extrait in contenu
