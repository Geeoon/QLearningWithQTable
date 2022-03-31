import random
import numpy as np

class Tile:
    def __init__(self, score:int, terminal:bool):
        self._score = score
        self._terminal = terminal

    def __init__(self):
        self.__init__(0, False)

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, s):
        self._score = s

    @property
    def terminal(self):
        return self._terminal

    @terminal.setter
    def terminal(self, t):
        self._terminal = t
    

class Board:
    def __init__(self, x, y):
        self._board = np.zeros(shape=(x, y), dtype=Tile)

    def set_tile(self, x, y, tile:Tile):
        self._board[x, y] = tile

    def get_tile(self, x, y):
        return self._board[x, y]

    def get_shape(self):
        return self._board.shape

    def get_actions(self, x, y):
        possible_actions = [1, 2, 3, 4]  # up, right, down, left
        if x == 0:
            possible_actions.remove(4)

        if y == 0:
            possible_actions.remove(1)

        if x == self._board.shape[0] - 1:
            possible_actions.remove(2)

        if y == self._board.shape[1] - 1:
            possible_actions.remove(3)

        return possible_actions


class QTable:
    def __init__(self, board:Board):
        self._table = np.zeros(shape=(board.get_shape()[0], board.get_shape()[1], 4), dtype=int)

    def get_state_action_value(self, x, y):
        return self._table[x, y]

    def set_state_action_value(self, x, y, val):
        self._table[x, y] = val


class Agent:
    def __init__(self, learning_rate:float, discount_factor:float, board:Board):
        self._learning_rate = learning_rate
        self._discount_factor = discount_factor
        self._board = board
        self._qtable = QTable(board)
        self._position = np.zeros(shape=(2), dtype=int)

    def update(self):
        if random.random() < self._learning_rate:  # explore
            print(self._board.get_actions(self._position[0], self._position[1]))

    def episode(self):
        actual_return = 0.0


if __name__ == "__main__":
    board = Board(5, 5)
    agent = Agent(1, 1.0, board)
    agent.update()