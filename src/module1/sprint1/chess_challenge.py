"""
Turing College DS M1, S1 Chess challenge

:author: @mjuuti
"""
import math
import random

EMPTY = '  '
VERTICAL = '87654321'
HORIZONTAL = 'abcdefgh'
PIECES = {
    'bishop': 'bishop',
    'king': 'king',
    'knight': 'horse',  # set alias to horse so we could actually use king as well
    'pawn': 'pawn',
}
ALLOWED_PIECES = ['knight', 'bishop']


def printf(message: str):
    """
    Helper function to print with border above and below text to make output more readable
    :param message: message to print
    :return: None
    """
    border = '-' * len(message)
    print(border)
    print(message)
    print(border)


class ChessBoard:
    """
    Class for chess, holding data of pieces on the board
    """

    board = None  # type: list
    white_coordinates = None  # type: tuple
    white_type = None  # type: str

    def __init__(self):
        self.initialize_board()

    def main(self):
        """
        Main method run by module if run directly
        :return: None
        """
        # white input
        while True:
            self.print_board()
            white_input = input("White piece and location: ")
            if not self.is_valid_input(white_input):
                continue

            piece, location = self.get_input_params(white_input)
            self.add_piece_to_board(piece, location, 'w')
            break

        # black input
        while True:
            self.print_board()
            black_input = input("Black piece and location: ")
            if not self.is_valid_input(black_input):
                continue
            if black_input.lower() == 'done':
                break
            piece, location = self.get_input_params(black_input)
            self.add_piece_to_board(piece, location, 'b')

            # user-friendly addition would be
            # if self.black_count == 16:
            #     break

        self.show_pieces_white_can_take()

    @property
    def white_count(self) -> int:
        """
        Property for count of white pieces on table
        :return: number of whites
        """
        return self.get_piece_count('w')

    @property
    def black_count(self):
        """
        Property for count of black pieces on table
        :return: number of blacks
        """
        return self.get_piece_count('b')

    def add_piece_to_board(self, piece: str, location: str, side: str):
        """
        Helper method to add pieces on board
        :param piece: name of the piece
        :param location: location of piece (like a3 or f6)
        :param side: player side (white or black)
        :return: None
        """
        x, y = self.get_coordinates_from_location(location)
        if side == 'w':
            self.white_coordinates = (x, y)
            self.white_type = piece

        self.board[x][y] = self.get_piece_abbreviation(piece, side)

    def get_black_pieces_in_range(self):
        """
        Getter for black pieces in hero piece's range
        :return: list of coordinates
        """
        in_range = list()
        for x, y in self.get_pieces('b'):
            if self.is_valid_move(x, y):
                in_range.append((x, y))
        return in_range

    def show_pieces_white_can_take(self):
        """
        Helper method to print out all pieces our white hero piece can take, and show board with only hits after
        :return:
        """
        print('')
        in_range = self.get_black_pieces_in_range()

        for x, y in in_range:
            abbrev = self.board[x][y]
            side, piece = self.get_side_and_piece_from_abbreviation(abbrev)
            location = self.get_location_from_coordinates(x, y)

            print(
                f'{piece.capitalize()} in {location} can be taken out '
                f'by our {self.white_type.capitalize()} hero'
            )

        if not in_range:
            white_loc = self.get_location_from_coordinates(*self.white_coordinates)
            print(
                f'No pieces can be taken out '
                f'by our {self.white_type.capitalize()} hero from location {white_loc}'
            )

        # show board with only relevant pieces
        print('')
        in_range.append(self.white_coordinates)
        for x in range(8):
            for y in range(8):
                if (x, y) in in_range:
                    continue
                self.board[x][y] = EMPTY
        self.print_board()

    def get_pieces(self, prefix: str = "b"):
        """
        Get coordinates of all pieces on the board
        :param prefix: show only if abbreviation is prefixed with this string, typically 'w' or 'b'
        :return: List of coordinates
        """
        coordinates = list()
        for x in range(8):
            for y in range(8):
                if self.board[x][y].startswith(prefix):
                    coordinates.append((x, y))
        return coordinates

    def get_piece_count(self, prefix: str = '') -> int:
        """
        Get total number of pieces on board
        :param prefix: Filter to include pieces with abbreviation prefix only
        :return: Number of pieces mathing the filter
        """
        temp = list()
        [temp.extend(loc) for loc in self.board]
        return len([loc for loc in temp if loc.strip().startswith(prefix)])

    def initialize_board(self):
        """
        Set up new fresh board
        :return:
        """
        self.board = list()
        for _ in range(8):
            self.board.append([EMPTY] * 8)

    def is_valid_input(self, user_input: str) -> bool:
        """
        Validate user input to match '{piece} {location}' format
        :param user_input: entry from user input
        :return: True if input is valid
        """
        if user_input.lower() == 'done':
            if not self.white_coordinates:
                printf("White piece and at least 1 black piece must be added before done")
                return False

            if not self.black_count > 0:
                printf("At least 1 black piece must be added")
                return False
            return True

        if self.black_count == 16:
            printf("Maximum 16 black pieces can be added. Type 'done' to finish")
            return False

        piece, location = self.get_input_params(user_input)
        if not piece or piece not in ALLOWED_PIECES:
            return False
        x, y = self.get_coordinates_from_location(location)
        if not self.is_free(x, y):
            printf(f"Location {location} is already taken")
            return False

        return True

    @staticmethod
    def get_side_and_piece_from_abbreviation(abbreviation: str):
        """
        Helper to convert abbreviations like bB to Black,bishop tuple
        :param abbreviation: abbreviation to convert from
        :return: tuple of side,piece
        """
        side = 'Black' if abbreviation.startswith('b') else 'White'
        for name, alias in PIECES.items():
            if alias.startswith(abbreviation[1].lower()):
                return side, name

    @staticmethod
    def get_piece_abbreviation(piece: str, side: str) -> str:
        """
        Helper to convert piece and side to abbreviation to put on the board
        :param piece: name of piece
        :param side: black or white
        :return: abbreviation in lowercase side, uppercase piece style like bB or wH
        """
        if piece.lower() == "knight":
            piece = "horse"
        return f'{side}{piece.upper()[0]}'

    def get_input_params(self, user_input: str):
        """
        Convert user input to a tuple. If input is invalid, return False, False
        :param user_input: entry from user input
        :return: tuple(piece, location)
        """
        try:
            piece, location = user_input.split(' ')
            if not self.is_valid_location(location):
                printf("Location must be given as letter A-H followed by number 1-8")
                return False, False
            if piece not in ALLOWED_PIECES:
                printf(f"Unallowed piece. Allowed pieces are {", ".join(ALLOWED_PIECES)}")

            return piece, location

        except ValueError:
            printf(f'Input must be in format "piece location" '
                  f'like "{random.choice(ALLOWED_PIECES)} a4".')
            return False, False

    @staticmethod
    def get_distance(start: tuple, end: tuple) -> float:
        """
        Get Pythagorean distance between two coordinates
        :param start: tuple(x,y)
        :param end: tuple(x,y)
        :return: distance as float
        """
        return math.sqrt(math.pow(abs(start[0] - end[0]), 2) +
                         math.pow(abs(start[1] - end[1]), 2))

    def is_valid_move(self, x: int, y: int):
        """
        Is move to given coordinates valid move for our hero piece, including obstacles
        :param x: x-coordinate
        :param y: y-coordinate
        :return: boolean if hero can reach this destination following chess rules
        """
        if self.white_type == 'knight':
            if abs(self.white_coordinates[0] - x) > 2 or abs(self.white_coordinates[1] - y) > 2:
                return False

            if self.get_distance(self.white_coordinates, (x, y)) != math.sqrt(5):
                return False

            return True

        if self.white_type == 'king':
            return self.get_distance(self.white_coordinates, (x, y)) <= math.sqrt(2)

        if self.white_type == 'bishop':
            wx, wy = self.white_coordinates  # makes code a bit more readable
            if abs(x - wx) != abs(y - wy):
                return False

            # Check if route to the target is obstructed by any other piece
            xc = -1 if x - wx < 0 else 1
            yc = -1 if y - wy < 0 else 1
            tx, ty = wx, wy  # temp location coordinates
            while True:
                tx += xc
                ty += yc
                if (tx, ty) == (x, y):
                    return True
                if self.board[tx][ty] != EMPTY:
                    return False

    @staticmethod
    def is_valid_location(location: str):
        """
        Validate location is on board on [a-h][1-8] format
        :param location: location string
        :return: boolean if location is valid
        """
        location = location.lower()
        return len(location) == 2 and location[0] in HORIZONTAL and location[1] in VERTICAL

    @staticmethod
    def is_valid_coordinate(x: int, y: int) -> bool:
        return x in range(8) and y in range(8)

    def is_free(self, x: int, y: int) -> bool:
        """
        Check if coordinates are already taken
        :param x:
        :param y:
        :return: True if no piece is on given coordinates
        """
        return self.board[x][y] == EMPTY

    def get_coordinates_from_location(self, location: str):
        """
        Convert [a-h][1-9] location to coordinates
        :param location: location string
        :return: tuple of coordinates
        """
        location = location.lower()
        x = VERTICAL.index(location[1])
        y = HORIZONTAL.index(location[0])
        return x, y

    def get_location_from_coordinates(self, x: int, y: int) -> str:
        """
        Get chess-y location string from coordinates
        :param x:
        :param y:
        :return: string representing chess location like a5 or f8
        """
        return f'{HORIZONTAL[x]}{VERTICAL[y]}'

    def print_board(self):
        """
        Print board to the console with abbreviated piece names and sides shown
        :return:
        """
        board_lines = list()
        # print board ascii string with cells filled with coordinates and with +--+--+ border
        board_lines.append('  A  B  C  D  E  F  G  H')
        border = f' {"+--" * 8}+'
        board_lines.append(border)
        for xn in range(8):
            xline = str(8 - xn)
            for yn in range(8):
                xline += f'|{self.board[xn][yn]}'
            board_lines.append(xline + '|')
            board_lines.append(border)
        print("\n".join(board_lines))


if __name__ == '__main__':
    cb = ChessBoard()
    cb.main()
