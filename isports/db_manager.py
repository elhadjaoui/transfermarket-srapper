from pymongo import MongoClient
import os
import dotenv

dotenv.load_dotenv()


db = MongoClient(os.getenv('MONGO_URI')).sportime
# db.uplayers.create_index("playerId", 1)
def save_player_to_db(player):
    db.uplayers.insert_one(player)
