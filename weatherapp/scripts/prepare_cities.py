import pandas as pd
import streamlit as st
from rho_store import RhoClient

from weatherapp.scripts.geocode_service import GeocodeService

rho_client = RhoClient(api_key=st.secrets.get("rho_api_key"))
geo_client = GeocodeService(google_api_key=st.secrets.get("google_api_key"))


def append_lat_long() -> None:
    table = rho_client.get_table("examples/weather/cities")
    data = table.get_df()

    lat_long_data = []

    for index, row in data.iterrows():
        city, country = row["city"], row["country"]
        search_string = f"{city}, {country}"
        try:
            lat, lon = geo_client.get_lat_long(search_string)
        except Exception:
            # failed to geocode string
            lat, lon = None, None

        result = {
            "index": index,
            "latitude": lat,
            "longitude": lon,
        }
        lat_long_data.append(result)

    lat_long_df = pd.DataFrame(lat_long_data)
    lat_long_df.set_index("index", inplace=True)
    data.update(lat_long_df)
    table.new_version(
        data=pd.DataFrame(lat_long_data)
    )


if __name__ == "__main__":
    append_lat_long()
