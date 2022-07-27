import os
import time
from selenium import webdriver

class WebDriver(webdriver.Chrome):
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument("no-sandbox")
        options.add_argument("incognito")
        options.add_argument("lang=ko")
        options.add_argument("disable-dev-shm-usage")
        options.add_argument("disable-gpu")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36")
        options.page_load_strategy = 'normal'

        driver_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__ + "/../")),
            "drivers",
            "chromedriver",
        )
        self.driver = super().__init__(driver_path, options=options)

    def send_keys(element, sequence: str):
        for character in sequence:
            element.send_keys(character)
            time.sleep(0.5)
