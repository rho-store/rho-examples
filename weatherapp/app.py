import calendar
import datetime
import logging

import pandas as pd
import plost
import streamlit as st
from rho_store import RhoClient

from weatherapp.src.temperature import analyze_temperature
from weatherapp.src.weather import get_daily_temperature_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


rho_client = RhoClient(api_key=st.secrets.get("rho_api_key"))


@st.cache_data
def get_cities_df_cached() -> pd.DataFrame:
    """ Cached function to get cities from Rho """
    table_path = "examples/weather/cities"
    cities_table = rho_client.get_table(table_path)
    return cities_table.get_df()


@st.cache_data
def get_temperature_data_cached(
        latitude: float,
        longitude: float,
        start_date: datetime.date = None,
        end_date: datetime.date = None
) -> pd.DataFrame:
    """ Cached function to get temperature data """
    return get_daily_temperature_data(
        latitude=latitude,
        longitude=longitude,
        start_date=start_date,
        end_date=end_date
    )


def render_description() -> None:
    """Render app description with external links."""
    st.html("""
    <div>
    <p>This app is built using <a href="https://rho.store" target="_blank">rho store</a> as DB, 
    and with weather data from <a href="https://open-meteo.com" target="_blank">Open Meteo</a>.</p>
    </div>
    """)


def display_city_map(city_data: pd.DataFrame) -> None:
    """Display map for selected city."""
    st.map(
        city_data,
        size=10 ** 5,
        zoom=3,
        width=1000,
        height=200
    )


def plot_temperature_over_time(weather_data: pd.DataFrame, city_name: str) -> None:
    """Plot temperature time series."""
    st.divider()
    st.subheader(f"Temperature over time for {city_name}")
    plost.line_chart(
        weather_data,
        x="timestamp",
        y="temperature",
        pan_zoom=None
    )


def plot_monthly_comparison(weather_data: pd.DataFrame) -> None:
    """Plot monthly temperature comparison."""
    st.divider()
    st.subheader("Comparison by month over years")
    plost.time_hist(
        data=weather_data,
        date="timestamp",
        x_unit="year",
        y_unit="month",
        color="temperature",
        aggregate="median",
        legend=None,
    )


def plot_current_month_distribution(weather_data: pd.DataFrame, city_name: str) -> None:
    """Plot temperature distribution for current month."""
    current_date = datetime.date.today()
    month_name = calendar.month_name[current_date.month]

    weather_data_this_month = weather_data[weather_data["timestamp"].dt.month == current_date.month]
    st.divider()
    st.subheader(f"Distribution for daily temperatures in {city_name} during {month_name}")
    plost.hist(
        data=weather_data_this_month,
        x="temperature",
        aggregate="count"
    )


def display_temperature_analysis(result: dict) -> None:
    """Display temperature analysis results in a table."""
    result_items = [{
        "Title": f"Latest temperature ({result['latest_date'].isoformat()})",
        "Result": f"{result['latest_temperature']}°C"
    }, {
        "Title": "Historical Mean",
        "Result": f"{result['mean_temperature']}°C"
    }, {
        "Title": "Historical Standard Deviation",
        "Result": f"{result['std_temperature']}°C"
    }, {
        "Title": "Historical Range (min - max)",
        "Result": f"{result['min_temperature']}°C - {result['max_temperature']}°C"
    }, {
        "Title": "Normal Range (+/- 2 sigma)",
        "Result": f"{result['lower_bound']}°C - {result['upper_bound']}°C"
    }, {
        "Title": "Deviation from historical mean",
        "Result": f"""
            {result['deviation_from_mean']}°C 
            ({result['deviation_from_mean_percentage']}% 
            {result['deviation_direction']} than {result['mean_temperature']}°C)
            """
    }, {
        "Title": "Is the current temperature within normal range?",
        "Result": 'Yes' if result['is_normal'] else 'No'
    }]
    st.table(result_items)


def main() -> None:
    """Main Streamlit app function."""
    st.set_page_config(page_title="Weather Data Analysis", page_icon=":thermometer:", layout="centered")
    st.title("Weather Data Analysis")
    st.text("Select a city to see the weather data for that city. The demo supports the top 800 cities by population.")
    render_description()

    # Load city data
    cities_df = get_cities_df_cached()
    cities_names = sorted(cities_df["city"].to_list())

    # City selection
    option = st.selectbox("Select a city", cities_names)

    # Process selected city
    if option:
        # Find city data
        matches = cities_df[cities_df["city"] == option]
        first_match = matches.iloc[0]
        city_name = first_match["city"]

        # Display city map
        display_city_map(matches)

        # Fetch and log weather data
        logger.info("Fetching weather data for %s", city_name)
        weather_data = get_daily_temperature_data(
            latitude=first_match["latitude"],
            longitude=first_match["longitude"],
            start_date=datetime.date(2000, 1, 1),
            end_date=datetime.date.today()
        )

        # Visualizations
        plot_temperature_over_time(weather_data, city_name)
        plot_monthly_comparison(weather_data)
        plot_current_month_distribution(weather_data, city_name)

        # Temperature analysis
        result = analyze_temperature(weather_data)
        display_temperature_analysis(result)


if __name__ == "__main__":
    main()
