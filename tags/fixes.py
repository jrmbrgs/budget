from typing import List, Tuple

from tags.tags import T

ope_fixes: List[Tuple[str, T, List[T]]] = [
    ("Autoroutes du Sud de la France", T.TRANSPORT, [T.ROUTE]),
    ("BOUYGUES", T.ABO, [T.FORFAIT]),
    ("SFR", T.ABO, [T.FORFAIT]),
    ("Orange", T.ABO, [T.FORFAIT]),
    ("PRIXTEL", T.ABO, [T.FORFAIT]),
    ("EDF", T.HOUSE, [T.ENER]),
    ("TOTALENERGIES", T.HOUSE, [T.ENER]),
    ("LUKO", T.HOUSE, [T.ASS]),
    ("MACIF", T.HOUSE, [T.ASS]),
    ("SDC LE FRANCE", T.HOUSE, [T.COPRO]),
    ("ECHEANCE PRET", T.HOUSE, [T.CREDIT]),
    ("VIR SEPA Bourgeais Marie-JosA", T.HOUSE, [T.CREDIT]),
    ("CPTE DE:D.G.F.I.P", T.HOUSE, [T.IMPOTS]),
    ("CHEQUE", T.CHEQUE, [T.CHEQUE]),
    ("COMPTE DEBITEUR NON AUTORISE", T.BANK, []),
    ("MINIMUM FORFAITAIRE", T.BANK, []),
    ("FRAIS VIR INSTANTANE", T.BANK, []),
    ("Netflix", T.ABO, [T.VOD]),
    ("Spotify", T.ABO, [T.MUSIC]),
    ("APPLE.COM/BILL", T.ABO, [T.CLOUD]),
    ("APPLE.COM BILL", T.ABO, [T.CLOUD]),
]
