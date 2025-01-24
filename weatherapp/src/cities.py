import streamlit as st
from rho_store import RhoClient
import pandas as pd


rho_client = RhoClient(api_key=st.secrets.get("rho_api_key"))


@st.cache_data
def get_cities_df() -> pd.DataFrame:
    cities_table = rho_client.get_table("examples/weather/cities")
    return cities_table.get_df()


@st.cache_data
def get_cities_names() -> list[str]:
    cities_df = get_cities_df()
    return sorted(cities_df["city"].to_list())
