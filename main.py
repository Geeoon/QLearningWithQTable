import random
import numpy as np

class Tile:
    def __init__(self, score:int, terminal:bool):
        self._score = score
        self._terminal = terminal

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
    def __init__(self, x:int, y:int):
        self._board = np.zeros(shape=(x, y), dtype=Tile)
        self._board.fill(Tile(0, False))

    def set_tile(self, x:int, y:int, tile:Tile):
        self._board[x, y] = tile

    def get_tile(self, x:int, y:int):
        return self._board[x, y]

    def get_shape(self):
        return self._board.shape

    def get_actions(self, x:int, y:int):
        possible_actions = [0, 1, 2, 3]  # up, right, down, left
        if x == 0:
            possible_actions.remove(3)

        if y == 0:
            possible_actions.remove(0)

        if x == self._board.shape[0] - 1:
            possible_actions.remove(1)

        if y == self._board.shape[1] - 1:
            possible_actions.remove(2)

        return possible_actions


class QTable:
    def __init__(self, board:Board):
        self._table = np.zeros(shape=(board.get_shape()[0], board.get_shape()[1], 4), dtype=int)

    def get_state_action_values(self, x:int, y:int):
        return self._table[x, y]

    def set_state_action_value(self, x:int, y:int, action:int, val:float):
        self._table[x, y, action] = val

    def get_max_state_action_value_actions(self, x:int, y:int):
        print(np.argwhere(self.get_state_action_values(x, y) == np.amax(self.get_state_action_values(x, y))).flatten())
        return np.argwhere(self.get_state_action_values(x, y) == np.amax(self.get_state_action_values(x, y))).flatten()


class Agent:
    def __init__(self, learning_rate:float, discount_factor:float, board:Board):
        self._learning_rate = learning_rate
        self._discount_factor = discount_factor
        self._board = board
        self._qtable = QTable(board)
        self._position = np.zeros(shape=(2), dtype=int)

    def __str__(self):
        output = ""
        for y in range(0, self._board.get_shape()[1]):
            for x in range(0, self._board.get_shape()[0]):
                if y == self._position[1] and x == self._position[0]:
                    output += "██"
                else:
                    output += "[]"
            output += "\n"
        return output

    def move(self, dir:int):
        if dir == 0:
            self._position[1] = self._position[1] - 1
        elif dir == 1:
            self._position[0] = self._position[0] + 1
        elif dir == 2:
            self._position[1] = self._position[1] + 1
        elif dir == 3:
            self._position[0] = self._position[0] - 1

    def update(self):
        possible_actions = self._board.get_actions(self._position[0], self._position[1])
        action = 0
        if random.random() < self._learning_rate:  # explore
            action = random.choice(possible_actions)
        else:
            best_actions = np.intersect1d(possible_actions, self._qtable.get_max_state_action_value_actions(self._position[0], self._position[1]))  # find actions with 
            action = random.choice(best_actions)
        

        return self._board.get_tile(self._position[0], self._position[1]).score

    def episode(self):
        print(self)
        while self._board.get_tile(self._position[0], self._position[1]).terminal == False:
            self.update()
            print(agent)
        self._position = [0, 0]


if __name__ == "__main__":
    board = Board(5, 5)
    board.set_tile(4, 4, Tile(100, True))
    agent = Agent(0, 1.0, board)
    agent.episode()