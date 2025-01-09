import hmac
import io
from typing import Any, Dict
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

import streamlit as st

import pandas as pd

from lib.df import clean_raw_df
from lib.tagization import tag_transactions
from ui.budget import display_budget
from ui.yearly import display_year

from google.oauth2.service_account import Credentials


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]


def load_credentials():
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=SCOPES
    )
    return creds


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


@st.cache_data(ttl=60)
def read_csv_from_google_drive(file_id: str) -> pd.DataFrame:
    creds = load_credentials()
    drive_service = build("drive", "v3", credentials=creds)
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()

    fh.seek(0)
    df = pd.read_csv(fh, delimiter=";")
    df.head()
    return df


FILES = {
    "2024": [
        "1XheEKlBvaMdeSdZ749fVmG0FBcDFq6h2",
        "1Gl0nXhKxYPzcQsocUTv9Qg3heuq4gy6H",
        "15jmvooCIRqQq7w6EcNxPzodkihgrzQEX",
    ],
    "2025": [
        "1STa8pGeXP-2DWcMXq9xsa4nbPhSc9R-9",
        "1SPXand0JjXyZJkiChJv-T3OA3fLiN-lG",
        "1-F52HtMpyA2pi7PTS0l7zeKHBBWNRXIu",
    ],
}


def load_dfs() -> Dict[str, pd.DataFrame]:
    dfs: Dict[str, pd.DataFrame] = {}
    for y in ["2024", "2025"]:
        year_dfs = []
        for f_id in FILES[y]:
            print(f"loading {f_id}")
            df = read_csv_from_google_drive(file_id=f_id)
            year_dfs.append(df)
        year_df_raw = pd.concat(year_dfs, axis=0, keys=None).reset_index()  # type: ignore
        year_df_clean = clean_raw_df(year_df_raw)
        df_categorized, df_not_categorized = tag_transactions(year_df_clean)
        dfs[y] = pd.concat([df_categorized, df_not_categorized], axis=0, keys=None)
    return dfs


def app(
    tags_df: pd.DataFrame,
    budget: Dict[str, Any],
):
    if not check_password():
        st.stop()
    st.set_page_config(layout="wide")

    year_dfs = load_dfs()

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
