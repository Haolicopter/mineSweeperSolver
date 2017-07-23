from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
<<<<<<< HEAD
from selenium.common.exceptions import NoSuchElementException
=======
>>>>>>> 415ee25e8594b38fd5e1debe55c2034bb9f1f456
import os


class Browser:

    def __init__(self):
        self.driver = self.getChromeDriver()

<<<<<<< HEAD
    def getChromeDriver(self):
=======
    def getChromeDriver():
>>>>>>> 415ee25e8594b38fd5e1debe55c2034bb9f1f456
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

<<<<<<< HEAD
    def elementExists(self, cssSelector):
        try:
            self.driver.find_element_by_css_selector(cssSelector)
        except NoSuchElementException:
            return False
        return True

    def click(self, row, col):
        cellCssId = str(row+1) + '_' + str(col+1)
        cell = self.driver.find_element_by_id(cellCssId)
        ActionChains(self.driver).click(cell).perform()
        print('Clicking on sqaure ' + cellCssId)

    def flag(self, row, col):
        cellCssId = str(row+1) + '_' + str(col+1)
        cell = self.driver.find_element_by_id(cellCssId)
        ActionChains(self.driver).context_click(cell).perform()
        print('Flaging sqaure ' + cellCssId + ' as bomb')

    def restartGame(self):
        cell = self.driver.find_element_by_id('face')
        ActionChains(self.driver).click(cell).perform()
        print('Bad luck, restarting...')
=======
    def click(self, row, col):
        cellCssId = str(row+1) + '_' + str(col+1)
        cell = self.driver.find_element_by_css_selector(cellCssId)
        ActionChains(self.driver).click(cell).perform()

    def flag(self, row, col):
        cellCssId = str(row+1) + '_' + str(col+1)
        cell = self.driver.find_element_by_css_selector(cellCssId)
        ActionChains(self.driver).context_click(cell).perform()

    def restartGame(self, face):
        cell = self.driver.find_element_by_css_selector(face)
        ActionChains(self.driver).click(cell).perform()
>>>>>>> 415ee25e8594b38fd5e1debe55c2034bb9f1f456
