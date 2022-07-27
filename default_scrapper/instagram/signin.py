import os
import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from .webdriver import WebDriver

COOKIE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "tmp",
    "cookies.json"
)

def load_cookies():
    if not os.path.exists(COOKIE_PATH):
        return None

    with open(COOKIE_PATH, "r") as file:
        cookies = json.loads(file.read())
    return cookies

def save_cookies(cookies):
    os.makedirs(os.path.dirname(COOKIE_PATH), exist_ok=True)
    with open(COOKIE_PATH, "w") as file:
        json.dump(cookies, file)

def signin(username: str, password: str, use_cookie: bool=True):
    loaded_cookies = load_cookies() if use_cookie else None

    driver = WebDriver()
    wait = WebDriverWait(driver, 15, 500)

    driver.get("https://www.instagram.com")
    driver.implicitly_wait(5)

    if loaded_cookies is None:
        # Enter usernae
        username_input = wait.until(expected_conditions.visibility_of_element_located((By.NAME, "username")))
        time.sleep(1)
        WebDriver.send_keys(username_input, username)

        # Enter password
        password_input = wait.until(expected_conditions.visibility_of_element_located((By.NAME, "password")))
        time.sleep(1)
        WebDriver.send_keys(password_input, password)

        # Click sign-in button
        signin_button = wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "#loginForm > div > div:nth-child(3) > button")))
        signin_button.click()
        time.sleep(1)
    else:
        for cookie in loaded_cookies:
            driver.add_cookie(cookie)
        print("Saved cookies have been loaded.")

    # Search any tag to build more cookies
    driver.get("https://www.instagram.com/explore/tags/instagram")
    driver.implicitly_wait(5)

    register_button_ko, register_button_en = None, None
    try:
        register_button_ko = driver.find_element(By.XPATH, "//div[text()=\"가입하기\"]")
    except:
        pass
    try:
        register_button_en = driver.find_element(By.XPATH, "//div[text()=\"Sign Up\"]")
    except:
        pass
    if register_button_ko is not None or register_button_en is not None:
        # Not signed in
        return signin(username, password, False)

    # Get activated cookies after sign-in
    cookies = driver.get_cookies()

    driver.quit()

    if loaded_cookies is None or not use_cookie:
        save_cookies(cookies)
        print(f"Cookies have been saved in `{COOKIE_PATH}`.")

    return cookies
