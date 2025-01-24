import streamlit as st

from weatherapp.src.cities import get_cities_names

st.title("Weather data")

cities_names = get_cities_names()
option = st.selectbox("Select a city", cities_names)
st.divider()
