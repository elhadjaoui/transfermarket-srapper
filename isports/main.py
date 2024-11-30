import logging
logging.basicConfig(filename='my_main.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')

import json
from api_client import get_players_for_team
from storage_manager import upload_photo_to_azure
from db_manager import save_player_to_db


# Read teams from JSON file
with open('../utils/sportime_teams.json', 'r') as file:
    logging.debug("Reading teams from JSON file")
    teams = json.load(file)

def main():
    try:
        for team in teams:
            team_id = team['teamId']
            print(f"Fetching players for team {team_id}")
            logging.info(f"Fetching players for team {team_id}")
            players = get_players_for_team(team_id)
            for player in players:
                logging.debug(f"Uploading photo for player {player['playerId']}")
                photo_url = upload_photo_to_azure(player['photo'], player['playerId'], logging)
                player['photo'] = photo_url
                player['teamName'] = team['name']
                logging.debug(f"Saving player {player['playerId']} to DB")
                save_player_to_db(player)
    except Exception as e:
        logging.info(f"Error: {e}")


if __name__ == "__main__":
    print("Launching script...")
    print("Fetching data from isportsapi.com...")
    main()
    pass