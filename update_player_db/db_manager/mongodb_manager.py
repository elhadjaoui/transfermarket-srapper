from pymongo import MongoClient
import os
import dotenv
from unidecode import unidecode
# import logging

from fuzzywuzzy import process
from fuzzywuzzy import fuzz

dotenv.load_dotenv()

# logging.basicConfig(filename='my_main.log', level=logging.INFO,
#                     format='%(asctime)s %(levelname)s %(name)s %(message)s')
def normalize(text):
    return unidecode(text)

db = MongoClient(os.getenv('MONGO_URI')).sportime
# db.uplayers.create_index("playerId", 1)
def save_player_to_db(player):
    db.players.insert_one(player)

def update_player_in_db(player, tm_data):
    try:
        return db.players.update_one({"_id": player["_id"]},{"$set": tm_data})
    except Exception as e:
        print(e)
        print("Error updating player in DB")
        return 0

def search_players_in_db(search_name, player_number, player_nationality, tm_data, logging):
    candidate_players = list(db.players.find(
        {"number": player_number, "country": player_nationality},
        {"name": 1}
    ).limit(20))  #  limit based on expected data size and performance
    if not candidate_players:
        return 0
    # Extract names for fuzzy matching
    candidate_names = [player["name"] for player in candidate_players]
    best_name_match = process.extractOne(search_name, candidate_names, score_cutoff=90)  # score_cutoff can be adjusted
    print(best_name_match)
    if best_name_match:
        player =  db.players.find_one({"name": best_name_match[0], "number": player_number, "country": player_nationality})
        if player:
            logging.info(f"ISP_Player {player['playerId']} found in DB")
            if not update_player_in_db(player,tm_data):
                logging.info(f"ISP_Player {player['playerId']} not updated in DB")
                return 0
            else:
                logging.info(f"ISP_Player {player['playerId']} updated in DB")
                return 1
        else:
            return 0
    else:
        return 0

# tm_data = {
#     "tm_photo": "https://example.com/photo.jpg",
#     "tm_name": "Raphael rtc",
#     "tm_market_value": "2566666M",
#     "tm_highest_market_value": "30M",
#     "tm_age": 28
# }
# result = search_players_in_db("Ignacio Pena Sotorres", 13, "Spain", tm_data, logging)
# print(result)
