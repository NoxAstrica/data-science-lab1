import csv
from typing import Dict, List, Union, TextIO

try:
    from .utils import load_json
except ImportError:
    from utils import load_json


def summarize_weather_data(data: List[Dict[str, any]]) -> Dict[str, float]:
    n = len(data)
    return {
        "average_max_temp": sum(d["max_temperature"] for d in data) / n,
        "average_min_temp": sum(d["min_temperature"] for d in data) / n,
        "total_precipitation": sum(d["precipitation"] for d in data),
        "average_wind_speed": sum(d["wind_speed"] for d in data) / n,
        "average_humidity": sum(d["humidity"] for d in data) / n,
        "hot_days": sum(d["max_temperature"] > 30 for d in data),
        "windy_days": sum(d["wind_speed"] > 15 for d in data),
        "rainy_days": sum(d["precipitation"] > 0 for d in data),
    }


def export_to_csv(data: List[Dict[str, any]], file: Union[str, TextIO]) -> None:
    headers = ["Date", "Max Temperature", "Min Temperature", "Precipitation", "Wind Speed", "Humidity",
               "Weather Description", "Is Hot Day", "Is Windy Day", "Is Rainy Day"]

    def write_data(writer):
        writer.writeheader()
        for d in data:
            writer.writerow({
                "Date": d["date"],
                "Max Temperature": d["max_temperature"],
                "Min Temperature": d["min_temperature"],
                "Precipitation": d["precipitation"],
                "Wind Speed": d["wind_speed"],
                "Humidity": d["humidity"],
                "Weather Description": d["weather_description"],
                "Is Hot Day": d["max_temperature"] > 30,
                "Is Windy Day": d["wind_speed"] > 15,
                "Is Rainy Day": d["precipitation"] > 0,
            })

    if isinstance(file, str):
        with open(file, "w", newline="", encoding="utf-8") as f:
            write_data(csv.DictWriter(f, fieldnames=headers))
    else:
        write_data(csv.DictWriter(file, fieldnames=headers))


if __name__ == "__main__":
    try:
        # Load the JSON data
        import os
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "tokyo_weather_complex.json")
        weather_data = load_json(json_path)

        # Summarize the weather data
        summary = summarize_weather_data(weather_data['daily'])

        # Print the summary for verification
        print("Weather Data Summary:")
        for key, value in summary.items():
            print(f"{key}: {value}")

        # Export the summarized data to a CSV file
        export_to_csv(weather_data['daily'], "tokyo_weather_summary.csv")

        print("Data successfully exported to tokyo_weather_summary.csv")
    except Exception as e:
        print(f"An error occurred: {e}")
