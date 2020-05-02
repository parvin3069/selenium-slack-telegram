import os
import random
import sys
import time
sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__name__), "../slnm/app/slnm")))
from typing import NoReturn
import functions


class Component:
    """
    :Methods:
     - auth
     - get_url
     - random_catalog
     - change_iframe
    """
    def __init__(self, driver):
        """
        :Attributes:
         - driver: webdriver for browser
         - function: class Functions
        """
        self.driver = driver
        self.function = functions.Functions(self.driver)

    def get_url(self, url) -> NoReturn:
        self.driver.get(url)
        if self.driver.title != "Маркетплейс Беру - большой ассортимент товаров " \
                                "из интернет-магазинов с быстрой доставкой и по выгодным ценам":
            exc = {
                "Action": "Go to page",
                "Result": f"Didn’t go to the desired page. Incorrect title: {self.driver.title}."
            }
            raise ValueError(exc)

    def auth(self, url: str, login: str, password: str) -> NoReturn:
        """
        :Args:
         - url: url for loads a web page in the current browser session
         - *user: user login and password (ex: ['test', '123'])

        :Raises:
         - ValueError: if the user is not logged in

        :Usage:
            auth = component.auth('http://test.com', 'test', '123')
        """
        self.driver.get(url)
        self.function.find_element("", False, login)
        self.function.find_element("", False, password)
        self.function.find_element("", True)  # btn Enter
        if self.driver.title != "":
            exc = f"Login failed"
            self.driver.close()
            raise ValueError(exc)

    def random_catalog(self) -> str:
        self.function.find_element("span._3RM4_n5whA", True)
        time.sleep(1)
        catalog = self.driver.find_elements_by_css_selector("li span")
        random_section = random.choice(catalog)
        random_section_title = random_section.text
        time.sleep(1)
        random_section.click()
        if self.function.search_text("div:nth-child(3) h1") != random_section_title:
            exc = {
                "Action": "Select a random section and go to this section.",
                "Result": "Didn’t go to the desired section."
            }
            self.driver.close()
            raise ValueError(exc)
        return random_section_title

    def change_iframe(self, iframe) -> NoReturn:
        if iframe == 'iframe':
            iframe = self.function.find_element("[name='mainFrame']")
            self.driver.switch_to.frame(iframe)
        if iframe == "default":
            self.driver.switch_to.default_content()

