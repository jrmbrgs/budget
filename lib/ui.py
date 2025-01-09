from datetime import datetime
from typing import Any, Dict
import streamlit as st
import plotly.express as px

import pandas as pd

from tags.tags import T


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


def display_budget(df: pd.DataFrame, budget: Dict[str, Any]) -> None:
    df["month"] = df["dateOp"].dt.month
    df["year"] = df["dateOp"].dt.year
    df["year-month"] = df["dateOp"].dt.strftime("%Y-%m")
    df["amount"] = df["amount"].abs()
    months_options = df["year-month"].sort_values().unique()
    month_selection = st.segmented_control(
        "Year", months_options, selection_mode="single"
    )
    month_selection = months_options[-1] if not month_selection else month_selection

    current_month_df = df[df["year-month"] == month_selection]
    cat_month_sum = (
        current_month_df.groupby(["month", "cat"]).agg({"amount": "sum"}).reset_index()
    )
    cat_sum = cat_month_sum.groupby(["cat"]).agg({"amount": "sum"}).reset_index()

    st.header("Budget par Cat")
    columns = st.columns(5)
    for idx, cat_budget in enumerate(budget.items()):
        cat, budget_amount = cat_budget
        with columns[idx % len(columns)]:
            current_month_cat_df = cat_sum[cat_sum["cat"] == cat]
            if len(current_month_cat_df):
                spent_amount = current_month_cat_df["amount"].iloc[0].round()
            else:
                spent_amount = 0
            progress = round((100 / budget_amount) * spent_amount, 2)
            st.subheader(f"{cat}")
            st.write(f"{spent_amount}/{budget_amount} ({progress}%)")

            if progress >= 100:
                st.progress(100, text="Budget")
            else:
                st.progress(((progress) / 100), text="Budget")
            remaining_amount = spent_amount - budget_amount
            while remaining_amount > 0:
                progress = round((100 / budget_amount) * remaining_amount, 2)
                st.write(f"{remaining_amount}/{budget_amount} ({progress}%)")
                if progress >= 100:
                    st.progress(100, text="Hors budget")
                else:
                    st.progress(((progress) / 100), text="Hors budget")
                remaining_amount = remaining_amount - budget_amount

    st.divider()
    st.header("Répartition des dépenses du mois")
    monthly_sum = cat_sum.agg({"amount": "sum"})

    cats_options = current_month_df["cat"].sort_values().unique()
    selected_cats = []
    toggle_state = {cat: False for cat in cats_options}

    toggle_all = st.toggle(f"ALL {monthly_sum['amount'].round()}", value=True)
    if toggle_all:
        toggle_state = {cat: True for cat in cats_options}
    else:
        toggle_state = {cat: False for cat in cats_options}

    columns = st.columns(6)
    for idx, cat in enumerate(cats_options):
        with columns[idx % len(columns)]:
            avg = cat_sum[cat_sum["cat"] == cat]["amount"].iloc[0].round()
            toggle_state[cat] = st.toggle(
                f"{cat} ({avg}€)", value=toggle_state[cat], key=f"{cat}"
            )
            if toggle_state[cat]:
                selected_cats.append(cat)

    filtered_data = current_month_df[current_month_df["cat"].isin(selected_cats)]

    col1, col2 = st.columns(2)
    # CATEGORIES
    with col1:
        st.markdown("**Dépenses Mensuelles par :blue[Catégorie]**")
        monthly_expenses = (
            filtered_data.groupby(["month", "cat"]).agg({"amount": "sum"}).reset_index()
        )
        fig = px.pie(
            monthly_expenses,
            values="amount",
            names="cat",
        )
        st.plotly_chart(fig)
    # TAGS
    with col2:
        st.markdown("**Dépenses Mensuelles par :blue[Tags]**")

        monthly_expenses = (
            filtered_data.groupby(["month", "tags"])
            .agg({"amount": "sum"})
            .reset_index()
        )
        fig = px.pie(
            monthly_expenses,
            values="amount",
            names="tags",
        )
        st.plotly_chart(fig)

    st.divider()
    st.header("Transactions du mois")
    st.data_editor(filtered_data)


def app(
    tags_df: pd.DataFrame, year_dfs: Dict[str, pd.DataFrame], budget: Dict[str, Any]
):
    st.set_page_config(layout="wide")

    def page_yearly():
        st.title("Annual Review")
        tab2025, tab2024 = st.tabs(sorted(year_dfs.keys(), reverse=True))
        with tab2025:
            y = "2025"
            df = year_dfs[y]
            display_year(y=y, df=df)

        with tab2024:
            y = "2024"
            df = year_dfs[y]
            display_year(y=y, df=df)

    def page_budget():
        st.title("Monthly budget")
        y = "2025"
        df = year_dfs[y]
        df = pd.concat(
            [year_dfs["2024"], year_dfs["2025"]], axis=0, ignore_index=False, keys=None
        )

        display_budget(df=df, budget=budget)

    def page_config_cattags():
        st.title("Config")
        st.data_editor(tags_df)

        def save_dataframe(df):
            df.to_csv("modified_dataframe.csv", index=False)
            st.success("DataFrame sauvegardée localement sous 'modified_dataframe.csv'")

        if st.button("Sauvegarder"):
            save_dataframe(tags_df)

    def page_config_transac():
        st.title("Config")
        df = pd.concat(
            [year_dfs["2024"], year_dfs["2025"]], axis=0, ignore_index=False, keys=None
        )
        df_non_categorized = df[df["cat"] == "NOCAT"]
        st.data_editor(df_non_categorized)

    pages = {
        "Budget": [
            st.Page(page_budget, title="Monthly budget", icon=":material/favorite:"),
        ],
        "Annual review": [
            st.Page(page_yearly, title="Yearly Analisis"),
        ],
        "Config": [
            st.Page(page_config_cattags, title="Categories & Tags"),
            st.Page(page_config_transac, title="Transaction à catégoriser"),
        ],
    }

    pg = st.navigation(pages)
    pg.run()
