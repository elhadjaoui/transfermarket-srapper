from operator import contains
import sys
import re
import json
import subprocess
import os
import dotenv

dotenv.load_dotenv()


try:
    from dotenv import load_dotenv, dotenv_values
except ModuleNotFoundError:
    print("module 'dotenv' is not installed")
    print("installing 'python-dotenv'..")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "python-dotenv"])
try:
    from selenium import webdriver
except ModuleNotFoundError:
    print("module 'selenium' is not installed")
    print("installing 'selenium'..")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])

from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

try:
    from webdriver_manager.chrome import ChromeDriverManager
except ModuleNotFoundError:
    print("module 'webdriver_manager' is not installed")
    print("installing 'webdriver_manager'..")
    subprocess.check_call([sys.executable, "-m", "pip",
                          "install", "webdriver_manager"])
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import random
import time


RED = "\033[0;31m"  # ANSI ESCAPE CODE
GREEN = "\033[0;32m"
CYAN = "\033[0;36m"
NC = "\033[0m"

print(CYAN, "Launching script...")
options = Options()

options.add_argument("--lang=en-US")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options,
    desired_capabilities={"pageLoadStrategy": "none"}
)
driver.maximize_window()
# driver.set_page_load_timeout(6)
actions = ActionChains(driver)
max_retries = 2

def get_file_to_save_path(clubId):
    league_path = os.path.join(os.path.dirname(__file__), '..', f'utils/players/{os.getenv("LEAGUE", "default_league")}_{os.getenv("SAISON", "default_league")}')
    if not os.path.exists(league_path):
        os.mkdir(league_path)
    return  os.path.join(league_path, f"{str(clubId)}_players.json")
def get_file_path_to_read():
    clubs_utils_path = os.path.join(os.path.dirname(__file__), '..', 'utils/clubs')
    return  os.path.join(clubs_utils_path, f"{os.getenv('LEAGUE', 'default_league')}_{os.getenv('SAISON', 'default_league')}_clubs.json")

def switch_to_privacy_iframe():
    try:
        coockies = WebDriverWait(driver,float(os.getenv('TIME_TO_SLEEP'))).until(
            EC.presence_of_element_located(
                (By.XPATH, "//iframe[@title='SP Consent Message']")
            )
        )
        driver.switch_to.frame(coockies)
        accept = WebDriverWait(driver,float(os.getenv('TIME_TO_SLEEP'))).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[text()='ACCEPT ALL']"))
        )
        accept.click()
        driver.switch_to.default_content()
    except (NoSuchElementException, TimeoutException):
        print("No such element found")
        return

def get_players_link(max_players=35, clubLink="", clubId=0):
    players = []
    i = 0
    for i in range(1, max_players + 1):
        retries = 0
        while retries < max_retries:
            try:
                xpath = f"//*[@id='yw1']/table/tbody/tr[{i}]/td[2]/table/tbody/tr[1]/td[2]/a"
                player_link = (WebDriverWait(driver, float(os.getenv('TIME_TO_SLEEP'))).until(EC.presence_of_element_located((By.XPATH,xpath,))).get_attribute("href"))
                # clubId = re.search(r'/verein/(\d+)', clubLink)
                # playerId = re.search(r'/spieler/(\d+)', player_link)
                print(f"Fetching player {player_link}")
                players.append(player_link)
                break
            except (NoSuchElementException, TimeoutException) as e:
                print(f"Error fetching player at row : {i}: {e}")
                retries += 1  # Increment the retry counter
                if retries >= max_retries:
                    print(f"Maximum retries reached for player id: {i}")
    return players

def go_to_player_link():
    try:
        with open(get_file_path_to_read(), "r") as jsonFile:
            clubs = json.load(jsonFile)
            for club in clubs:
                driver.get(club)
                # switch_to_privacy_iframe()
                clubId = re.search(r'/verein/(\d+)', club)
                clubId = clubId.group(1)
                print(f"Fetching players for club {clubId}")
                players = get_players_link(clubLink=club, clubId=clubId)
                print(f"Found {len(players)} players for club {clubId}")
                print(f"Saving players for club {clubId}...")
                print(players)
                with open(get_file_to_save_path(clubId=clubId), "w") as jsonFile:
                    json.dump(players, jsonFile, indent=4)
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error fetching club : {e}")

    # time.sleep(float(os.getenv("TIME_TO_SLEEP")))
  


def start():
    driver.get("https://www.transfermarkt.com/")
    switch_to_privacy_iframe()

    go_to_player_link()
    # time.sleep(float(os.getenv("TIME_TO_SLEEP")))
    print("Done.")
    driver.quit()


start()
