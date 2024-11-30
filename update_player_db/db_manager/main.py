import os
import pandas as pd
from postgresql_manager import  update_players
import json
import logging
logging.basicConfig(filename='my_main.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')


def get_players():
    return pd.read_csv(os.path.join(os.path.dirname(__file__), '../data', 'players.csv'), on_bad_lines='skip')

def save_broken_data(players):
    try:
        logging.info(f"Saving broken data to JSON file")
        with open('broken_data.json', 'w') as file:
            json.dump(players, file)
    except Exception as e:
        logging.info(f"Error: {e}")


def main():
    broken_data = []
    for _, row in get_players().iterrows():
        try:
            # search and update player in DB
            tm_data = {
                "tm_photo": row['image'],
                "tm_name": row['name'],
                "tm_market_value": row['marketValue'],
                "tm_id": row['playerId'],
            }
            if not update_players(row['name'], int(row['number']), row['citizenship'], tm_data, logging):
                raise Exception(f"TM_Player {row['name']} not in DB")
            else:
                logging.info(f"TM_Player {row['name']} updated in DB")
        except Exception as e:
            logging.info(f"Error: {e}")
            # print(len(broken_data))
            broken_data.append(row['playerId'])
    save_broken_data(broken_data)


if __name__ == "__main__":
    print("Launching script...")
    main()
    pass
