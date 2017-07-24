class Matrix:

    def __init__(self, browser, height, width):
        self.browser = browser
        self.driver = self.browser.driver
        self.height = height
        self.width = width
        self.init()
        self.cssToVal = {
            'blank': None,
            'open0': 0,
            'open1': 1,
            'open2': 2,
            'open3': 3,
            'open4': 4,
            'open5': 5,
            'open6': 6,
            'open7': 7,
            'open8': 8,
            'bombflagged': -1,
            'bombdeath': -999,
            'bombrevealed': -999
        }

    # Game starts with empty matrix
    def init(self):
        self.error = None
        self.values = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(None)
            self.values.append(row)

    # Update the matrix
    def update(self):
        cells = self.driver.find_elements_by_class_name('square')
        for i in range(self.height):
            for j in range(self.width):
                cellClasses = cells[i*self.width+j].get_attribute('class')
                # cellId = str(i+1) + '_' + str(j+1)
                # print('Updating cell ' + cellId)
                self.values[i][j] = self.getValue(cellClasses)

    # Parse cell css classes to get value
    def getValue(self, cssclasses):
        # print('Translating css classes:' + cssclasses)
        # Remove the first sqaure classp
        cssClass = cssclasses.strip('square ')
        val = self.cssToVal[cssClass]
        if val is not None and val == -999:
            self.error = 'Bomb'
        # print('To value: ' + str(val))
        return val

    # Get surrounding neighbours (up to 8)
    def getNeighbours(self, i, j):
        imaginaryNeighbours = [
            (i-1, j-1),
            (i-1, j),
            (i-1, j+1),
            (i, j-1),
            (i, j+1),
            (i+1, j-1),
            (i+1, j),
            (i+1, j+1),
        ]
        neighbours = []
        for (x, y) in imaginaryNeighbours:
            if self.indexIsInRange(x, y):
                neighbours.append((x, y))

        return neighbours

    # Check if index is in range
    def indexIsInRange(self, row, col):
        if row < 0 or row > self.height-1:
            return False
        if col < 0 or col > self.width-1:
            return False
        return True

    # Scan through all cells
    def scan(self):
        self.updated = False
        for i in range(self.height):
            for j in range(self.width):
                self.inspect(i, j)
                if self.hasError():
                    return False
        return self.updated

    # See what we can do with this cell
    def inspect(self, i, j):
        cellId = str(i+1) + '_' + str(j+1)
        val = self.values[i][j]
        print('Inspecting cell ' + cellId + ', with val of ' + str(val))
        if val is not None and 1 <= val <= 8:
            print('This cell has ' + str(val) + ' bombs around it')
            # Check neighbour cells (up to 8)
            blanks = []
            bombsFlagged = 0
            for (x, y) in self.getNeighbours(i, j):
                if self.values[x][y] is None:
                    blanks.append((x, y))
                elif self.values[x][y] == -1:
                    bombsFlagged += 1
            # No work to do
            if len(blanks) == 0:
                print('But it has no blank neighbours')
                return
            if bombsFlagged == val:
                print('All the bombs already found around ' + cellId)
                print('Clicking on all blanks...')
                for (x, y) in blanks:
                    self.click(x, y)
                    if self.hasError():
                        return
            elif val == bombsFlagged + len(blanks):
                print('Mark all blanks as bombs around ' + cellId)
                for (x, y) in blanks:
                    self.flag(x, y)
            else:
                print('Nothing to do with this cell, here\' some evidence:')
                print('Val: ' + str(val))
                print('BombsFlagged: ' + str(bombsFlagged))
                print('No of blanks: ' + str(len(blanks)))
            # Update all at once
            self.update()
        else:
            print('This cell provides no value')

    # Click a cell to reavel value
    def click(self, row, col):
        self.browser.click(row, col)
        self.updated = True

    # Flag a cell as bomb
    def flag(self, row, col):
        self.browser.flag(row, col)
        self.values[row][col] = -1
        self.updated = True

    def hasError(self):
        return self.error is not None
