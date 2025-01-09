import pandas as pd

from lib.df import clean_raw_df, load_csv, save_to_csv
from lib.tagization import tag_transactions
from lib.ui import app
from tags.tags import T


if __name__ == "__main__":
    data = {}
    for y in ["2024", "2025"]:
        bourso = f"data/{y}/opbourso.csv"
        sg = f"data/{y}/opsg.csv"
        revolut = f"data/{y}/oprevolut.csv"

        df_raw_bourso = load_csv(bourso)
        df_raw_sg = load_csv(sg)
        df_raw_revolut = load_csv(revolut)
        df_raw = pd.concat(
            [df_raw_bourso, df_raw_sg, df_raw_revolut],
            axis=0,
            ignore_index=False,
            keys=None,
        ).reset_index()  # type: ignore

        df = clean_raw_df(df_raw)
        df.head()
        df_categorized, df_not_categorized = tag_transactions(df)

        # output_not_categorized_file = "operations_bancaires_non_categorisees.csv"
        # output_categorized_file = "operations_bancaires_categorisees.csv"
        # save_to_csv(df_categorized, output_categorized_file)
        # save_to_csv(df_not_categorized, output_not_categorized_file)

        df_year = pd.concat(
            [df_categorized, df_not_categorized], axis=0, ignore_index=False, keys=None
        )
        data[y] = df_year

    budget = {
        T.ALIM.value: 1000,
        T.SHOPPING.value: 400,
        T.LOISIRS.value: 400,
        T.EPARGNE.value: 750,
        T.TRANSPORT.value: 250,
    }

    tags_df = pd.DataFrame(
        {"Name": [member.name for member in T], "Value": [member.value for member in T]}
    )
    app(tags_df=tags_df, year_dfs=data, budget=budget)
