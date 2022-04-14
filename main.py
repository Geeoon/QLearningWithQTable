# https://sci-hub.ru/10.1017/9781108955652.016
import random
import copy
import numpy as np
import matplotlib.pyplot as plt

class Tile:
    def __init__(self, score:int, terminal:bool = False):
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

    def get_max_state_action_value_actions(self, x:int, y:int, board:Board):
        actions = []
        max = -float("inf")
        action_values = self.get_state_action_values(x, y)
        for i in range(len(action_values)):
            if i in board.get_actions(x, y):
                if (action_values[i] > max):
                    max = action_values[i]
        for i in range(len(action_values)):
            if i in board.get_actions(x, y) and action_values[i] == max:
                actions.append(i)
        return actions

    def get_max_state_action_value(self, x:int, y:int):
        return max(self._table[x, y])


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

    def optimal_action(self):
        possible_actions = self._board.get_actions(self._position[0], self._position[1])
        if 0 < self._learning_rate:  # explore
            return random.choice(possible_actions)  
        else:
            best_actions = self._qtable.get_max_state_action_value_actions(self._position[0], self._position[1], self._board)  # find actions with best Q-value
            return random.choice(best_actions)  # if there are multiple, choose a random one

    def update(self):
        action = self.optimal_action()  # a <- get_action(Q, s)
        saved_position = copy.deepcopy(self._position)
        self.move(action)
        self._qtable.set_state_action_value(saved_position[0], saved_position[1], action, (1 - self._learning_rate) * self._qtable.get_state_action_values(saved_position[0], saved_position[1])[action] + self._learning_rate * (self._board.get_tile(self._position[0], self._position[1]).score + self._discount_factor * self._qtable.get_max_state_action_value(self._position[0], self._position[1])))
        
        return self._board.get_tile(self._position[0], self._position[1]).score

    def episode(self):
        episode_score = 0
        self._position = [0, 0]  # s <- get_initial_state()
        while self._board.get_tile(self._position[0], self._position[1]).terminal == False:  # while s not terminal do
            episode_score += self.update()
        return episode_score


if __name__ == "__main__":
    board = Board(5, 5)
    board.set_tile(4, 4, Tile(100, True))
    board.set_tile(1, 1, Tile(-100))
    board.set_tile(0, 1, Tile(-30, True))
    board.set_tile(1, 0, Tile(-40))
    board.set_tile(0, 3, Tile(200, True))
    agent = Agent(0.9, 0.75, board)
    for i in range(100): # training with high learning rate
        agent.episode()

    agent._learning_rate = 0
    trials = 0
    trails_score_pair = [[], []]
    for i in range(100):
        trails_score_pair[0].append(trials)
        trails_score_pair[1].append(agent.episode())
        trials += 1

plt.plot(trails_score_pair[0], trails_score_pair[1])
plt.xlabel('Trial Number')
plt.ylabel('Score of Episode')
plt.show()