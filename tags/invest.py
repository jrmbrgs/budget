from typing import List, Tuple

from tags.tags import T

ope_invest: List[Tuple[str, T, List[T]]] = [
    ("PRLV SEPA GENERALI VIE", T.EPARGNE, [T.INVEST]),
    ("VIR Epargne programmee", T.EPARGNE, []),
    ("VIR Epargne Eliott", T.EPARGNE, [T.KIDS]),
    ("VIR Epargne Simon", T.EPARGNE, [T.KIDS]),
    ("VIR Epargne J", T.EPARGNE, [T.SECURE]),
    ("VIR Cantines Enfants", T.EPARGNE, [T.SECURE]),
    ("VIR Vacances Ete", T.EPARGNE, [T.VAC]),
    ("VIR Entretien voiture", T.EPARGNE, [T.SECURE]),
    ("VIR Orthodontie Eliott", T.EPARGNE, [T.SECURE]),
    ("LW-BRICKS.CO", T.EPARGNE, [T.INVEST]),
]
