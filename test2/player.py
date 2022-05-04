import random

import numpy as np
from numpy import array, roll
from queue import Queue
from test1.node import a_star_search
import time

MAX = 10000
MIN = -10000
# Utility function to add two coord tuples
_ADD = lambda a, b: (a[0] + b[0], a[1] + b[1])

# Neighbour hex steps in clockwise order
_HEX_STEPS = array([(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)],
                   dtype="i,i")
_PLAYER_AXIS = {
    "red": 0, # Red aims to form path in r/0 axis
    "blue": 1 # Blue aims to form path in q/1 axis
}

# Format: (where to capture, opponent coordinate1, opponent coordinate2
_CAPTURE_PATTERNS = [[_ADD(n1, n2), n1, n2]
                     for n1, n2 in
                     list(zip(_HEX_STEPS, roll(_HEX_STEPS, 1))) +
                     list(zip(_HEX_STEPS, roll(_HEX_STEPS, 2)))]

_SWAP_PLAYER = {0: 0, 1: 2, 2: 1}

def length_of_path(path, occupied):
    length = len(path)
    for coords in path:
        if coords in occupied:
            length -= 1

    return length


def neighbours(node, all_nodes, red_occupied_list, blue_occupied_list):
    dirs = [[1, -1],  # up left
            [1, 0],  # up right
            [0, -1],  # left
            [0, 1],  # right
            [-1, 0],  # down left
            [-1, 1], ]  # down right
    result = []
    for i in dirs:
        neighbor = [node[0] + i[0], node[1] + i[1]]
        if neighbor in all_nodes and neighbor not in red_occupied_list and neighbor not in blue_occupied_list:
            result.append(neighbor)
    return result


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
    center = []

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
        self.center = [self.boardSize // 2, self.boardSize // 2]
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
        badOpening = [[0, 0], [0, 1], [1, 0], [self.boardSize, self.boardSize],
                     [self.boardSize-1, self.boardSize], [self.boardSize, self.boardSize-1]]

        if self.color == "red":
            if self.count == 0:
                decision = ('PLACE', 0, self.boardSize-1)  # best opening move considering swap mechanism
                self.count += 1
            elif self.count == 1 and self.center not in self.blueOccupiedList:
                decision = ('PLACE', self.center[0], self.center[1])
                self.count += 1
            else:
                best_move = self.find_best_move()
                print(best_move)
                decision = ('PLACE', best_move[0], best_move[1])

        elif self.color == "blue":

            if self.count == 0 and self.redOccupiedList[0] not in badOpening:
                decision = ('STEAL',)
                self.count += 1
            elif self.count == 0 and self.center not in self.redOccupiedList:
                decision = ('PLACE', self.center[0], self.center[1])
                self.count += 1
            else:

                best_move = self.find_best_move()
                print(best_move)
                decision = ('PLACE', best_move[0], best_move[1])

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
                self.redOccupiedList.append([action[1], action[2]])

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
                self.blueOccupiedList.append(self.redOccupiedList[-1])
                if len(self.blueStartList) != self.boardSize:
                    self.blueStartList.append(self.redOccupiedList[-1])
                if len(self.blueGoalList) != self.boardSize:
                    self.blueGoalList.append([self.redOccupiedList[-1][0], self.boardSize - 1])
                self.redOccupiedList.pop()
            else:
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
                self.blueOccupiedList.append(self.redOccupiedList[-1])
                if len(self.blueStartList) != self.boardSize:
                    self.blueStartList.append(self.redOccupiedList[-1])
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

                if [action[1], action[2]] in self.redStartList:
                    index = self.redStartList.index([action[1], action[2]])
                    self.redStartList.pop(index)
                    self.redGoalList.pop(index)
                # print("red list start and goal", self.redStartList, self.redGoalList)
                if [action[1], action[2]] in self.redGoalList:
                    index = self.redGoalList.index([action[1], action[2]])
                    self.redStartList.pop(index)
                    self.redGoalList.pop(index)

        start_time = time.time()
        print("evaluation is ", self.evaluation([self.all_nodes, self.redOccupiedList, self.blueOccupiedList]))
        print("--- %s seconds ---" % (time.time() - start_time))

    def evaluation(self, state):
        """
        evaluate each board state, and return the current value
        negative means good for blue, positive means good for red

        the goal of the game is to create an unbroken chain of hexes that connect to the opposing sides of the board,
        so it would be good to calculate the shortest paths between the opposing sides


        Args:
            state:

        Returns:

        """
        if len(state[2]) == 0 and len(state[1]) > 0:
            return 1
        if len(state[1]) == 0 and len(state[2]) > 0:
            return -1
        # print("red already occupied", self.redOccupiedList)
        red_score = self.get_shortest_path("red", state)

        # print("blue already occupied", self.blueOccupiedList)
        blue_score = self.get_shortest_path("blue", state)
        # print("red score is blue score is", red_score, blue_score)

        # shortest path, start will be each two sides' coordinates, goal will be the same
        # by using A* search, work out the shortest path's, get this path's steps, minus already occupied cell number.
        # then get the shortest path number.

        # print("evulating state", blue_score - red_score)
        return blue_score - red_score

    def find_best_move(self):
        moves = self.get_all_possible_moves()
        current_state = [self.all_nodes, self.redOccupiedList, self.blueOccupiedList]
        got_removed = False
        got_removed1 = False
        best_move = []
        level = 1
        cells_around = neighbours(self.blueOccupiedList[-1], self.all_nodes, self.redOccupiedList,
                                  self.blueOccupiedList) \
                       + neighbours(self.redOccupiedList[-1], self.all_nodes, self.redOccupiedList,
                                    self.blueOccupiedList)

        print(cells_around)
        if self.color == "red":
            bestVal = MIN
            for move in cells_around:
                if move in self.blueStartList:
                    index = self.blueStartList.index(move)
                    self.blueStartList.pop(index)

                    remove = self.blueGoalList[index]
                    self.blueGoalList.pop(index)
                    # print(self.blueStartList, self.blueGoalList)
                    got_removed = True
                if move in self.blueGoalList:
                    index = self.blueGoalList.index(move)
                    remove = self.blueStartList[index]

                    self.blueStartList.pop(index)
                    self.blueGoalList.pop(index)
                    got_removed1 = True
                self.redOccupiedList.append(move)

                moveVal = self.minimax_abpuring(current_state, level, "blue", MIN, MAX)

                self.redOccupiedList.remove(move)
                if got_removed:
                    self.blueStartList.append(move)
                    self.blueGoalList.append(remove)
                    got_removed = False
                if got_removed1:
                    self.blueGoalList.append(move)
                    self.blueStartList.append(remove)
                    got_removed1 = False

                if moveVal > bestVal:
                    best_move = move
                    bestVal = moveVal
        else:
            bestVal = MAX
            for move in cells_around:
                self.blueOccupiedList.append(move)
                if move in self.redStartList:
                    index = self.redStartList.index(move)
                    self.redStartList.pop(index)

                    remove = self.redGoalList[index]
                    self.redGoalList.pop(index)
                    got_removed = True

                if move in self.redGoalList:
                    # print(self.redGoalList,self.redStartList)
                    index = self.redGoalList.index(move)
                    remove = self.redStartList[index]
                    self.redStartList.pop(index)
                    self.redGoalList.pop(index)
                    got_removed1 = True

                moveVal = self.minimax_abpuring(current_state, level, "red", MIN, MAX)

                self.blueOccupiedList.remove(move)

                if got_removed:
                    self.redStartList.append(move)
                    self.redGoalList.append(remove)
                    got_removed = False
                if got_removed1:
                    self.redStartList.append(remove)
                    self.redGoalList.append(move)
                    got_removed1 = False

                if moveVal < bestVal:
                    bestVal = moveVal
                    best_move = move

        print("The value of the best Move is :", bestVal)

        if best_move is None:
            print(moves)
            return random.choice(moves)

        return best_move

    def get_shortest_path(self, color, state):
        final = MAX
        length = MAX
        if color == "red":
            # print("redstart list, red goal list ",self.redStartList,self.redGoalList)
            if len(state[1]) == 1 and len(state[2]) == 0:
                return self.boardSize - 1
            for j in range(len(self.redStartList)):
                temp_path = []
                # print("start is ,goal is, blueOccupied list is ", self.redStartList[j], self.redGoalList[j], state[2])
                # print("start timing")
                start_time = time.time()

                temp_path = a_star_search(state[0], self.redStartList[j], self.redGoalList[j],
                                          state[2])

                # print("--- %s seconds ---" % (time.time() - start_time))
                # print(temp_path)
                if temp_path is not None:
                    length = length_of_path(temp_path, state[1])
                    # print(length)
                if length < final:
                    final = length
                    red_path = temp_path

            # print(red_path)
            # print("final length", final)
            return final

        else:
            for j in range(len(self.blueStartList)):
                # print("blue start is ,goal is ", self.blueStartList[j], self.blueGoalList[j])
                temp_path = a_star_search(state[0], self.blueStartList[j], self.blueGoalList[j],
                                          state[1])
                if temp_path is not None:
                    # print(temp_path)
                    length = length_of_path(temp_path, state[2])

                    # print(length)

                if length < final:
                    final = length
                    blue_path = temp_path

            # print("best path for blue", blue_path)
            return final

    def get_all_possible_moves(self):
        result = []
        for move in self.all_nodes:
            if (move not in self.redOccupiedList) and (move not in self.blueOccupiedList):
                result.append(move)
        return result

    def minimax_abpuring(self, state, depth, player, alpha, beta):
        got_removed = False
        got_removed1 = False
        current_state = state
        moves = self.get_all_possible_moves()
        score = self.evaluation(current_state)
        cells_around = neighbours(self.blueOccupiedList[-1], self.all_nodes, self.redOccupiedList,
                                  self.blueOccupiedList) \
                       + neighbours(self.redOccupiedList[-1], self.all_nodes, self.redOccupiedList,
                                    self.blueOccupiedList)

        if depth == 0 or score >= 9999 or score <= -9999:
            return self.evaluation(current_state)

        if player == "red":
            for move in cells_around:
                best = MIN
                if move in self.blueStartList:
                    index = self.blueStartList.index(move)
                    self.blueStartList.pop(index)
                    remove = self.blueGoalList[index]
                    self.blueGoalList.pop(index)
                    # print(self.blueStartList, self.blueGoalList)
                    got_removed = True
                if move in self.blueGoalList:
                    index = self.blueGoalList.index(move)
                    remove = self.blueStartList[index]
                    self.blueStartList.pop(index)
                    self.blueGoalList.pop(index)
                    got_removed1 = True

                self.redOccupiedList.append(move)

                # print("red best,alpha,beta is", best, alpha, beta)

                best = max(best, self.minimax_abpuring(current_state, depth - 1, "blue", alpha, beta))
                alpha = max(alpha, best)

                if got_removed:
                    self.blueStartList.append(move)
                    self.blueGoalList.append(remove)
                    got_removed = False
                if got_removed1:
                    self.blueGoalList.append(move)
                    self.blueStartList.append(remove)
                    got_removed1 = False

                self.redOccupiedList.remove(move)

                if alpha >= beta:
                    # print("\nbreak here\n")
                    break
            if best is None:
                return MIN
            return best
        elif player == "blue":
            best = MAX
            for move in cells_around:
                self.blueOccupiedList.append(move)

                if move in self.redStartList:
                    index = self.redStartList.index(move)
                    self.redStartList.pop(index)
                    remove = self.redGoalList[index]
                    self.redGoalList.pop(index)
                    got_removed = True

                if move in self.redGoalList:
                    index = self.redGoalList.index(move)
                    remove = self.redStartList[index]
                    self.redStartList.pop(index)
                    self.redGoalList.pop(index)
                    got_removed1 = True
                # print("blue best,alpha,beta is", best, alpha, beta)
                best = min(best, self.minimax_abpuring(current_state, depth - 1, "red", alpha, beta))
                beta = min(beta, best)

                self.blueOccupiedList.remove(move)

                if got_removed:
                    self.redStartList.append(move)
                    self.redGoalList.append(remove)
                    got_removed = False
                if got_removed1:
                    self.redStartList.append(remove)
                    self.redGoalList.append(move)
                    got_removed1 = False

                if alpha >= beta:
                    # print("\nbreak here\n")
                    break
            if best is None:
                return MAX
            return best

    def check_game_over(self, state):
        red_start = np.intersect1d(state[1],self.redStartList)
        red_goal=np.intersect1d(state[1],self.redGoalListList)
        blue_start = np.intersect1d(state[2],self.blueStartList)
        blue_goal = np.intersect1d(state[2],self.blueGoalList)

        for i in range(red_start):
            for j in range(red_goal):
                return 0


    # The following codes are derived from the referee folder
    # !NOT COMPLETED

    def connected_coords(self, start_coord):
        """
        Find connected coordinates from start_coord. This uses the token
        value of the start_coord cell to determine which other cells are
        connected (e.g., all will be the same value).
        """
        # Get search token type
        token_type = self._data[start_coord]

        # Use bfs from start coordinate
        reachable = set()
        queue = Queue(0)
        queue.put(start_coord)

        while not queue.empty():
            curr_coord = queue.get()
            reachable.add(curr_coord)
            for coord in self._coord_neighbours(curr_coord):
                if coord not in reachable and self._data[coord] == token_type:
                    queue.put(coord)

        return list(reachable)

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


    def capture(coord, selfOccupiedList, oppOccupiedList):
        """
        Takes in the colour, coordinate of current move, list of occupied cells of the opponent colour
        and a list to record the captured cells.
        For current move, check if a capture pattern exists and returns the coordinate needed to capture
        Derived from _apply_captures function in referee
        """

        captureList = []

        for pattern in _CAPTURE_PATTERNS:
            self = [coord[0] + list(pattern[0])[0], coord[1] + list(pattern[0])[1]]
            opponent1 = [coord[0] + list(pattern[1])[0], coord[1] + list(pattern[1])[1]]
            opponent2 = [coord[0] + list(pattern[2])[0], coord[1] + list(pattern[2])[1]]

            if opponent1 in oppOccupiedList and opponent2 in oppOccupiedList and self in selfOccupiedList:
                captureList.append([opponent1, opponent2])

        return captureList




