from typing import Any, Dict
import streamlit as st
import plotly.express as px

import pandas as pd


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
