from operator import contains
import sys
import os
import re
import json
import subprocess

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