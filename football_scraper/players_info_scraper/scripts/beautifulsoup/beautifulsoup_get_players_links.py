from bs4 import BeautifulSoup
import requests
import json
import re
import os
import dotenv

dotenv.load_dotenv()

my_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OSX 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/71.0.3578.98 Safari/537.36",
              "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"}

session = requests.Session()
session.headers.update(my_headers)

max_players = 35

def save_player(players):
    players_path = os.path.join(os.path.dirname(__file__), '../..', 'utils/players.json')
    if os.path.exists(players_path):
        with open(players_path, 'r') as file:
            data = json.load(file)
        data = list(set(data + players))
    else:
        data = list(set(players))
    with open(players_path, 'w') as file:
        json.dump(data, file)
def get_file_path_to_read():
    return os.path.join(os.path.dirname(__file__), '../..', 'utils/clubs.json')



def go_to_player_link():
    try:
        with open(get_file_path_to_read(), "r") as jsonFile:
            clubs = json.load(jsonFile)
            for club in clubs:
                response = session.get(club, headers=my_headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                # clubName = re.search(r'/(\w+)', club)
                # clubId = re.search(r'/verein/(\d+)', club)
                # clubId = clubId.group(1)
                players = []
                for i in range(1, max_players + 1):
                    css_selector = f"#yw1 > table > tbody > tr:nth-of-type({i}) > td:nth-of-type(2) > table > tr > td:nth-of-type(2) > a"
                    element = soup.css.select_one(css_selector)
                    print(i)
                    if element:
                        player_link = element['href']
                        # join the link with the base url
                        player_link = f"https://www.transfermarkt.us{player_link}"
                        players.append(player_link)
                    else:
                        print(f"Element not found for index {i}")
                save_player(players)
    except (Exception) as e:
        print(f"Error fetching club : {e}")

    # time.sleep(float(os.getenv("TIME_TO_SLEEP")))
  


def start():
    go_to_player_link()
    print("Done.")


start()
