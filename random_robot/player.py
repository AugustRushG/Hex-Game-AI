import random

import numpy as np
from numpy import array, roll
from queue import Queue

from test1.node import a_star_search
import time
MAX = 10000
MIN = -10000

_ADD = lambda a, b: (a[0] + b[0], a[1] + b[1])

# Neighbour hex steps in clockwise order
_HEX_STEPS = array([(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)],
                   dtype="i,i")
_PLAYER_AXIS = {
    "red": 0,  # Red aims to form path in r/0 axis
    "blue": 1  # Blue aims to form path in q/1 axis
}

# Format: (where to capture, opponent coordinate1, opponent coordinate2
_CAPTURE_PATTERNS = [[_ADD(n1, n2), n1, n2]
                     for n1, n2 in
                     list(zip(_HEX_STEPS, roll(_HEX_STEPS, 1))) +
                     list(zip(_HEX_STEPS, roll(_HEX_STEPS, 2)))]

_SWAP_PLAYER = {0: 0, 1: 2, 2: 1}



class Player:
    redOccupiedList = []
    blueOccupiedList = []

    redGoalList = []
    blueGoalList = []
    redStartList = []
    blueStartList = []

    START_BOUND = 2
    turns_left = 0
    color = ""
    boardSize = 0
    all_nodes = []
    count = 1

    def __init__(self, player, n):
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "red" if your player will
        play as Red, or the string "blue" if your player will play
        as Blue.
        """
        # put your code here
        self.boardSize = n
        self.turns_left = n * n

        # draw the board
        for x in range(n):
            for y in range(n):
                self.all_nodes.append([x, y])

        if player == "red":
            self.color = "red"

            lower = []
            upper = []
            for i in range(n):
                lower.append([0, i])
                upper.append([n - 1, i])
            start_list = lower
            goal_list = upper

            self.redStartList = start_list
            self.redGoalList = goal_list

            left = []
            right = []

            for i in range(n):
                left.append([i, 0])
                right.append([i, n - 1])
            start_list = left
            goal_list = right

            self.blueStartList = start_list
            self.blueGoalList = goal_list

            print("red move")

        else:
            self.color = "blue"

            left = []
            right = []

            for i in range(n):
                left.append([i, 0])
                right.append([i, n - 1])
            start_list = left
            goal_list = right

            self.blueStartList = start_list
            self.blueGoalList = goal_list

            lower = []
            upper = []
            for i in range(n):
                lower.append([0, i])
                upper.append([n - 1, i])
            start_list = lower
            goal_list = upper

            self.redStartList = start_list
            self.redGoalList = goal_list

            print("blue move")

    def action(self):
        """
        Called at the beginning of your turn. Based on the current state
        of the game, select an action to play.
        """

        """
        read the board first everytime before action
        then figure out whats the best way
        """

        # put your code here
        decision = ()

        # print("still have this many cells that can be placed", turns_left, len(self.redOccupiedList),len(self.blueOccupiedList))

        if self.color == "red":
            if self.count == 0:
                decision = ('PLACE', 0, 0)
                self.count += 1
            else:
                best_move = self.find_best_move()
                print(best_move)
                decision = ('PLACE', best_move[0], best_move[1])

        elif self.color == "blue":
            # print("countis",self.count)
            best_move = self.find_best_move()
            print(best_move)
            decision = ('PLACE', best_move[0], best_move[1])
            # print("countis",self.count)

        return decision

    def turn(self, player, action):
        """
        Called at the end of each player's turn to inform this player of
        their chosen action. Update your internal representation of the
        game state based on this. The parameter action is the chosen
        action itself.

        Note: At the end of your player's turn, the action parameter is
        the same as what your player returned from the action method
        above. However, the referee has validated it at this point.
        """
        # put your code here
        print("self color", self.color)
        print("player color", player)
        print("action is ", action)

        if self.color == "red" and player == "red":
            if action[0] == 'STEAL':
                self.redOccupiedList.pop()
            else:
                capture_list = self.detect_capture([action[1], action[2]], self.redOccupiedList, self.blueOccupiedList)
                self.redOccupiedList.append([action[1], action[2]])

                for pair in capture_list:
                    for coords in pair:
                        if coords in self.blueOccupiedList:
                            self.blueOccupiedList.remove(coords)

                if [action[1], action[2]] in self.blueStartList:
                    index = self.blueStartList.index([action[1], action[2]])
                    self.blueStartList.pop(index)
                    self.blueGoalList.pop(index)
                    # print("blue list start", self.blueStartList)
                if [action[1], action[2]] in self.blueGoalList:
                    index = self.blueGoalList.index([action[1], action[2]])
                    self.blueStartList.pop(index)
                    self.blueGoalList.pop(index)
                # print("blue list goal", self.blueGoalList)
                # print("red List recording self")
                # print(self.redOccupiedList)
        elif self.color == "blue" and player == "red":

            self.redOccupiedList.append([action[1], action[2]])
            capture_list = self.detect_capture([action[1], action[2]], self.redOccupiedList, self.blueOccupiedList)
            for pair in capture_list:
                for coords in pair:
                    if coords in self.blueOccupiedList:
                        self.blueOccupiedList.remove(coords)
            # print(self.blueStartList[1])
            # print(action)
            if [action[1], action[2]] in self.blueStartList:
                index = self.blueStartList.index([action[1], action[2]])
                self.blueStartList.pop(index)
                self.blueGoalList.pop(index)
                # print("blue list start", self.blueStartList)
            if [action[1], action[2]] in self.blueGoalList:
                index = self.blueGoalList.index([action[1], action[2]])
                self.blueStartList.pop(index)
                self.blueGoalList.pop(index)

            # print("blue List recording red")
            # print(self.redOccupiedList)
        elif self.color == "red" and player == "blue":
            if action[0] == 'STEAL':
                self.blueOccupiedList.append([self.redOccupiedList[-1][-1], self.redOccupiedList[-1][0]])
                if len(self.blueStartList) != self.boardSize:
                    self.blueStartList.append([self.redOccupiedList[-1][-1], self.redOccupiedList[-1][0]])
                if len(self.blueGoalList) != self.boardSize:
                    self.blueGoalList.append([self.redOccupiedList[-1][0], self.boardSize - 1])
                self.redOccupiedList.pop()
            else:
                capture_list = self.detect_capture([action[1], action[2]], self.blueOccupiedList, self.redOccupiedList)
                print(capture_list)
                for pair in capture_list:
                    for coords in pair:
                        if coords in self.redOccupiedList:
                            self.redOccupiedList.remove(coords)

                self.blueOccupiedList.append([action[1], action[2]])
                # if blue placed at my goal or start cell, remove this cell from the list
                if [action[1], action[2]] in self.redStartList:
                    index = self.redStartList.index([action[1], action[2]])
                    self.redStartList.pop(index)
                    self.redGoalList.pop(index)
                # print("red list start and goal", self.redStartList, self.redGoalList)
                if [action[1], action[2]] in self.redGoalList:
                    index = self.redGoalList.index([action[1], action[2]])
                    self.redStartList.pop(index)
                    self.redGoalList.pop(index)

                # print("red List recording blue")
                # print(self.blueOccupiedList)
        else:
            if action[0] == 'STEAL':
                self.blueOccupiedList.append([self.redOccupiedList[-1][-1], self.redOccupiedList[-1][0]])
                if len(self.blueStartList) != self.boardSize:
                    self.blueStartList.append([self.redOccupiedList[-1][-1], self.redOccupiedList[-1][0]])
                if len(self.blueGoalList) != self.boardSize:
                    self.blueGoalList.append([self.redOccupiedList[-1][0], self.boardSize - 1])

                if self.redOccupiedList[-1] in self.redStartList:
                    index = self.redStartList.index(self.redOccupiedList[-1])

                    self.redStartList.pop(index)
                    self.redGoalList.pop(index)

                # print("red start and goal is ",self.redStartList,self.redGoalList)
                self.redOccupiedList.pop()

            else:
                self.blueOccupiedList.append([action[1], action[2]])

                capture_list = self.detect_capture([action[1], action[2]], self.blueOccupiedList, self.redOccupiedList)
                for pair in capture_list:
                    for coords in pair:
                        if coords in self.redOccupiedList:
                            self.redOccupiedList.remove(coords)

                if [action[1], action[2]] in self.redStartList:
                    index = self.redStartList.index([action[1], action[2]])
                    self.redStartList.pop(index)
                    self.redGoalList.pop(index)
                # print("red list start and goal", self.redStartList, self.redGoalList)
                if [action[1], action[2]] in self.redGoalList:
                    index = self.redGoalList.index([action[1], action[2]])
                    self.redStartList.pop(index)
                    self.redGoalList.pop(index)

        # print(self.redOccupiedList)




    def find_best_move(self):
        moves = self.get_all_possible_moves()

        if self.color == "red":
            bestVal = MIN
            best_move=random.choice(moves)
        else:
            bestVal = MAX
            best_move=random.choice(moves)

        print("The value of the best Move is :", bestVal)
        return best_move


    def get_all_possible_moves(self):
        result = []
        for move in self.all_nodes:
            if (move not in self.redOccupiedList) and (move not in self.blueOccupiedList):
                result.append(move)
        return result

    def _coord_neighbours(self, coord):
        """
        Returns (within-bounds) neighbouring coordinates for given coord.
        """
        return [_ADD(coord, step) for step in _HEX_STEPS \
                if self.inside_bounds(_ADD(coord, step))]

    def _turn_detect_end(self, player, action):
        """
        Register that a turn has passed: Update turn counts and detect
        termination conditions.
        """
        # Register turn
        self.nturns += 1
        self.history[self.board.digest()] += 1

        # Game end conditions

        # Condition 1: player forms a continuous path spanning board (win).
        # check reachable coords from just-placed token to detect winning path
        # NOTE: No point checking this while total turns is less than 2n - 1
        if self.nturns >= (self.board.n * 2) - 1:
            _, r, q = action
            reachable = self.board.connected_coords((r, q))
            axis_vals = [coord[_PLAYER_AXIS[player]] for coord in reachable]
            if min(axis_vals) == 0 and max(axis_vals) == self.board.n - 1:
                self.result = "winner: " + player
                self.result_cluster = set(reachable)
                return

    def inside_bounds(self, coord):
        """
        True iff coord inside board bounds.
        """
        r, q = coord
        return r >= 0 and r < self.n and q >= 0 and q < self.n

    def capture(self, coord, occupiedList, captureList):

        """
        Takes in the colour, coordinate of current move, list of occupied cells of the opponent colour
        and a list to record the captured cells.
        For current move, check if a capture pattern exists and returns the coordinate needed to capture
        Derived from _apply_captures function in referee
        """

        coordToCapture = []
        for pattern in _CAPTURE_PATTERNS:

            opponent1 = [coord[0] + list(pattern[1])[0], coord[1] + list(pattern[1])[1]]
            opponent2 = [coord[0] + list(pattern[2])[0], coord[1] + list(pattern[2])[1]]

            if opponent1 in occupiedList and opponent2 in occupiedList:
                captureList.append([opponent1, opponent2])
                coordToCapture.append(list(pattern[0]))

        return coordToCapture

    def detect_capture(self, coord, selfOccupiedList, oppOccupiedList):
        """Function to find pieces that have been captured,
        given the occupied list of red and blue and the current coordinate"""

        captureList = []

        for pattern in _CAPTURE_PATTERNS:
            self = [coord[0] + list(pattern[0])[0], coord[1] + list(pattern[0])[1]]
            opponent1 = [coord[0] + list(pattern[1])[0], coord[1] + list(pattern[1])[1]]
            opponent2 = [coord[0] + list(pattern[2])[0], coord[1] + list(pattern[2])[1]]

            if opponent1 in oppOccupiedList and opponent2 in oppOccupiedList and self in selfOccupiedList:
                captureList.append([opponent1, opponent2])

        return captureList

