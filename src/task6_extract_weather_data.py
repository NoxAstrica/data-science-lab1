import csv
import re
from typing import List, Dict


def clean_text(line: str) -> str:
    line = line.replace("\xa0", " ")
    line = line.encode("ascii", "ignore").decode()
    return line.strip()


def extract_weather_data(text_file: str) -> List[Dict[str, any]]:
    pattern = re.compile(
        r"Date:\s*(\d{4}-\d{2}-\d{2}),\s*"
        r"Max Temp:\s*(-?\d+(?:\.\d+)?)\D*,\s*"
        r"Min Temp:\s*(-?\d+(?:\.\d+)?)\D*,\s*"
        r"Humidity:\s*(\d+)\D*,\s*"
        r"Precipitation:\s*(\d+(?:\.\d+)?)"
    )

    data = []
    with open(text_file, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = clean_text(line)
            match = pattern.search(line)
            if match:
                data.append({
                    "date": match.group(1),
                    "max_temperature": float(match.group(2)),
                    "min_temperature": float(match.group(3)),
                    "humidity": int(match.group(4)),
                    "precipitation": float(match.group(5)),
                })
    return data


def save_to_csv(data: List[Dict[str, any]], filename: str = "extracted_weather_data.csv") -> None:
    headers = ["Date", "Max Temperature", "Min Temperature", "Humidity", "Precipitation"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for r in data:
            writer.writerow({
                "Date": r["date"],
                "Max Temperature": r["max_temperature"],
                "Min Temperature": r["min_temperature"],
                "Humidity": r["humidity"],
                "Precipitation": r["precipitation"],
            })


if __name__ == "__main__":
    try:
        # Extract data from the text file
        import os
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        txt_path = os.path.join(script_dir, "weather_report.txt")
        weather_data = extract_weather_data(txt_path)

        # Save the extracted data to a CSV file
        save_to_csv(weather_data)
        print("Data has been successfully extracted and saved to extracted_weather_data.csv.")
    except Exception as e:
        print(f"An error occurred: {e}")
