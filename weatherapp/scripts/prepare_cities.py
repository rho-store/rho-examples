import pandas as pd
import streamlit as st
from rho_store import RhoClient

from weatherapp.scripts.geocode_service import GeocodeService

rho_client = RhoClient(api_key=st.secrets.get("rho_api_key"))
geo_client = GeocodeService(google_api_key=st.secrets.get("google_api_key"))


def append_lat_long() -> None:
    table_path = "examples/weather/cities"
    table = rho_client.get_table(table_path)
    data = table.get_df()

    # collect coordinates for each city
    coordinates_df = []
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
        coordinates_df.append(result)
        if (index + 1) % 10 == 0:
            print(f"Processed {index + 1} of {len(data)} rows")

    # merge coordinates into original dataframe
    lat_long_df = pd.DataFrame(coordinates_df)
    lat_long_df.set_index("index", inplace=True)
    data.update(lat_long_df)

    # store updated dataframe as new version
    table.new_version(data=data)


if __name__ == "__main__":
    append_lat_long()
