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
        self.cellsToScan = {}

    # Update the matrix
    def update(self):
        cells = self.driver.find_elements_by_class_name('square')
        cellsWithValues = []
        for i in range(self.height):
            for j in range(self.width):
                cellClasses = cells[i*self.width+j].get_attribute('class')
                newVal = self.getValue(cellClasses)
                if self.hasError():
                    return False
                if self.values[i][j] != newVal:
                    self.values[i][j] = newVal
                if self.isValuable(self.values[i][j]):
                    cellsWithValues.append((i, j))

        for (i, j) in cellsWithValues:
            self.updateScanList(i, j)

    # Parse cell css classes to get value
    def getValue(self, cssclasses):
        # Remove the first sqaure class
        cssClass = cssclasses.strip('square ')
        val = self.cssToVal[cssClass]
        if val is not None and val == -999:
            self.error = 'Bomb'
        return val

    # Check if a cell needs scan
    def updateScanList(self, i, j):
        val = self.values[i][j]
        blanks = []
        bombsFlagged = 0
        for (x, y) in self.getNeighbours(i, j):
            if self.values[x][y] is None:
                blanks.append((x, y))
            elif self.values[x][y] == -1:
                bombsFlagged += 1
        cellId = str(i+1) + '_' + str(j+1)
        if len(blanks) == 0:
            if (i, j) in self.cellsToScan:
                del self.cellsToScan[(i, j)]
                print('Removing cell ' + cellId + ' from the scan list')
            return
        if bombsFlagged == val or val == bombsFlagged + len(blanks):
            if (i, j) not in self.cellsToScan:
                self.cellsToScan[(i, j)] = (blanks, bombsFlagged)
                print('Adding cell ' + cellId + ' to the scan list')
        elif (i, j) in self.cellsToScan:
            del self.cellsToScan[(i, j)]
            print('Removing cell ' + cellId + ' from the scan list')

    # Check if a cell is worth scaning
    def isValuable(self, val):
        return val is not None and 1 <= val <= 8

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
        print('Start new round of scan...')
        while len(self.cellsToScan) > 0:
            (i, j), (blanks, bombsFlagged) = self.cellsToScan.popitem()
            self.inspect(i, j, blanks, bombsFlagged)
            cellId = str(i+1) + '_' + str(j+1)
            print('Popping cell ' + cellId + ' from the scan list')
            if self.hasError():
                return False

    # See what we can do with this cell
    def inspect(self, i, j, blanks, bombsFlagged):
        cellId = str(i+1) + '_' + str(j+1)
        val = self.values[i][j]
        print('\nInspecting cell ' + cellId + ', with val of ' + str(val))
        if self.isValuable(val):
            print('#Bomb: ' + str(val))
            print('#BombFlag: ' + str(bombsFlagged))
            print('#Blanks: ' + str(len(blanks)))
            if bombsFlagged == val:
                print('All the bombs already found around ' + cellId)
                print('Clicking on all blanks...')
                for (x, y) in blanks:
                    self.reveal(x, y)
                    if self.hasError():
                        return
            elif val == bombsFlagged + len(blanks):
                print('Mark all blanks as bombs around ' + cellId)
                for (x, y) in blanks:
                    self.flag(x, y)
            # Update all at once
            self.update()

    # Click a cell to reveal value
    def reveal(self, row, col):
        if self.values[row][col] is not None:
            return
        self.browser.reveal(row, col)

    # Flag a cell as bomb
    def flag(self, row, col):
        if self.values[row][col] == -1:
            return
        self.browser.flag(row, col)
        self.values[row][col] = -1

    def hasError(self):
        return self.error is not None
