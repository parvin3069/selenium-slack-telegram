import os
import sys
import time
import traceback
import unittest
sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__name__), "../slnm/app/slnm")))
import components
import functions
import chrome_options
from envparse import env


env.read_envfile()

GROUP_NAME = 'beru'
CASE = 'case for checking catalog'
DESC = 'case for checking catalog'


class run_test(unittest.TestCase):
    def test(self):
        function = ''
        url = env.str("URL")
        try:
            driver = chrome_options.set_up()
            component = components.Component(driver)
            function = functions.Functions(driver)
            component.get_url(url)
            section_title = component.random_catalog()
            info = {
                "Url": url,
                "Section title": section_title
            }
            driver.close()
            function.save_file(CASE, DESC, info, None, GROUP_NAME)
        except Exception as e:
            exc = traceback.format_exc()
            info = {
                "Ссылка": url
            }

            function.save_file(CASE, DESC, info, exc, GROUP_NAME)


if __name__ == "__main__":
    unittest.main()
