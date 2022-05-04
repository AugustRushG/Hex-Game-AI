import random

import numpy as np

from random_robot.node import a_star_search
import time

MAX = 10000
MIN = -10000


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
    count = 0

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
        print("action is ",action)

        if self.color == "red" and player == "red":
            if action[0] == 'STEAL':
                self.redOccupiedList.pop()
            else:
                self.redOccupiedList.append([action[1], action[2]])

                if [action[1], action[2]] in self.blueStartList:
                    self.blueStartList.remove([action[1], action[2]])
                    # print("blue list start", self.blueStartList)
                if [action[1], action[2]] in self.blueGoalList:
                    self.blueGoalList.remove([action[1], action[2]])
                # print("blue list goal", self.blueGoalList)
                # print("red List recording self")
                # print(self.redOccupiedList)
        elif self.color == "blue" and player == "red":
            self.redOccupiedList.append([action[1], action[2]])
            # print(self.blueStartList[1])
            # print(action)
            if [action[1], action[2]] in self.blueStartList:
                self.blueStartList.remove([action[1], action[2]])
                # print("blue list start and goal", self.blueStartList, self.blueGoalList)
            if [action[1], action[2]] in self.blueGoalList:
                self.blueGoalList.remove([action[1], action[2]])
                # print("blue list start and goal", self.blueStartList, self.blueGoalList)

            # print("blue List recording red")
            # print(self.redOccupiedList)
        elif self.color == "red" and player == "blue":
            if action[0] == 'STEAL':
                self.blueOccupiedList.append(self.redOccupiedList[-1])
                if len(self.blueStartList) != self.boardSize:
                    self.blueStartList.append(self.redOccupiedList[-1])
                if len(self.blueGoalList) != self.boardSize:
                    self.blueGoalList.append(self.redOccupiedList[-1])
                self.redOccupiedList.pop()
            else:
                self.blueOccupiedList.append([action[1], action[2]])
                # if blue placed at my goal or start cell, remove this cell from the list
                if [action[1], action[2]] in self.redStartList:
                    self.redStartList.remove([action[1], action[2]])
                # print("red list start and goal", self.redStartList, self.redGoalList)
                if [action[1], action[2]] in self.redGoalList:
                    self.redGoalList.remove([action[1], action[2]])

                # print("red List recording blue")
                # print(self.blueOccupiedList)
        else:
            if action[0] == 'STEAL':
                self.blueOccupiedList.append(self.redOccupiedList[-1])
                if len(self.blueStartList) != self.boardSize:
                    self.blueStartList.append(self.redOccupiedList[-1])
                if len(self.blueGoalList) != self.boardSize:
                    self.blueGoalList.append(self.redOccupiedList[-1])
                if self.redOccupiedList[-1] in self.redStartList:
                    self.redStartList.remove(self.redOccupiedList[-1])
                    # print("blue list start and goal", self.blueStartList, self.blueGoalList)
                if self.redOccupiedList[-1] in self.redGoalList:
                    self.redGoalList.remove(self.redOccupiedList[-1])
                self.redOccupiedList.pop()

            else:
                self.blueOccupiedList.append([action[1], action[2]])

                if [action[1], action[2]] in self.redStartList:
                    self.redStartList.remove([action[1], action[2]])
                    # print("blue list start and goal", self.blueStartList, self.blueGoalList)
                if [action[1], action[2]] in self.redGoalList:
                    self.redGoalList.remove([action[1], action[2]])
                    # print("blue list start and goal", self.blueStartList, self.blueGoalList)
                # print("blue List recording blue")
                # print(self.blueOccupiedList)
        start_time = time.time()

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


