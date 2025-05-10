import pandas as pd


def load_csv(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path, delimiter=";") # type: ignore


def save_to_csv(df: pd.DataFrame, output_file_path: str)-> None:
    df.to_csv(output_file_path, index=False, sep=";")


def clean_raw_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop(
        columns=[
            "dateVal",
            "supplierFound",
            "accountbalance",
            "accountLabel",
            "accountNum",
            "comment",
        ]
    )
    df["dateOp"] = pd.to_datetime(df["dateOp"])
    df["amount"] = df["amount"].str.replace(",", ".").replace(" ", "")
    df["amount"] = df["amount"].str.replace(" ", "")
    df["amount"] = df["amount"].astype(float)
    return df
