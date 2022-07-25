import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from config import *

def signin(username: str, password: str):
    driver = webdriver.get_webdriver()
    wait = WebDriverWait(driver, 15, 500)

    driver.get("https://www.instagram.com")
    driver.implicitly_wait(5)

    # Enter usernae
    username_input = wait.until(expected_conditions.visibility_of_element_located((By.NAME, "username")))
    time.sleep(1)
    username_input.send_keys(username)

    # Enter password
    password_input = wait.until(expected_conditions.visibility_of_element_located((By.NAME, "password")))
    time.sleep(1)
    password_input.send_keys(password)

    # Click sign-in button
    signin_button = wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "#loginForm > div > div:nth-child(3) > button")))
    signin_button.click()

    # Get activated cookies after sign-in
    cookies = driver.get_cookies()

    driver.quit()

    return cookies
