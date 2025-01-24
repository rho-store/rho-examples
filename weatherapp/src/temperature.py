import numpy as np
import pandas as pd


def analyze_temperature(df: pd.DataFrame) -> dict:
    # Ensure "timestamp" is a datetime column
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Get the latest data point
    latest_data = df.loc[df["timestamp"].idxmax()]
    latest_temperature = latest_data["temperature"]
    latest_date = latest_data["timestamp"].date()

    # Filter historical data for the same month (ignoring year)
    historical_data = df[df["timestamp"].dt.month == latest_date.month]

    # Calculate statistics
    mean_temp = historical_data["temperature"].mean()
    std_temp = historical_data["temperature"].std()
    min_temp = historical_data["temperature"].min()
    max_temp = historical_data["temperature"].max()

    # Check if the current temperature is normal
    lower_bound = mean_temp - 2 * std_temp
    upper_bound = mean_temp + 2 * std_temp
    is_normal = lower_bound <= latest_temperature <= upper_bound

    # Calculate deviation from mean
    deviation_from_mean = latest_temperature - mean_temp
    deviation_from_mean_percentage = 100 * abs(deviation_from_mean / mean_temp)
    deviation_direction = "lower" if deviation_from_mean < 0 else "higher"
    return {
        "latest_date": latest_date,
        "latest_temperature": format_np_value(latest_temperature),
        "mean_temperature": format_np_value(mean_temp),
        "std_temperature": format_np_value(std_temp),
        "min_temperature": format_np_value(min_temp),
        "max_temperature": format_np_value(max_temp),
        "is_normal": bool(is_normal),
        "lower_bound": format_np_value(lower_bound),
        "upper_bound": format_np_value(upper_bound),
        "deviation_from_mean": format_np_value(deviation_from_mean),
        "deviation_from_mean_percentage": format_np_value(deviation_from_mean_percentage),
        "deviation_direction": deviation_direction,
    }


def format_np_value(val: np.float64 | np.int64, decimals: int = 2) -> float:
    return round(float(val), decimals)
