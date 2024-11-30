from bs4 import BeautifulSoup
import requests
import json
import re
import os
import pandas as pd
import dotenv
from unidecode import unidecode

dotenv.load_dotenv()

my_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OSX 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/71.0.3578.98 Safari/537.36",
              "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"}

session = requests.Session()
session.headers.update(my_headers)

default_image = "https://img.a.transfermarkt.technology/portrait/header/default.jpg?lm=1"
players_broken_data = []

def normalize(text):
    return unidecode(text)

def get_file_to_save_path( format='_players.json'):
    raw_players = os.path.join(os.path.dirname(__file__), '../..', f'data/raw/players')
    if not os.path.exists(raw_players):
        os.mkdir(raw_players)
    return  os.path.join(raw_players, f"{format}")


def get_players_file_path_to_read():
    players_file = os.path.join(os.path.dirname(__file__), '../..', f'utils/players')
    return  players_file


def save_as_json(data):
    with open(get_file_to_save_path(format="players.json"), "w") as jsonFile:
        json.dump(data, jsonFile, indent=4)

def save_as_csv(data):
    df = pd.DataFrame(data)
    file_path = get_file_to_save_path(format="players.csv")
    df.to_csv(file_path, mode='a', index=False, header=not os.path.exists(file_path))

def extract_data(link):
    # using session instead of requests.get() to  reduce the time spent in setting up new connections for each request.
    response = session.get(link, headers=my_headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    contry_box = soup.find('div', {'class': 'data-header__box--big'})
    country_flag = None if contry_box is None else contry_box.find('img', {'class':'flaggenrahmen'})
    country = '-' if country_flag is None else country_flag['title']

    player_id = link.split('/')[-1]
    image = soup.find('img', {'class': 'data-header__profile-image'})
    name = soup.find('h1', {'class': 'data-header__headline-wrapper'})
    number = soup.find('span', {'class': 'data-header__shirt-number'})
    market_value = soup.find('a', {'class': 'data-header__market-value-wrapper'})
    # market_value =  market_value.find('span')
    highest_market_value = soup.find('div', {'class': 'tm-player-market-value-development__max-value'})
    n_name = name.text.replace('\n', '').split()
    n_name = " ".join(n_name)
    full_name = re.sub(r'#\d+\s*', '', n_name, count=1)
    displayName = link.split('/')[3].replace('-', ' ')
    
    data = {
        'playerId': player_id,
        'name': normalize(full_name),
        'image': default_image if image is None else image['src'],
        'number': "-" if number is None  else number.text.replace('\n', '').replace(' ', '')[1:],
        'marketValue': '-' if market_value is None else market_value.text.split()[0].strip(),
        # 'highestMarketValue': '-' if highest_market_value is None else highest_market_value.text.replace('\n', '').replace(' ', '') ,
        'teamCountry': '-' if country is None else country,
        'displayName': displayName
    }
    new_data = {}
    # all_data = soup.find('div', {'class': 'info-table info-table--right-space'})
    all_data = soup.css.select_one('div[class*="info-table info-table--right-space"]')
    if all_data is None:
        print('broken')
        print(link)
        players_broken_data.append(link)
    all_data = all_data.find_all('span', recursive=False)
    key = ''
    value = ''
    index = 0
    for items in range(0, len(all_data), 2):
        key = all_data[items].text.replace('\n', '').replace(' ', '').replace(':', '').strip().lower()
        if key == 'citizenship':
            value = all_data[items + 1].find('img', {'class': 'flaggenrahmen'})
            value = '-' if value is None else value.get('title').strip()
            new_data[key] = value
        elif key == 'nameinhomecountry' or key == 'fullname':
            value = all_data[items + 1].text.replace('\n', '').strip()
            key = 'fullName'
            new_data[key] = normalize(value)
            index = index + 1
        # else:
        #     value = all_data[items + 1].text.replace('\n', '').strip()
        print(key, value)
    if index == 0:
        new_data['fullName'] = '-'
    data.update(new_data)
    return data

def go_to_player_link():
    players_path = os.path.join(os.path.dirname(__file__), '../..', 'utils/players.json')
    players_data = []
    with open(players_path, 'r') as f:
        players = json.load(f)
        for player in players:
            players_data.append(extract_data(player))
        # save_as_json(players_data)
            save_as_csv(players_data)
            # players_broken_data.append(filename)
            # continue
    with open('players_broken_data', "w") as jsonFile:
                json.dump(players_broken_data, jsonFile, indent=4)

if __name__ == "__main__":  
        go_to_player_link()
        print("Done.")


