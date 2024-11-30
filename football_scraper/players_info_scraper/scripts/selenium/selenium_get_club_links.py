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
config = dotenv_values("data.env")
driver.maximize_window()
# driver.set_page_load_timeout(6)
actions = ActionChains(driver)



def switch_to_privacy_iframe():
    try:
        coockies = WebDriverWait(driver,10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//iframe[@title='SP Consent Message']")
            )
        )
        driver.switch_to.frame(coockies)
        accept = WebDriverWait(driver,10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[text()='ACCEPT ALL']"))
        )
        accept.click()
        driver.switch_to.default_content()
    except (NoSuchElementException, TimeoutException):
        print("No such element found")
        return

def get_clubs_link(max_clubs=20):
    clubs = []
    i = 0
    for i in range(1, max_clubs + 1):
        try:
            xpath = f"//table/tbody/tr[{i}]/td[@class='zentriert no-border-rechts']/a"
            club = (WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,xpath,))).get_attribute("href"))
            clubs.append(club)
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error fetching club at row {i}: {e}")
    return clubs

def go_to_website():
    driver.get(os.getenv("LEAGUE_URL"))
    # time.sleep(float(os.getenv("TIME_TO_SLEEP")))
    switch_to_privacy_iframe()
    clubs = get_clubs_link()
    utils_path = os.path.join(os.path.dirname(__file__), '..', 'utils/clubs')
    file_path = os.path.join(utils_path, f"{os.getenv('LEAGUE', 'default_league')}_{os.getenv('SAISON', 'default_league')}_clubs.json")
    with open(file_path, "w") as jsonFile:
        json.dump(clubs, jsonFile, indent=4)


def start():
    go_to_website()
    time.sleep(float(os.getenv("TIME_TO_SLEEP")))
    print("Done.")
    driver.quit()


start()
