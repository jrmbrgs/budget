import itertools
from typing import Any, Dict, List, Tuple
import pandas as pd
from tags.tags import T
from tags import fixes, life, vacances, todrop, invest, other

ALL_TAGS = list(
    itertools.chain(
        life.ope_course,
        life.ope_kids,
        life.ope_sante,
        life.ope_shopping,
        life.ope_sorties,
        life.ope_transport,
        life.ope_bienetre,
        vacances.ope_vacances,
        other.ope_other,
        other.ope_gift,
        invest.ope_invest,
        fixes.ope_fixes,
    )
)

CATEGORIES = {
    "TO DROP": {
        "Virements": ["VIR INST", "VIR SEPA", "Virement"],
    },
}


def cat_transaction(row: Dict[str, Any]) -> str:
    for keyword, cat, tags in ALL_TAGS:
        if keyword.upper() in row["label"].upper():
            return cat.value
    return "NOCAT"


def tag_transaction(row: Dict[str, Any]) -> List[str]:
    for keyword, cat, tags in ALL_TAGS:
        if keyword.upper() in row["label"].upper():
            return ";".join([tag.value for tag in tags])
    return ""


def clean_transaction(row: Dict[str, Any]) -> int:
    if row["amount"] > 0:
        return 1
    for keyword, tags in todrop.ope_todrop:
        if keyword.upper() in row["label"].upper() and row["cat"] == "NOCAT":
            return 1
        if row["category"] == "Autorisation paiement / retrait en cours":
            return 1
    return 0


def tag_transactions(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df["cat"] = df.apply(cat_transaction, axis=1)
    df["tags"] = df.apply(tag_transaction, axis=1)
    df["todrop"] = df.apply(clean_transaction, axis=1)
    df_clean = df[df["todrop"] == 0]
    df_clean = df_clean.drop(columns=["todrop"])
    print(df_clean.head())

    #
    df_categorized = df_clean[df_clean["tags"].apply(lambda x: len(x) > 0)]
    df_non_categorized = df_clean[df_clean["tags"].apply(lambda x: len(x) == 0)]
    no_tag_value = T.NOTAG.value
    df_non_categorized.loc[:, "tags"] = df.apply(lambda x: no_tag_value, axis=1)

    return (df_categorized, df_non_categorized)
