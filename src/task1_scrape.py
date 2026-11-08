import requests
from bs4 import BeautifulSoup
from typing import Dict
import re

try:
    from .utils import save_to_json
except ImportError:
    from utils import save_to_json


def fetch_wikipedia_page(url: str) -> str:
    headers = {"User-Agent": "DS-Lab-1 student"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.text


def extract_title(soup: BeautifulSoup) -> str:
    return soup.find("h1").get_text(strip=True)


def extract_first_sentence(soup: BeautifulSoup) -> str:
    for p in soup.find_all("p"):
        text = p.get_text().strip()
        if text:
            text = re.sub(r"\[\d+\]", "", text)
            return text.split(". ")[0] + "."
    return ""


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Web_scraping"
    try:
        page_content = fetch_wikipedia_page(url)
        soup = BeautifulSoup(page_content, 'html.parser')

        # Extract the title of the page
        title = extract_title(soup)

        # Extract the first sentence of the first paragraph
        first_sentence = extract_first_sentence(soup)

        # Combine the extracted data
        extracted_data = {
            "title": title,
            "first_sentence": first_sentence
        }

        # Print the extracted data
        print("Extracted Data:", extracted_data)

        # Save the data to a JSON file
        save_to_json(extracted_data, 'extracted_wikipedia_data.json')

        print("Data successfully saved to extracted_wikipedia_data.json")
    except Exception as e:
        print(f"An error occurred: {e}")
