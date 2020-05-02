import json
import os
from typing import NoReturn
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime as dt
from selenium.webdriver.common.keys import Keys


class Functions:
    """
    :Methods:
     - find_element
     - attribute
     - search_text
     - check
     - is_element_present
    """
    def __init__(self, driver):
        """
        :Args:
         - driver: webdriver for browser
        """
        self.driver = driver

    def find_element(self, selector: str, click=False, keys=''):
        """
        Finds elements by css selector.

        :Args:
         - selector: CSS selector string, ex: 'a.nav#home'
         - click: type boolean - "True"/"False" (default "False")
         - keys: type str (default empty)

        :Returns:
         if click=False and not keys
         - WebElement: the element if it was found

        :Raises:
         - NoSuchElementException: if the element wasn't found

        :Usage:
            click = function.find_element('.foo', click=True)
            keys = function.find_element('.foo', click=False, keys='test')
            element = function.find_element('.foo')
        """
        self.check(selector)
        if click:
            self.driver.find_element_by_css_selector(selector).click()
        if len(str(keys)):
            self.driver.find_element_by_css_selector(selector).send_keys(Keys.CONTROL + 'a')
            self.driver.find_element_by_css_selector(selector).send_keys(str(keys))
        if not click and not keys:
            return self.driver.find_element_by_css_selector(selector)

    def attribute(self, selector: str, attribute: str):
        """
        :Args:
         - selector: CSS selector string, ex: 'a.nav#home'
         - attribute: Name of the attribute/property to retrieve

        :Returns:
         - value of elements attribute

        :Usage:
            value = function.attribute('.foo', 'title')
        """
        self.check(selector)
        if attribute:
            return self.driver.find_element_by_css_selector(selector).get_attribute(attribute)

    def search_text(self, selector: str):
        """
        :Args:
         - selector: CSS selector string, ex: 'a.nav#home'

        :Returns:
         - A string of text directly after the start tag, or None

        :Usage:
            text = function.search_text('.foo')
        """
        self.check(selector)
        return self.driver.find_element_by_css_selector(selector).text

    def check(self, selector: str, sec=0) -> bool:
        """
        :Args:
         - selector: CSS selector string, ex: 'a.nav#home'
         - sec: seconds (default sec=0)

        :Returns:
         - boolean False

        :Raises:
         - ValueError

        :Usage:
            check = function.check('.foo')
            check = function.check('.foo', 5)
        """
        element = self.is_element_present(By.CSS_SELECTOR, selector)
        start_time = dt.now()
        while element is False:
            action_time = dt.now() - start_time
            if sec > 0:
                if action_time.seconds > sec:
                    self.driver.close()
                    return False
            if sec <= 0:
                if action_time.seconds > 10:
                    self.driver.close()
                    raise ValueError('Превышено время ожидания')
            element = self.is_element_present(By.CSS_SELECTOR, selector)
        return True

    def is_element_present(self, how, what: str) -> bool:
        """
        :Args:
         - how: locator (ex: By.CSS_SELECTOR, By.ID, etc.)
         - selector: CSS selector string, ex: 'a.nav#home'

        :Returns:
         - boolean True

        :Raises:
         - boolean False

        :Usage:
            check = function.check('.foo')
            check = function.check('.foo', 5)
        """
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def today_dt(self) -> str:
        now = dt.today().strftime('%d-%m-%y_%H-%M')
        return now

    def save_file(self, case: str, desc: str, info: str, exc: str, group_name: str) -> NoReturn:
        case_object = {
            "Case": case,
            "Description": desc,
            "Info": info,
            "Error": exc
        }

        date = self.today_dt()
        file = f"{group_name}_log_{date}.json"  # название json файла

        if not os.path.isfile(file):  # проверка, существует ли json файл в директории
            """
            если файла нет:
                1. создается новый файл
                2. в файл парстится массив с объектов
            """
            with open(file, 'a') as f:
                json.dump([case_object], f, indent=4, ensure_ascii=False)
            """
            если файл есть:
                1. открытвается данный файл
                2. расспарсивается json
                3. в массив добавляется еще объект
                4. и в конце заново парсится в файл
            """
        else:
            with open(file, 'r+') as read:
                tmp_data = json.load(read)
                tmp_data.append(case_object)

            with open(file, 'w') as f:
                json.dump(tmp_data, f, indent=4, ensure_ascii=False)