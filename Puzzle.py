#!/usr/bin/env python3

import helpers
import os
from Matrix import Matrix


class Puzzle:
    DIFFICULTY = [
        'beginner',
        'intermediate',
        'expert',
        'custom'
    ]

    def __init__(self):
        # Get Selenium Chrome Driver
        self.browser = helpers.getChromeDriver()
        # Load game into browser
        self.browser.get('http://minesweeperonline.com/')
        # Load game setting
        self.loadSettings()
        # Load matrix from game
        self.matrix = Matrix(self.browser, self.height, self.width)

    # Load game settings like difficulty, height, width, and mines
    def loadSettings(self):
        for d in Puzzle.DIFFICULTY:
            radioButton = self.browser.find_element_by_id(d)
            if radioButton.is_selected():
                # Get difficulty level from radio buttons
                self.difficulty = d
                print('Difficulty: ' + d)
                # Get height, width, and mines
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
        return
