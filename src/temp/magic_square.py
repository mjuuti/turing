

class Square:

    board = [[0,0,0]] * 3

    def __init__(self, lines: list):
        self.board = lines

    @property
    def max_line(self):
        return max([sum(line) for line in self.board])

    @property
    def max_column(self):
        return max([sum(line) for line in zip(self.board)])

    @property
    def max_diagonal(self):
        dd = sum([self.board[x][x] for x in range(3)])
        du = sum([self.board[x][2-x] for x in range(3)])

        if dd > du:
            return dd
        return du
