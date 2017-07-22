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
        self.matrix = Matrix(self.driver, self.height, self.width)

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
        # First take a random guess that does not end the game
        while True:
            randomRow = random.randrange(self.height)
            randomCol = random.randrange(self.width)
            self.click(randomRow, randomCol)

            if self.status() == 'facedead':
                self.restart()
            else:
                break

        while True:
            for i in range(self.height):
                for j in range(self.width):
                    val = self.matrix.values[i][j]
                    if val is not None and 1 <= val <= 8:
                        # Check neighbour cells (up to 8)
                        blanks = []
                        bombCount = 0
                        for (x, y) in self.matrix.getNeighbours(i, j):
                            if self.matrix.values[x][y] is None:
                                blanks.append((x, y))
                            elif self.matrix.values[x][y] == -1:
                                bombCount += 1
                        # If the number of blanks is equal to current val
                        if len(blanks) == val:
                            # We have flaged all the bombs
                            if bombCount == val:
                                for (x, y) in blanks:
                                    self.click(x, y)
                            # Mark all blanks as bombs
                            elif bombCount == 0:
                                for (x, y) in blanks:
                                    self.flag(x, y)

            if self.status() == 'facedead':
                self.restart()
            elif self.status() == 'facewin':
                print('We did it!')
                return

    # Click a cell to reavel value
    def click(self, row, col):
        self.browser.click(row, col)
        self.matrix.update()

    # Flag a cell as bomb
    def flag(self, row, col):
        self.browser.flag(row, col)
        self.matrix.values[row][col] = -1

    # Get the game status
    def status(self):
        for face in Puzzle.faces:
            if self.driver.find_element_by_class(face) is not None:
                return face

        return 'unknown'

    # Restart the game
    def restart(self):
        for face in Puzzle.faces:
            if self.driver.find_element_by_class(face) is not None:
                self.browser.restartGame(face)
        self.matrix.initWithEmptyVaules()
