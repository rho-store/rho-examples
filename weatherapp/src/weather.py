import datetime
import streamlit as st

import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry


def init_client() -> openmeteo_requests.Client:
    cache_session = requests_cache.CachedSession(
        backend="memory"
    )
    retry_session = retry(cache_session, retries=3, backoff_factor=0.2)
    return openmeteo_requests.Client(session=retry_session)


@st.cache_data
def get_daily_temperature_data(
        latitude: float,
        longitude: float,
        start_date: datetime.date,
        end_date: datetime.date
) -> pd.DataFrame:
    openmeteo_client = init_client()
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "daily": "temperature_2m_mean"
    }
    responses = openmeteo_client.weather_api(url, params=params)
    response = responses[0]
    daily = response.Daily()
    daily_temperature_2m = daily.Variables(0).ValuesAsNumpy()
    timestamp_range = pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s", utc=True),
        end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=daily.Interval()),
        inclusive="left"
    )
    data = {
        "timestamp": timestamp_range,
        "temperature": daily_temperature_2m
    }
    df = pd.DataFrame(data=data)
    df.dropna(inplace=True)
    return df
