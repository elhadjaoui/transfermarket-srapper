from operator import contains
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse
import os
import dotenv
import time

dotenv.load_dotenv()
max_clubs=20


my_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OSX 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/71.0.3578.98 Safari/537.36",
              "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"}

session = requests.Session()
session.headers.update(my_headers)

utils_path = os.path.join(os.path.dirname(__file__), '../..', 'utils')
file_path = os.path.join(utils_path, "clubs.json")

def get_clubs_link(soup):
    clubs = []
    i = 0
    for i in range(1, max_clubs + 1):
        try:
            css_selector = f"#yw1 > table > tbody > tr:nth-child({i}) > td.hauptlink.no-border-links > a:nth-child(1)"
            club = soup.select_one(css_selector).get("href")
            club = f"https://www.transfermarkt.us{club}"
            clubs.append(club)
        except (Exception) as e:
            print(f"Error fetching club at row {i}: {e}")
    return clubs
def go_to_website(league_url):
    response = session.get(league_url, headers=my_headers)
    print(f"Fetching {league_url}")
    soup = BeautifulSoup(response.text, 'html.parser')
    clubs = get_clubs_link(soup)
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        data = list(set(data + clubs))
    else:
        data = list(set(clubs))
    with open(file_path, 'w') as file:
        json.dump(data, file)

def start():
    leagues_path = os.path.join(os.path.dirname(__file__), '../..', 'utils/leagues.json')
    with open(leagues_path, "r") as jsonFile:
            leagues = json.load(jsonFile)
            for league in leagues:
                go_to_website(league)
start()
