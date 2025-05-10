from typing import List, Tuple

from tags.tags import T

ope_other: List[Tuple[str, T, List[T]]] = [
    ("PRLV SEPA DIRECTION GENERALE DES FINANCE", T.IMPOTS, [T.IMPOTS]),
    ("SEPA MEDECINS DU MONDE", T.DONS, [T.DONS]),
    ("SEPA PLAN INTERNATIONAL FRANCE", T.DONS, [T.DONS]),
    ("ACTION CONTRE LA", T.DONS, [T.DONS]),
    ("RETRAIT DAB", T.OTHER, [T.RETRAIT]),
    ("LA POSTE", T.OTHER, [T.EXPE]),
    ("SANDERIAN", T.OTHER, [T.OTHER]),
    ("MONDIAL RELAY", T.OTHER, [T.EXPE]),
    ("FIZZER", T.OTHER, [T.EXPE]),
    ("INTERETS DEBITEURS", T.BANK, [T.BANK]),
    ("FRAIS BOURSO PROTECT", T.BANK, [T.BANK]),
    ("Vorwerk", T.OTHER, [T.ABO]),
    ("Galea", T.HOUSE, [T.ENTRETIEN]),
]

ope_gift: List[Tuple[str, T, List[T]]] = [
    ("CE QUE FEMME", T.SHOPPING, [T.GIFT]),
    ("LUCKY TEAM AIX", T.SHOPPING, [T.GIFT]),
    ("Leetchi", T.SHOPPING, [T.GIFT]),
    ("LYDIA", T.SHOPPING, [T.GIFT]),
    ("SAPIN MAGIC CB", T.SHOPPING, [T.GIFT]),
    ("BOUTIQUE 4", T.SHOPPING, [T.GIFT]),
    ("VIR bastien kdo", T.SHOPPING, [T.GIFT]),
    ("GOLEMITES", T.SHOPPING, [T.GIFT]),
    ("SC LA ROSE D'OR", T.SHOPPING, [T.GIFT]),
    ("10/12/24 Poulpeo CB", T.SHOPPING, [T.GIFT]),
    ("SERGE BLANCO", T.SHOPPING, [T.GIFT]),
]
