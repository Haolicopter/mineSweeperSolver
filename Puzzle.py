from Browser import Browser
from Matrix import Matrix
import random


class Puzzle:
    DIFFICULTY = {
        'beginner': 'beginner',
        'intermediate': 'intermediate',
        'expert': '',
        'custom': ''
    }
    FACES = [
        'facesmile',
        'faceooh',
        'facedead',
        'facewin'
    ]

    def __init__(self):
        self.browser = Browser()
        self.driver = self.browser.driver
        self.url = 'http://minesweeperonline.com/'

    def loadGame(self):
        self.driver.get(self.url)
        # Load game setting
        self.loadSettings()
        # Load matrix from game
        self.matrix = Matrix(self.browser, self.height, self.width)

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

    def set(self, difficulty):
        self.url += '#' + Puzzle.DIFFICULTY[difficulty]

    # Let's play!
    def play(self):
        self.loadGame()
        # First take a random guess
        self.randomClick()

        while True:
            self.matrix.scan()
            if self.matrix.hasError() or self.status() == 'facedead':
                print('Error!')
                self.restart()
                continue
            elif self.status() == 'facewin':
                print('We did it!')
                return

            if (self.matrix.scanNotEffective or
                    len(self.matrix.cellsToScan) == 0):
                print('Scans not effective, firing secret weapon...')
                self.randomClick()

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
                self.matrix.update()
                self.uselessScanCount = 0
                break

    # Get the game status
    def status(self):
        return self.driver.find_element_by_id('face').get_attribute('class')

    # Restart the game
    def restart(self):
        self.browser.restartGame()
        self.uselessScanCount = 0
        self.matrix.init()
        self.randomClick()
