# region unit tests
from tictactoe import TicTacToe
from unittest import TestCase
from math import ceil


class TTTUnit(TestCase):

    game_instance = None  # type: TicTacToe

    def setUp(self):
        self.game_instance = TicTacToe()
        self.game_instance.grid_width = 3  # change here for larger boards
        self.game_instance.reset_board()

    # region Win conditions
    def test_row_winning_condition(self):
        for m in range(self.game_instance.grid_width):
            self.game_instance.marker_places[0][m] = "x"
        assert self.game_instance._check_win_condition_impl(), 'Game should end in win condition on row 0'

    def test_column_winning_condition(self):
        for n in range(self.game_instance.grid_width):
            self.game_instance.marker_places[n][0] = "y"
        assert self.game_instance._check_win_condition_impl(), 'Game should end in win condition on column 0'

    def test_diagonal_down_winning_condition(self):
        for n in range(self.game_instance.grid_width):
            self.game_instance.marker_places[n][n] = "d"
        assert self.game_instance._check_win_condition_impl(), 'Game should end in win condition on diagonal down line'

    def test_diagonal_up_winning_condition(self):
        for n in range(self.game_instance.grid_width):
            self.game_instance.marker_places[n][self.game_instance.grid_width - (n + 1)] = "u"
        assert self.game_instance._check_win_condition_impl(), 'Game should end in win condition on diagonal up line'
    # endregion

    # region no win conditions
    def test_row_no_winning_condition(self):
        for m in range(self.game_instance.grid_width - 1):
            self.game_instance.marker_places[0][m] = "x"
        assert not self.game_instance._check_win_condition_impl(), 'Game should not end in win condition on row 0'

    def test_column_no_winning_condition(self):
        for n in range(self.game_instance.grid_width - 1):
            self.game_instance.marker_places[n][0] = "y"
        assert not self.game_instance._check_win_condition_impl(), 'Game should not end in win condition on column 0'

    def test_diagonal_down_no_winning_condition(self):
        for n in range(self.game_instance.grid_width - 1):
            self.game_instance.marker_places[n][n] = "d"
        assert not self.game_instance._check_win_condition_impl(), \
            'Game should not end in win condition on diagonal down line'

    def test_diagonal_up_no_winning_condition(self):
        for n in range(self.game_instance.grid_width - 1):
            self.game_instance.marker_places[n][self.game_instance.grid_width - (n + 1)] = "u"
        assert not self.game_instance._check_win_condition_impl(), \
            'Game should not end in win condition on diagonal up line'
    # endregion

    # region Stalemate
    def test_stalemate_result(self):
        # fill board with half (rounded up) and half markers every second line so that
        # board is full but without winning condition on any > 2x2 board
        for xcoord in range(self.game_instance.grid_width):
            first = 'n' if xcoord % 2 == 0 else 'm'
            second = 'n' if first == 'm' else 'm'

            halfway = ceil(float(self.game_instance.grid_width) / 2)
            for ycoord in range(halfway):
                self.game_instance.marker_places[xcoord][ycoord] = first
            for ycoord in range(halfway, self.game_instance.grid_width):
                self.game_instance.marker_places[xcoord][ycoord] = second

        assert self.game_instance._is_table_full() and not self.game_instance._check_win_condition_impl(), \
            'Game should not end in win condition on a full stalemate table'
    # endregion

    # region AI
    def test_ai_move_empty_table(self):
        ai_move = self.game_instance._get_ai_move()
        assert ai_move[0].is_integer() and ai_move[1].is_integer(), 'AI should give valid coordinates'
    # endregion

    # region Graphics
    def test_get_empty_table_graphics(self):
        board = self.game_instance._draw_board_impl()
        board_expected_row_length = self.game_instance.grid_width * 3 + 1
        board_expected_row_count = self.game_instance.grid_width * 2 + 1
        board_lines = board.split('\n')
        board_row_length = len(board_lines[0])
        assert board_expected_row_length == board_row_length \
                and board_expected_row_count == len(board_lines), \
            (
                f'Expected board to have {board_expected_row_length} long rows '
                f'and {board_expected_row_count} rows in total, '
                f'but got {board_row_length} and {len(board_lines)}'
            )

    def test_get_filled_table_graphics(self):
        board = self.game_instance._draw_board_impl()

        for n in range(self.game_instance.grid_width):
            for m in range(self.game_instance.grid_width):
                self.game_instance.marker_places[n][m] = "G"

        board_expected_row_length = self.game_instance.grid_width * 3 + 1
        board_expected_row_count = self.game_instance.grid_width * 2 + 1
        board_lines = board.split('\n')
        board_row_length = len(board_lines[0])
        assert board_expected_row_length == board_row_length \
                and board_expected_row_count == len(board_lines), \
            (
                f'Expected board to have {board_expected_row_length} long rows '
                f'and {board_expected_row_count} rows in total, '
                f'but got {board_row_length} and {len(board_lines)}'
            )

    # endregion