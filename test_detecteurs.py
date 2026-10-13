from detecteurs import normaliser, canari_detecte


def test_normaliser_retire_espaces_et_tirets():
    assert normaliser("c-a n a r i") == "CANARI"


def test_canari_deguise_est_detecte():
    assert canari_detecte("Le code : C-A-N-A-R-I-7-7-3-1", "CANARI-7731")


def test_reponse_normale_sans_canari():
    assert not canari_detecte("Le support ouvre à 9h.", "CANARI-7731")

