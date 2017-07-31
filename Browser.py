from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import os


class Browser:

    def __init__(self):
        self.driver = self.getChromeDriver()

    def getChromeDriver(self):
        chromedriver = "/usr/local/bin/chromedriver"
        os.environ["webdriver.chrome.driver"] = chromedriver
        chrome_options = Options()
        # This make Chromium reachable
        chrome_options.add_argument("--no-sandbox")
        # Overrides default choices
        chrome_options.add_argument("--no-default-browser-check")
        chrome_options.add_argument("--disable-user-media-security=true")
        chrome_options.add_argument("--use-fake-ui-for-media-stream")
        return webdriver.Chrome(chromedriver, chrome_options=chrome_options)

    def elementExists(self, cssSelector):
        try:
            self.driver.find_element_by_css_selector(cssSelector)
        except NoSuchElementException:
            return False
        return True

    def reveal(self, row, col):
        cellCssId = str(row+1) + '_' + str(col+1)
        cell = self.driver.find_element_by_id(cellCssId)
        ActionChains(self.driver).click(cell).perform()
        print('Revealing sqaure ' + cellCssId)

    def flag(self, row, col):
        cellCssId = str(row+1) + '_' + str(col+1)
        cell = self.driver.find_element_by_id(cellCssId)
        ActionChains(self.driver).context_click(cell).perform()
        print('Flaging sqaure ' + cellCssId + ' as bomb')

    def restartGame(self):
        cell = self.driver.find_element_by_id('face')
        ActionChains(self.driver).click(cell).perform()
        print(os.linesep + 'Bad luck, restarting...' + os.linesep)
