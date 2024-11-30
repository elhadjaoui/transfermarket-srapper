import requests
import os
import dotenv
from unidecode import unidecode

dotenv.load_dotenv()


def normalize(text):
    return unidecode(text)





def get_players_for_team(team_id):
    name = normalize("Ronald Araújo")
    try:
        # url = f"http://api.isportsapi.com/sport/football/player?api_key={os.getenv('API_KEY')}&teamId={team_id}"
        url = f"http://api.isportsapi.com/sport/football/player/search?api_key={os.getenv('API_KEY')}&name={name}"
        response = requests.get(url)
        if response.status_code != 200 :
            raise Exception(f"Error: {response.status_code}")
        elif response.json()['code'] != 0 or response.json()['message'] != 'success':
            raise Exception(f"Error: {response.json()['message']}")
        data = response.json()
        if data['data'] is None:
            raise Exception(f"Error: {data['message']}")
        print(data['data'][0])
    except Exception as e:
        print(e)
    # return data['data']

get_players_for_team(9)