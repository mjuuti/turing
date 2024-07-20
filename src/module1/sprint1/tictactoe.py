"""
tic-tac-toe implementation with python

:author: @mjuuti
"""
import random
import sys
from argparse import ArgumentParser
from datetime import datetime
from logging import getLogger

log = getLogger('TicTacToe')


def get_arguments():
    """
    Command-line argument parser for the program. Just to allow 2-player mode and larger boards,
    as well as unit tests
    :return:
    """
    parser = ArgumentParser('TicTacToe')
    parser.add_argument('--size', type=int, help='Game grid width', default=3)
    parser.add_argument('--players', type=int, help='Number of players (1 or 2)',
                        default=1, nargs='?', const=1, choices=[1, 2])
    parser.add_argument('--dumb', action="store_false", dest='smart', help="AI will play smarter. Max grid size 3x3")
    return parser.parse_known_args()[0]


class TicTacToe:

    _grid_width = None  # type: int
    marker_places = None  # type: list
    terminated = False
    winner = None  # type: str
    players = None  # type: int
    _board_template = None  # type: str
    placeholder = ' '
    ai_max_grid = 8

    def __init__(self):
        args = get_arguments()
        self.players = args.players
        self.grid_width = args.size
        self.reset_board()

    # region Properties
    @property
    def grid_width(self):
        return self._grid_width

    @grid_width.setter
    def grid_width(self, value: int):
        """
        Grid width setter with input validation
        :param value: integer value for grid width (and height)
        :return: None
        """
        if value < 3 or value > 15:
            print("Grid size must be between 3 and 15")
            sys.exit(1)
        self._grid_width = value
    # endregion

    # region High level methods
    def main(self):
        """
        Main function for the game, iterating required high level game actions turn by turn
        for both players
        :return: None
        """
        turn = 0
        while not self.terminated:
            self.draw_board()
            self.check_game_end_condition()
            if self.terminated:
                break
            self.get_player_move(1 + turn % 2)
            turn += 1

    def reset_board(self):
        """
        Reset game board to initial state
        :return: None
        """
        self.marker_places = list()
        self.terminated = False
        for _ in range(self.grid_width):
            self.marker_places.append([" "] * self.grid_width)

    def draw_board(self):
        """
        Draw game board with current state to console out
        :return: None
        """
        if self.terminated:
            return
        print(self._draw_board_impl())

    def check_game_end_condition(self):
        """
        Check if game has ended on either player's win or to stalemate
        :return:
        """
        if self.terminated:
            return

        if self._check_win_condition_impl():
            print(f"\nGame Over - {self.winner} wins!")
            self.terminated = True

        elif self._is_table_full():
            print("\nGame Over - Stalemate")
            self.terminated = True

    def get_player_move(self, player_num: int):
        """
        Get move from the player in turn
        :param player_num: number of player
        :return:
        """
        if player_num == 2 and self.players == 1:
            search_start = datetime.now()
            coord = self._get_ai_move()
            duration = datetime.now() - search_start
            print(f'AI move: {coord} ({duration.total_seconds()}s)')
        else:
            coord = self._get_coordinates(player_num)

        self._enter_move(coord, 'X' if player_num == 1 else 'O')
    # endregion

    # region graphics
    def _get_board_template(self):
        """
        Getter for board template to prevent it being created every time before filling
        :return:
        """
        if self._board_template is None:
            board_lines = list()

            # print board ascii string with cells filled with coordinates and with +--+--+ border
            border = f'{"+--" * self.grid_width}+'
            board_lines.append(border)
            for xn in range(self.grid_width):
                xline = str()
                for yn in range(self.grid_width):
                    xline += f'|{xn}{yn}'
                board_lines.append(xline + '|')
                board_lines.append(border)
            self._board_template = '\n'.join(board_lines)
        return self._board_template

    def _draw_board_impl(self):
        """
        Implementation of board graphics builder
        :return: String representing the game board state
        """
        board = self._get_board_template()
        for x in range(self.grid_width):
            for y in range(self.grid_width):
                board = board.replace(
                    f'|{x}{y}|',
                    f'| {self.marker_places[x][y]}|')
        return board
    # endregion

    # region Game results
    def _check_win_condition_impl(self, player: str = None) -> bool:
        """
        Check if either player has claimed any row, any column or either diagonal
        :return: boolean if game has finished to a win
        """
        if player:
            player = player.upper()
        for n in range(self.grid_width):
            # x-axis
            row = self.marker_places[n]
            log.debug(f'row {n}: {row}')
            if self._is_same_value(row):
                if not player:
                    self.winner = row[0]
                    return True
                return row[0] == player

            # y-axis
            column = list(zip(*self.marker_places))[n]
            log.debug(f'column {n}: {column}')
            if self._is_same_value(column):
                if not player:
                    self.winner = column[0]
                    return True
                return column[0] == player

        # diagonals
        down_diagonal = [self.marker_places[n][n] for n in range(self.grid_width)]
        log.debug(f'down diag: {down_diagonal}')
        if self._is_same_value(down_diagonal):
            if not player:
                self.winner = self.marker_places[0][0]
                return True
            return self.marker_places[0][0] == player

        up_diagonal = [list(zip(*self.marker_places))[::-1][n][n] for n in range(self.grid_width)]
        log.debug(f'up diag: {up_diagonal}')
        if self._is_same_value(up_diagonal):
            if not player:
                self.winner = list(zip(*self.marker_places))[::-1][0][0]
                return True
            return list(zip(*self.marker_places))[::-1][0][0] == player

        return False

    # region player moves
    def _enter_move(self, coordinates: list, character: str):
        """
        Enter move by the player to the board
        :param coordinates: list of integers represeting board coordinates
        :param character: player's marker (X or O)
        :return: None
        """
        self.marker_places[coordinates[0]][coordinates[1]] = character

    def _get_coordinates(self, player_num: int) -> list:
        """
        Get allowed coordinates for turn entry
        :param player_num: player's number
        :return: List of integers representing allowed coordinates entry
        """
        while True:
            coordinates = self._get_parsed_coordinates(player_num)
            if self._is_allowed_move(coordinates):
                break
            print("Unalloyed move, please try again")
        return coordinates

    @staticmethod
    def _get_parsed_coordinates(player_num: int) -> list:
        """
        Get validated integer coordinates from player input, or terminate if player
        wants to quit
        :param player_num: number of player in turn
        :return: list of integers representing coordinates on board
        """

        while True:
            player_input = input(f"Player {player_num} move: ")
            coordinates = [coord.strip() for coord in player_input.split(',')]
            try:
                if len(coordinates) != 2:
                    raise ValueError("need to have 2 coordinates")
                return [int(coord) for coord in coordinates]

            except ValueError:
                if coordinates[0].lower() in ['quit', 'exit']:
                    print("Thank you for playing Wing Commander")
                    sys.exit(0)

                print('Enter move as comma-separated numbers like "1,1" or "exit" to quit')
    # endregion

    # region AI logic
    def _get_random_coordinates(self):
        return [random.randint(0, self.grid_width - 1), random.randint(0, self.grid_width - 1)]

    def _get_ai_move(self):
        """
        Artificial intelligence logic, verified silently to be allowed on the board
        :return: list of integers representing coordinates
        """
        attempts = 0
        while True:
            if attempts > 5000:
                raise OverflowError("AI did not find coordinates with 5000 attempts")
            attempts += 1
            if get_arguments().smart:
                coords = self._get_best_move_coordinates()
            else:
                coords = self._get_random_coordinates()
            if self._is_allowed_move(coords, True):
                return coords

    def _minimax_algo_score(self, depth: int, ai_turn: bool) -> float:
        """
        Return best score current move would yield down the line using minimax algorith
        :param depth: current depth
        :param ai_turn: is AI in turn or not
        :return: best score as float
        """
        if self._check_win_condition_impl('X'):
            return float(-100/depth)
        elif self._check_win_condition_impl('O'):
            return float(100/depth)
        elif self._is_table_full():
            return 0
        elif depth > 6:
            return 0

        # change turn for next round
        ai_turn = not ai_turn
        scores = self._minimax_search_impl(depth, ai_turn)
        best_score = self._get_best_score_move_from_array(scores, ai_turn)[0]
        return best_score

    def _minimax_search_impl(self, depth: int, ai_turn: bool) -> list:
        scores = list()
        for n in range(self.grid_width):
            for m in range(self.grid_width):
                if self._is_allowed_move([n, m]):
                    self.marker_places[n][m] = 'O' if ai_turn else 'X'
                    ai_score = self._minimax_algo_score(depth + 1, ai_turn)
                    self.marker_places[n][m] = self.placeholder
                    scores.append((ai_score, (n, m)))
        return scores

    def _get_best_move_coordinates(self):
        """
        Get best coordinates to
        :return:
        """
        scores = self._minimax_search_impl(1, True)
        score, move = self._get_best_score_move_from_array(scores, True)
        print(f'Best move: {move} with score {score}')
        return move

    @staticmethod
    def _get_best_score_move_from_array(scores: list, ai_turn: bool) -> list:
        score_selector = max if ai_turn else min
        max_score = score_selector([score[0] for score in scores])
        rv = random.choice([score for score in scores if score[0] == max_score])
        return rv

    # endregion

    # region validation methods
    @staticmethod
    def _is_same_value(line_values: list, allow_empty: bool = False) -> bool:
        """
        Method to check if all elements in a given list are equal
        :param line_values: list of values
        :param allow_empty: boolean if empty values count
        :return: boolean if values are the same
        """
        if not allow_empty and any(not value.strip() for value in line_values):
            return False

        return all([line_values[n] == line_values[n - 1]
                    for n in range(1, len(line_values))])

    def _is_table_full(self) -> bool:
        """
        Check if all places on board have been used without either player winning,
        making game ending with stalemate result
        :return: boolean of stalemate condition
        """
        # flatten table and check if any empty cells are left
        all_cells = []
        [all_cells.extend(el) for el in self.marker_places]
        return not any(cell.strip() == '' for cell in all_cells)

    def _is_allowed_move(self, coords: list, quiet: bool = False) -> bool:
        """
        Check if given coordinates are on the board and are available for player's move
        :param coords: list of integers
        :param quiet: boolean if no error message should be displayed
        :return: boolean if move is allowed
        """
        if all(coords[n] in range(self.grid_width) for n in range(2)):
            return self.marker_places[coords[0]][coords[1]].strip() == ''
        if not quiet:
            print("Entered move outside coordinates")
        return False
    # endregion


if __name__ == '__main__':
    ttt_game = TicTacToe()
    ttt_game.main()
