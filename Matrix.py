class Matrix:

    def __init__(self, driver, height, width):
        self.driver = driver
        self.height = height
        self.width = width
        self.initWithEmptyVaules()
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
    def initWithEmptyVaules(self):
        self.values = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(None)
            self.values.append(row)

    # Update the matrix
    def update(self):
        for i in range(self.height):
            for j in range(self.width):
                cellId = str(i+1) + '_' + str(j+1)
                cellClasses = self.driver.find_element_by_id(cellId).get_attribute("class")
                val = self.getValue(cellClasses)
                if val is not None and val == -999:
                    print('Shit! A bomb!')
                    return False
                self.values[i][j] = val

        return True

    # Parse cell css classes to get value
    def getValue(self, cssclasses):
        # Remove the first sqaure classp
        cssClass = cssclasses.strip('square ')
        val = self.cssToVal[cssClass]

        return val

    # Print out the matrix
    def print(self):
        for i in range(self.height):
            for j in range(self.width):
                print(self.values[i][j], end=', ')
            print()

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
