from selenium.webdriver.chrome.options import Options
from selenium import webdriver


def set_up():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")  # запуск окна хрома в указанном размере
    chrome_options.add_argument("--incognito")  # запуск хрома в режиме инкогнито
    chrome_options.add_argument("--ignore-certificate-errors")
    # chrome_options.add_argument("--headless")  # запуск хрома в фоновом режиме
    chrome_options.add_argument("--disable-notifications")  # отключение всплывающих уведомлений в окне хрома
    chrome_options.add_argument("--disable-cache")  # отключение кэша
    chrome_options.add_argument("--disable-extensions")  # отключение расширений
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": "/tmp/src/go_services",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False
    })

    driver = webdriver.Chrome("./chromedriver", options=chrome_options)
    driver.implicitly_wait(10)
    return driver
