import copy
import random
import numpy as np
from termcolor import colored
from abc import ABC, abstractmethod

# Board


class GameBoard:
    MARKERS = ['X', 'O']

    def __init__(self, board_size=10, defeat_length=5):
        self.board_size = board_size
        self.defeat_length = defeat_length
        self.board_list = [[' ' for _i in range(self.board_size)] for _k in range(self.board_size)]
        self.players = []
        self.current_player = None
        self.occupied_count = 0

    @staticmethod
    def create_players(marker):
        # Создает игроков в соответствии с маркером, который
        # был выбран первым игроком.
        # Второй игрок получает оставшийся маркер.
        # Возвращает обоих игроков.

        first_player = HumanPlayer(marker)
        if marker == 'X':
            second_player = AIPlayer('O')
        else:
            second_player = AIPlayer('X')
        return [first_player, second_player]

    @staticmethod
    def split_line(line, index):
        after_line = line[index:]
        before_line = line[:index]
        before_line.reverse()
        return after_line, before_line

    @staticmethod
    def count_consecutive_markers(line, marker):
        count = 0
        for element in line:
            if element == marker:
                count += 1
            else:
                return count
        return count

    @staticmethod
    def get_diagonal_offset(row, column, size, main_diagonal):
        if main_diagonal:
            return column - row
        else:
            return size - 1 - row - column

    def draw_board(self, row=0, column=0):
        # Рисует игровое поле

        field = f'    {"   ".join(list(map(str, (range(self.board_size)))))}'
        for index, line in enumerate(self.board_list):
            if index == row:
                field += f'\n{index} | '
                for col_i in range(len(line)):
                    if col_i == column:
                        field += colored(f'{line[col_i]}', 'red')
                    else:
                        field += f'{line[col_i]}'
                    field += ' | '
            else:
                field += f'\n{index} | {" | ".join(line)} |'
        return field

    def start_game(self):
        self.players = self.create_players(self.choose_marker())
        self.current_player = self.choose_first_player()

    def choose_marker(self):
        # Позволяет игроку выбрать маркер: X или O. Возвращает этот маркер.

        marker = input('Do you want to play for X or for O? ').strip().upper()
        if marker == '0':
            marker = 'O'
        elif marker not in self.MARKERS:
            print('Enter X or O')
            return self.choose_marker()
        return marker

    def choose_first_player(self):
        # Случайным образом выбирается, кто играет первым: X или O.
        # Возвращает этого игрока.

        player = random.choice(self.players)
        print(f'{player} player goes first')
        return player

    def play_round(self, row, column):
        # Позволяет игроку разместить свой маркер, увеличивает количество занятых ячеек,
        # выводит игровое поле на экран, проверяет, закончена ли игра, и меняет текущего игрока на следующего.
        # Возвращает True если игра должна продолжаться. Иначе, возвращает False.

        self.current_player.place_marker(self, row, column)
        self.occupied_count += 1

        print(self.draw_board(row, column))

        if self.is_game_finished(row, column):
            return False

        self.current_player = self.get_other_player(self.current_player)
        return True

    def get_cell_axes(self, row, column, marker):
        board_list_copy = copy.deepcopy(self.board_list)
        board_list_copy[row][column] = marker

        horizontal = board_list_copy[row][0:self.board_size]
        vertical = [board_list_copy[x][column] for x in range(0, self.board_size)]

        offset = self.get_diagonal_offset(row, column, self.board_size, main_diagonal=True)
        main_diagonal = list(np.diag(board_list_copy, offset))

        offset = self.get_diagonal_offset(row, column, self.board_size, main_diagonal=False)
        flip_board_list = np.fliplr(board_list_copy)
        side_diagonal = list(np.diag(flip_board_list, offset))

        return horizontal, vertical, main_diagonal, side_diagonal

    def max_sequence_cell(self, row, column, marker):
        h, v, main_diag, side_diag = self.get_cell_axes(row, column, marker)
        max_h = self.max_sequence_line(h, row, column, marker, 'h')
        max_v = self.max_sequence_line(v, row, column, marker, 'v')
        max_main_diag = self.max_sequence_line(main_diag, row, column, marker, 'md')
        max_side_diag = self.max_sequence_line(side_diag, row, column, marker, 'sd')
        return max(max_h, max_v, max_main_diag, max_side_diag)

    def max_sequence_line(self, line, row, column, marker, line_type):
        if line_type == 'h':
            after_line, before_line = self.split_line(line, column)
        elif line_type == 'v':
            after_line, before_line = self.split_line(line, row)
        elif line_type == 'sd':
            offset = self.get_diagonal_offset(row, column, self.board_size, main_diagonal=False)
            after_line, before_line = self.split_line(line, row if offset >= 0 else row + offset)
        elif line_type == 'md':
            offset = self.get_diagonal_offset(row, column, self.board_size, main_diagonal=True)
            after_line, before_line = self.split_line(line, row if offset >= 0 else column)
        return self.count_consecutive_markers(after_line, marker) + self.count_consecutive_markers(before_line, marker)

    def is_current_player_won(self, row, column):
        # Возвращает значение True, если настольная игра выиграна.
        # В противном случае возвращает значение False.

        if self.max_sequence_cell(row, column, self.current_player.marker) >= self.defeat_length:
            return True
        return False

    def is_game_finished(self, row, column):
        # Возвращает значение True, если один из игроков выиграл или доска заполнена.
        # В противном случае возвращает значение False.

        if self.is_current_player_won(row, column):
            print(f'{self.get_other_player(self.current_player)} won!')
            return True
        elif self.is_board_full():
            print('Draw')
            return True
        return False

    def is_board_full(self):
        # Возвращает значение True, если на доске нет свободных ячеек.
        # В противном случае возвращает значение False."""

        return self.occupied_count == self.board_size ** 2

    def is_cell_available(self, row, column):
        # Возвращает значение True, если доступна ячейка с координатами строки, столбца.
        # В противном случае возвращает значение False.

        return self.board_list[row][column] not in self.MARKERS

    def is_cell_in_bounds(self, coord):
        return 0 <= coord < self.board_size

    def get_other_player(self, current_player):
        # Возвращает следующего игрока, который должен сделать ход.

        players_copy = self.players.copy()
        players_copy.remove(current_player)
        return players_copy[0]

# Gamers


class AbstractPlayer(ABC):
    def __init__(self, marker):
        self.marker = marker

    def __str__(self):
        return self.marker

    @abstractmethod
    def select_cell(self, board):
        pass

    def place_marker(self, board, row, column):
        board.board_list[row][column] = self.marker


class HumanPlayer(AbstractPlayer):
    def select_cell(self, board):
        # Просит пользователя ввести координаты для перемещения.
        # Если входные данные верны (координаты находятся в диапазоне размеров платы
        # и ячейка пуста) возвращает полученные координаты.
        # В противном случае попросит пользователя снова ввести координаты.

        position = (input(f'Player {self.marker}, choose cell coordinates in a format x y: ')).split(' ')
        try:
            row, column = map(int, position)
        except ValueError:
            print(f'Invalid Input. Enter coordinates from 0 to {board.board_size - 1}')
            return self.select_cell(board)
        if not (board.is_cell_in_bounds(row) and board.is_cell_in_bounds(column)):
            print(f'Enter coordinates from 0 to {board.board_size - 1}')
            return self.select_cell(board)
        elif not board.is_cell_available(row, column):
            print('This cell is not empty. Choose coordinates of another cell.')
            return self.select_cell(board)
        return row, column


class AIPlayer(AbstractPlayer):
    def select_cell(self, board):
        available_cells = self.calculate_cells_scores(board, self.marker)
        available_cells.sort(key=lambda cell: (cell[1], cell[2]))
        row, column = available_cells[0][0]
        return row, column

    def calculate_cells_scores(self, board, marker):
        cell_scores = []
        for row in range(board.board_size):
            for column in range(board.board_size):
                if board.board_list[row][column] == ' ':
                    max_seq_ai = board.max_sequence_cell(row, column, marker)
                    max_seq_player = board.max_sequence_cell(row, column, board.get_other_player(self).marker)
                    cell_scores.append(((row, column), max_seq_ai, max_seq_player))
        return cell_scores
