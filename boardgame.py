import math

class BoardGame:
    def __init__(self, file_name: str):
        self.change_matrix(file_name)

    def change_matrix(self, file_name: str):
        with open(file_name, "r") as in_file:
            text = in_file.read()
            text.strip()
        self._start_matrix = []
        self._start_matrix = text.split(",")
        self._user_matrix = []
        self._user_matrix = ['CLEAR' for i in range(len(self._start_matrix))]
        self._symbols_matrix = []
        self._symbols_matrix = [0 for i in range(len(self._start_matrix))]
        self._white_matrix = []
        self._white_matrix = [False for i in range(len(self._start_matrix))]

        self._cols = int(math.sqrt(len(self._start_matrix)))
        self._rows = int(math.sqrt(len(self._start_matrix)))

    def cells_around(self, cell: (int, int)):
        x, y = cell
        list = []

        if x == 0:
            if y == 0:
                list.append((x, y + 1))
            elif y == self._rows - 1:
                list.append((x, y - 1))
            else:
                list.append((x, y - 1))
                list.append((x, y + 1))

            list.append((x + 1, y))

        elif x == self._cols - 1:
            if y == 0:
                list.append((x, y + 1))
            elif y == self._rows - 1:
                list.append((x, y - 1))
            else:
                list.append((x, y - 1))
                list.append((x, y + 1))

            list.append((x - 1, y))

        elif y == 0:
            list.append((x, y + 1))
            list.append((x + 1, y))
            list.append((x - 1, y))

        elif y == self._rows - 1:
            list.append((x, y - 1))
            list.append((x + 1, y))
            list.append((x - 1, y))

        else:
            list.append((x, y - 1))
            list.append((x + 1, y))
            list.append((x - 1, y))
            list.append((x, y + 1))

        return list

    def findDouble(self, cell: (int, int)):
        x, y = cell
        double_pos = []
        pos = 0
        val = 0
        if self._user_matrix[y * self._cols + x] == 'CIRCLE':
            pos = y * self._cols + x
            val = self.value_at((x, y))
            for x2 in range(self._cols):
                if self._user_matrix[y * self._cols + x2] == 'CIRCLE':
                    if pos != y * self._cols + x2 and val[0:-1] == self.value_at((x2, y))[0:-1]:
                        double_pos.append((x2, y))

            for y2 in range(self._rows):
                if self._user_matrix[y2 * self._cols + x] == 'CIRCLE':
                    if pos != y2 * self._cols + x and val[0:-1] == self.value_at((x, y2))[0:-1]:
                        double_pos.append((x, y2))

        return double_pos

    def circle_around_black(self):
        for y in range(self._rows):
            for x in range(self._cols):
                if self._user_matrix[y * (self._cols) + x] == 'BLACK':
                    cells_around = self.cells_around((x, y))
                    for cell in cells_around:
                        self.flag_at(cell)

    def black_double(self):
        for y in range(self._rows):
            for x in range(self._cols):
                double_pos = self.findDouble((x, y))
                if double_pos != []:
                    for cell in double_pos:
                        self.play_at(cell)

    def value_at(self, cell: (int, int)):
        x, y = cell
        if self._user_matrix[y * self._cols + x] == 'BLACK':
            return self._start_matrix[y * self._cols + x] + "#"
        elif self._user_matrix[y * self._cols + x] == 'CIRCLE':
            return self._start_matrix[y * self._cols + x] + "!"
        else:
            return self._start_matrix[y * (self._cols) + x]

    def play_at(self, cell: (int, int)):
        x, y = cell
        self._user_matrix[y * (self._cols) + x] = 'BLACK'

    def flag_at(self, cell: (int, int)):
        x, y = cell
        self._user_matrix[y * (self._cols) + x] = 'CIRCLE'

    def tip(self):
        isWhite = False
        first_case = ""
        second_case = ""
        for y in range(self._rows):
            for x in range(self._cols):
                matrix_copy = self._user_matrix[:]
                if self._user_matrix[y * self._cols + x] == 'CLEAR':
                    is_white = True
                    self.play_at((x, y))
                    self.circle_around_black()
                    self.black_double()
                    if self.wrong():
                        self.flag_at((x, y))
                        if self.wrong():
                            self._user_matrix = matrix_copy[:]
                    first_case = self._user_matrix[y * self._cols + x]

                    self._user_matrix = matrix_copy[:]

                    self.flag_at((x, y))
                    self.circle_around_black()
                    self.black_double()
                    if self.wrong():
                        self.play_at((x, y))
                        if self.wrong():
                            self._user_matrix = matrix_copy
                    second_case = self._user_matrix[y * self._cols + x]

                    self._user_matrix = matrix_copy[:]

                    if is_white:
                        if first_case == 'CIRCLE' and second_case == 'CIRCLE' :
                            self.flag_at((x, y))
                        elif first_case == 'BLACK' and second_case == 'BLACK':
                            self.play_at((x, y))
                        else:
                            self._user_matrix[y * self._cols + x] == 'CLEAR'
                        isWhite = False

    def wrong(self):
        for y in range(self._rows):
            for x in range(self._cols):
                if self._user_matrix[y * self._cols + x] == 'BLACK':
                    cells_around = self.cells_around((x, y))
                    for cell in cells_around:
                        x_c, y_c = cell
                        if self._user_matrix[y_c * self._cols + x_c] == 'BLACK':
                            return True

                double_pos = self.findDouble((x, y))
                if double_pos != []:
                    return True
        return False

    def finished(self):
        for y in range(self._rows):
            for x in range(self._cols):
                if self._user_matrix[y * self._cols + x] == 'CLEAR': return False
                if self._user_matrix[y * self._cols + x] == 'BLACK':
                    cells_around = self.cells_around((x, y))
                    for cell in cells_around:
                        x_c, y_c = cell
                        if self._user_matrix[y_c * self._cols + x_c] == 'BLACK':
                            return False

                double_pos = self.findDouble((x, y))
                if double_pos != []:
                    return False

        self.white_contiguous((0, 0))

        contiguous = True
        for y in range(self._rows):
            for x in range(self._cols):
                if self._user_matrix[y*self._cols + x]  == 'CIRCLE' and not self._white_matrix[y*self._cols + x]:
                    contiguous = False

        if not contiguous:
            self._white_matrix = [False for i in range(len(self._start_matrix))]

        return (True and contiguous)

    def white_contiguous(self, cell: (int, int)):
        x,y = cell
        if self._user_matrix[y * self._cols + x] == 'BLACK' and cell == (0, 0):
            x += 1
        if self._user_matrix[y * self._cols + x] == 'CIRCLE' and self._white_matrix[y * self._cols + x] == False:
            self._white_matrix[y * self._cols + x] = True
            for c in self.cells_around((x, y)):
                self.white_contiguous(c)

    def symbols(self, cell:(int,int)):
        x,y = cell
        if self._user_matrix[y * (self._cols) + x] == 'CIRCLE':
            if self._symbols_matrix[y * (self._cols) + x] < 18:
                self._symbols_matrix[y * (self._cols) + x] += 1
            return self._symbols_matrix[y * (self._cols) + x]
        else:
            self._symbols_matrix[y * (self._cols) + x] = 0
        return 0

    def cols(self):
        return self._cols

    def rows(self):
        return self._rows