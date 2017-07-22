#!/usr/bin/env python3

import helpers


class Matrix:

    def __init__(self, browser, height, width):
        self.browser = browser
        self.height = height
        self.width = width
        # Game starts with empty matrix
        self.values = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(None)
            self.values.append(row)

    def print(self):
        for i in range(self.height):
            for j in range(self.width):
                print(self.values[i][j])
