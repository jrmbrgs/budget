import streamlit as st
import plotly.express as px

import pandas as pd


def display_year(y: str, df: pd.DataFrame) -> None:
    df["month"] = df["dateOp"].dt.month
    df["year"] = df["dateOp"].dt.year
    df["amount"] = df["amount"].abs()

    nb_month = len(df["month"].sort_values().unique())

    cat_month_sum = df.groupby(["month", "cat"]).agg({"amount": "sum"}).reset_index()
    cat_sum = cat_month_sum.groupby(["cat"]).agg({"amount": "sum"}).reset_index()
    cat_sum["amount"] = cat_sum["amount"] / nb_month
    monthly_sum = cat_sum.agg({"amount": "sum"})
    cats_options = df["cat"].sort_values().unique()
    selected_cats = []
    toggle_state = {cat: False for cat in cats_options}

    toggle_all = st.toggle(f"ALL {monthly_sum['amount'].round()}", value=True)
    if toggle_all:
        toggle_state = {cat: True for cat in cats_options}
    else:
        toggle_state = {cat: False for cat in cats_options}

    col1, col2, col3, col4, col5 = st.columns(5)
    columns = [col1, col2, col3, col4, col5]
    for idx, cat in enumerate(cats_options):
        with columns[idx % 5]:
            avg = cat_sum[cat_sum["cat"] == cat]["amount"].iloc[0].round()
            toggle_state[cat] = st.toggle(
                f"{cat} ({avg}€)", value=toggle_state[cat], key=f"{y}{cat}"
            )
            if toggle_state[cat]:
                selected_cats.append(cat)

    filtered_data = df[df["cat"].isin(selected_cats)]

    st.divider()
    monthly_expenses = (
        filtered_data.groupby(["month", "cat"]).agg({"amount": "sum"}).reset_index()
    )

    col1, col2 = st.columns(2)
    # CATEGORIES
    with col1:
        st.markdown("**Dépenses Mensuelles par :blue[Catégorie]**")
        # AVG
        cat_sum = (
            filtered_data.groupby(["month", "cat"]).agg({"amount": "sum"}).reset_index()
        )
        cat_sum_by_cat = cat_sum.groupby(["cat"]).agg({"amount": "sum"}).reset_index()
        cat_sum_by_cat["avg"] = cat_sum_by_cat["amount"] / nb_month
        cat_avg_pivoted = cat_sum_by_cat.set_index("cat").transpose()
        st.dataframe(cat_avg_pivoted)
        category_order = (
            monthly_expenses.groupby("cat")["amount"]
            .sum()
            .sort_values(ascending=False)
            .index.tolist()
        )

        fig = px.bar(
            monthly_expenses,
            x="month",
            y="amount",
            color="cat",
            labels={
                "month": "Mois",
                "amount": "Montant (€)",
                "category": "Catégorie",
            },
            barmode="stack",
            category_orders={"cat": category_order},
        )

        fig.update_layout(autosize=True, width=None, height=600)
        st.plotly_chart(fig, use_container_width=True)

    # TAGS
    with col2:
        st.markdown("**Dépenses Mensuelles par :blue[Tags]**")
        # AVG
        tag_sum = (
            filtered_data.groupby(["month", "tags"])
            .agg({"amount": "sum"})
            .reset_index()
        )
        tag_sum_by_tag = tag_sum.groupby(["tags"]).agg({"amount": "sum"}).reset_index()
        tag_sum_by_tag["avg"] = tag_sum_by_tag["amount"] / nb_month
        tag_avg_pivoted = tag_sum_by_tag.set_index("tags").transpose()
        st.dataframe(tag_avg_pivoted)

        monthly_expenses = (
            filtered_data.groupby(["month", "tags"])
            .agg({"amount": "sum"})
            .reset_index()
        )
        category_order = (
            monthly_expenses.groupby("tags")["amount"]
            .sum()
            .sort_values(ascending=False)
            .index.tolist()
        )

        fig = px.bar(
            monthly_expenses,
            x="month",
            y="amount",
            color="tags",
            labels={"month": "Mois", "amount": "Montant (€)", "tags": "Tags"},
            barmode="stack",
            category_orders={"tags": category_order},
        )

        fig.update_layout(autosize=True, width=None, height=600)
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.header("Transactions")
    st.data_editor(filtered_data)
