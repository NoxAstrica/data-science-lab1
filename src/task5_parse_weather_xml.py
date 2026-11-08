import xml.etree.ElementTree as ET
import csv
from typing import List, Dict


def parse_weather_xml(xml_file: str) -> List[Dict[str, any]]:
    tree = ET.parse(xml_file)
    root = tree.getroot()

    data = []
    for day in root.findall("day"):
        data.append({
            "date": day.find("date").text,
            "temperature": float(day.find("temperature").text),
            "humidity": int(day.find("humidity").text),
            "precipitation": float(day.find("precipitation").text),
        })
    return data


def save_to_csv(data: List[Dict[str, any]], filename: str = "parsed_weather_data.csv") -> None:
    headers = ["Date", "Temperature", "Humidity", "Precipitation"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for r in data:
            writer.writerow({
                "Date": r["date"],
                "Temperature": r["temperature"],
                "Humidity": r["humidity"],
                "Precipitation": r["precipitation"],
            })


if __name__ == "__main__":
    try:
        # Parse the XML file
        import os
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        xml_path = os.path.join(script_dir, "weather_data.xml")
        weather_data = parse_weather_xml(xml_path)

        # Save the parsed data to a CSV file
        save_to_csv(weather_data)
        print("Data has been successfully parsed and saved to parsed_weather_data.csv.")
    except Exception as e:
        print(f"An error occurred: {e}")
