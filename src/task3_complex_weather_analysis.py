from typing import Dict, List, Any

try:
    from .utils import load_json
except ImportError:
    from utils import load_json


def analyze_daily_weather(day: Dict[str, Any], temp_threshold: float = 30, 
                          wind_threshold: float = 15, humidity_threshold: float = 70) -> Dict[str, Any]:
    return {
        "date": day["date"],
        "weather_description": day["weather_description"],
        "max_temperature": day["max_temperature"],
        "min_temperature": day["min_temperature"],
        "temperature_swing": day["max_temperature"] - day["min_temperature"],
        "wind_speed": day["wind_speed"],
        "humidity": day["humidity"],
        "precipitation": day["precipitation"],
        "is_hot_day": day["max_temperature"] > temp_threshold,
        "is_windy_day": day["wind_speed"] > wind_threshold,
        "is_uncomfortable_day": day["humidity"] > humidity_threshold,
        "is_rainy_day": day["precipitation"] > 0,
    }

def generate_daily_report(analysis: Dict[str, Any]) -> str:
    lines = [
        f"Date: {analysis['date']}",
        f"Weather: {analysis['weather_description']}",
        f"Temperature: Max {analysis['max_temperature']:.1f}°C, "
        f"Min {analysis['min_temperature']:.1f}°C "
        f"(Swing: {analysis['temperature_swing']:.1f}°C)",
    ]
    if analysis["is_hot_day"]:
        lines.append("It was a hot day.")
    if analysis["is_windy_day"]:
        lines.append("It was a windy day.")
    if analysis["is_uncomfortable_day"]:
        lines.append("The humidity made the day uncomfortable.")
    if analysis["is_rainy_day"]:
        lines.append("It was a rainy day.")
    else:
        lines.append("There was no precipitation.")
    return "\n".join(lines) + "\n"


def summarize_weather_analysis(analyses: List[Dict[str, Any]]) -> str:
    hottest = max(analyses, key=lambda a: a["max_temperature"])
    windiest = max(analyses, key=lambda a: a["wind_speed"])
    humid = max(analyses, key=lambda a: a["humidity"])
    rainiest = max(analyses, key=lambda a: a["precipitation"])
    return (
        "Weather Summary:\n"
        f"Hottest day: {hottest['date']} with a maximum temperature of {hottest['max_temperature']:.1f}°C\n"
        f"Windiest day: {windiest['date']} with wind speeds of {windiest['wind_speed']:.1f} km/h\n"
        f"Most humid day: {humid['date']} with a humidity level of {humid['humidity']}%\n"
        f"Rainiest day: {rainiest['date']} with {rainiest['precipitation']:.1f} mm of precipitation"
    )


if __name__ == "__main__":
    try:
        # Load the JSON data
        import os
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "tokyo_weather_complex.json")
        weather_data = load_json(json_path)

        # Analyze the weather data for each day
        analyses = [analyze_daily_weather(day) for day in weather_data['daily']]

        # Generate and print daily reports
        for analysis in analyses:
            report = generate_daily_report(analysis)
            print(report)

        # Generate and print a summary report
        summary_report = summarize_weather_analysis(analyses)
        print(summary_report)
    except Exception as e:
        print(f"An error occurred: {e}")
