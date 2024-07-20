"""
Unit tests for chessboard challenge
"""
__author__ = "Markus Juuti"


from chess_challenge import ChessBoard
from unittest import TestCase


class TTTUnit(TestCase):

    chess = None  # type: ChessBoard

    def setUp(self):
        self.chess = ChessBoard()
        self.chess.initialize_board()

    # region valid entries
    def test_enter_knight_valid_location(self):
        loc_chars = 'abcdefgh'
        with self.subTest():
            for i in loc_chars:
                for j in range(1,9):
                    assert self.chess.is_valid_input(f'knight {i}{j}')

    def test_enter_bishop_valid_location(self):
        loc_chars = 'abcdefgh'
        with self.subTest():
            for i in loc_chars:
                for j in range(1,9):
                    assert self.chess.is_valid_input(f'bishop {i}{j}')
    # endregion

    # region Invalid entries
    def test_invalid_input_piece(self):
        assert not self.chess.is_valid_input(f'king a4')

    def test_invalid_input_location(self):
        assert not self.chess.is_valid_input(f'bishop a9')

    def test_invalid_input_location_letter(self):
        assert not self.chess.is_valid_input(f'bishop i4')

    def test_invalid_input_location_no_num(self):
        assert not self.chess.is_valid_input(f'bishop c')

    def test_invalid_input_already_used(self):
        self.chess.board[0][0] = 'bK'
        assert not self.chess.is_valid_input(f'bishop a8')

    def test_invalid_input_already_16_blacks(self):
        for i in range(2):
            for j in range(8):
                self.chess.board[i][j] = 'bK'
        self.chess.board[4][4] = 'wH'
        self.chess.white_coordinates = (4,4)
        assert not self.chess.is_valid_input(f'bishop a6')
    # endregion

    # region Done
    def test_done_before_white(self):
        assert not self.chess.is_valid_input(f'done')

    def test_done_before_black(self):
        self.chess.board[0][0] = 'wK'
        self.chess.white_coordinates = (0,0)
        assert not self.chess.is_valid_input(f'done')

    def test_done_after_black(self):
        self.chess.board[0][0] = 'wK'
        self.chess.white_coordinates = (0,0)
        self.chess.board[0][1] = 'bK'
        assert self.chess.is_valid_input(f'done')

    def test_valid_done_already_16_blacks(self):
        for i in range(2):
            for j in range(8):
                self.chess.board[i][j] = 'bK'
        self.chess.board[4][4] = 'wH'
        self.chess.white_coordinates = (4,4)
        assert self.chess.is_valid_input(f'done')
    # endregion

    def test_knight_takeouts(self):
        self.chess.white_type = 'knight'
        self.chess.board[4][4] = 'wH'
        self.chess.white_coordinates = (4,4)

        self.chess.board[2][3] = 'bB'
        self.chess.board[2][5] = 'bB'
        self.chess.board[3][2] = 'bB'
        self.chess.board[3][6] = 'bB'
        self.chess.board[5][2] = 'bB'
        self.chess.board[5][6] = 'bB'
        self.chess.board[6][3] = 'bB'
        self.chess.board[6][5] = 'bB'

        assert len(self.chess.get_black_pieces_in_range()) == 8

    def test_knight_takeouts_with_extra(self):
        self.chess.white_type = 'knight'
        self.chess.board[4][4] = 'wH'
        self.chess.white_coordinates = (4,4)

        self.chess.board[2][3] = 'bB'
        self.chess.board[2][4] = 'bB'
        self.chess.board[2][5] = 'bB'
        self.chess.board[3][2] = 'bB'
        self.chess.board[3][3] = 'bB'
        self.chess.board[3][6] = 'bB'
        self.chess.board[5][2] = 'bB'
        self.chess.board[5][4] = 'bB'
        self.chess.board[5][6] = 'bB'
        self.chess.board[6][3] = 'bB'
        self.chess.board[6][4] = 'bB'
        self.chess.board[6][5] = 'bB'

        assert len(self.chess.get_black_pieces_in_range()) == 8

    def test_knight_takeouts_with_no_hits(self):
        self.chess.white_type = 'knight'
        self.chess.board[4][4] = 'wH'
        self.chess.white_coordinates = (4,4)

        self.chess.board[2][4] = 'bB'
        self.chess.board[3][3] = 'bB'
        self.chess.board[5][4] = 'bB'
        self.chess.board[6][4] = 'bB'

        assert len(self.chess.get_black_pieces_in_range()) == 0

    def test_bishop_takeouts(self):
        self.chess.white_type = 'bishop'
        self.chess.board[4][4] = 'wB'
        self.chess.white_coordinates = (4,4)

        self.chess.board[5][5] = 'bB'
        self.chess.board[3][3] = 'bB'
        self.chess.board[5][3] = 'bB'
        self.chess.board[3][5] = 'bB'

        assert len(self.chess.get_black_pieces_in_range()) == 4

    def test_bishop_takeouts_with_distance(self):
        self.chess.white_type = 'bishop'
        self.chess.board[4][4] = 'wB'
        self.chess.white_coordinates = (4,4)

        self.chess.board[6][6] = 'bB'
        self.chess.board[2][2] = 'bB'
        self.chess.board[2][6] = 'bB'
        self.chess.board[6][2] = 'bB'

        assert len(self.chess.get_black_pieces_in_range()) == 4

    def test_bishop_takeouts_with_obstacles(self):
        self.chess.white_type = 'bishop'
        self.chess.board[4][4] = 'wB'
        self.chess.white_coordinates = (4,4)

        # direct
        self.chess.board[5][5] = 'bB'
        self.chess.board[3][3] = 'bB'
        self.chess.board[5][3] = 'bB'
        self.chess.board[3][5] = 'bB'

        # behind
        self.chess.board[6][6] = 'bB'
        self.chess.board[2][2] = 'bB'
        self.chess.board[2][6] = 'bB'
        self.chess.board[6][2] = 'bB'

        in_range = self.chess.get_black_pieces_in_range()

        assert len(in_range) == 4
        assert not any([coord for coord in [(2,2), (2,6), (6,2), (6,6)] if coord in in_range])

