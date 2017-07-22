from Browser import Browser
from Matrix import Matrix
import random


class Puzzle:
    DIFFICULTY = [
        'beginner',
        'intermediate',
        'expert',
        'custom'
    ]
    FACES = [
        'facesmile',
        'faceooh',
        'facedead',
        'facewin'
    ]

    def __init__(self):
        # Get Selenium Chrome Driver
        self.browser = Browser()
        self.driver = self.browser.driver
        # Load game into browser
        self.driver.get('http://minesweeperonline.com/')
        # Load game setting
        self.loadSettings()
        # Load matrix from game
        self.matrix = Matrix(self.browser, self.height, self.width)
        self.lapsOfNoWork = 0

    # Load game settings like difficulty, height, width, and mines
    def loadSettings(self):
        for d in Puzzle.DIFFICULTY:
            radioButton = self.driver.find_element_by_id(d)
            if radioButton.is_selected():
                # Get difficulty level from radio buttons
                self.difficulty = d
                print('Difficulty: ' + d)
                # Get height, width, and number of mines
                params = radioButton.find_elements_by_xpath(
                    '../../following-sibling::td')
                self.height = int(params[0].get_attribute('innerHTML'))
                self.width = int(params[1].get_attribute('innerHTML'))
                self.mines = int(params[2].get_attribute('innerHTML'))
                print('Height: ' + str(self.height))
                print('Width: ' + str(self.width))
                print('Mines: ' + str(self.mines))

    # Let's play!
    def play(self):
        # First take a random guess
        self.randomClick()

        self.lapsOfNoWork = 0
        while True:
            updated = self.matrix.scan()
            if self.matrix.hasError():
                self.restart()
                continue

            if updated:
                self.lapsOfNoWork = 0
            else:
                self.lapsOfNoWork += 1

            # Ok, let's take a guess
            if self.lapsOfNoWork > 2:
                self.randomClick()

            if self.status() == 'facedead':
                self.restart()
            elif self.status() == 'facewin':
                print('We did it!')
                return

    # Take a random guess that does not end the game
    def randomClick(self):
        while True:
            # Pick a random row and col that is blank
            while True:
                randomRow = random.randrange(self.height)
                randomCol = random.randrange(self.width)
                if self.matrix.values[randomRow][randomCol] is None:
                    break

            print('Taking a random guess...')
            self.matrix.click(randomRow, randomCol)
            if self.status() == 'facedead':
                self.restart()
            else:
                self.lapsOfNoWork += 1
                break

    # Get the game status
    def status(self):
        return self.driver.find_element_by_id('face').get_attribute('class')

    # Restart the game
    def restart(self):
        self.browser.restartGame()
        self.lapsOfNoWork = 0
        self.matrix.init()
        self.randomClick()