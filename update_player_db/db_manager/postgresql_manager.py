
import json
import logging
from fuzzywuzzy import process
import psycopg2 as pg
from configuration import config


def update_player_in_db(best_match,search_name, player_number, tm_data):
    sql = """ 
    UPDATE player
    SET transfer_market = %s, name = %s
    WHERE number = %s AND name = %s;
                """
    tm_data = json.dumps(tm_data)
    updated_rows = 0
    try:
        params = config()
        with pg.connect(**params) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (tm_data,search_name, player_number, best_match))
                updated_rows = cur.rowcount
                # commit not needed because of with statement
    except (Exception, pg.DatabaseError) as error:
        print(f"Database error: {error}")
    return updated_rows


def get_players_from_db(number, nationality):
    """ get players from the players table """

    sql = """ 
        SELECT player.name,  player.number , country.name FROM player 
        INNER JOIN country ON player."countryId" = country.id
        WHERE player.number = %s AND country.name = %s;
        """
    conn = None
    try:
        params = config()
        conn = pg.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (number, nationality,))
        players = cur.fetchall()
        # print(players)
        cur.close()
        return players
    except (Exception, pg.DatabaseError) as error:
        pass
    finally:
        if conn is not None:
            conn.close()


def update_players(search_name, player_number, player_nationality, tm_data, logging):
    candidate_names = [player[0] for player in get_players_from_db(
        player_number, player_nationality)]
    best = process.extractBests(search_name, candidate_names)
    print(f"search_name = {search_name}, best_name_match = {best}")
    # best_name_match = process.extractOne(
    #     search_name, candidate_names, score_cutoff=90)  # score_cutoff can be adjusted
    # if best_name_match and best_name_match[1] != 100: # 100 means exact match so no need to update
    #     if not update_player_in_db(best_name_match[0], search_name, player_number, tm_data):
    #         logging.info(f" [ {search_name} ,{player_number}, {player_nationality} ] not updated in DB")
    #         return 0
    #     else:
    #         logging.info(f"[ {search_name} ,{player_number}, {player_nationality} ]  updated in DB")
    #         return 1
    # else:
    #     return 0


# if __name__ == '__main__':
#     tm_data = {
#         "tm_photo": "https://example.com/photo.jpg",
#         "tm_name": "Raphael rtc",
#         "tm_market_value": "2566666M",
#         "tm_highest_market_value": "30M",
#         "tm_age": 28
#     }
#     # print(get_players_from_db(10, "Spain"))
# result = update_players("Eberechi Eze", 10, "England", tm_data, logging)
# print(result)

# insert one vendor
# insert_data('3M Co.')
# insert one vendor
# insert_data('AKM Semiconductor Inc.')
# insert multiple vendors
