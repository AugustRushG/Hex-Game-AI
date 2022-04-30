from Augustian.node import a_star_search
import time

MAX = 10000
MIN = -10000


def length_of_path(path, occupied):
    length = len(path)
    for coords in path:
        if coords in occupied:
            length -= 1

    return length


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
            start_list = [lower, upper]
            goal_list = [upper, lower]

            self.redStartList = start_list
            self.redGoalList = goal_list

            left = []
            right = []

            for i in range(n):
                left.append([i, 0])
                right.append([i, n - 1])
            start_list = [left, right]
            goal_list = [right, left]

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
            start_list = [left, right]
            goal_list = [right, left]

            self.blueStartList = start_list
            self.blueGoalList = goal_list

            lower = []
            upper = []
            for i in range(n):
                lower.append([0, i])
                upper.append([n - 1, i])
            start_list = [lower, upper]
            goal_list = [upper, lower]

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

        if self.color == "red" and player == "red":
            self.redOccupiedList.append([action[1], action[2]])

            if [action[1], action[2]] in self.blueStartList[0]:
                self.blueStartList[0].remove([action[1], action[2]])
                # print("blue list start and goal", self.blueStartList, self.blueGoalList)
            if [action[1], action[2]] in self.blueStartList[1]:
                self.blueStartList[1].remove([action[1], action[2]])
                # print("blue list start and goal", self.blueStartList, self.blueGoalList)
            # print("red List recording self")
            # print(self.redOccupiedList)
        elif self.color == "blue" and player == "red":
            self.redOccupiedList.append([action[1], action[2]])
            # print(self.blueStartList[1])
            # print(action)
            if [action[1], action[2]] in self.blueStartList[0]:
                self.blueStartList[0].remove([action[1], action[2]])
                # print("blue list start and goal", self.blueStartList, self.blueGoalList)
            if [action[1], action[2]] in self.blueStartList[1]:
                self.blueStartList[1].remove([action[1], action[2]])
                # print("blue list start and goal", self.blueStartList, self.blueGoalList)

            # print("blue List recording red")
            # print(self.redOccupiedList)
        elif self.color == "red" and player == "blue":
            self.blueOccupiedList.append([action[1], action[2]])

            # if blue placed at my goal or start cell, remove this cell from the list
            if [action[1], action[2]] in self.redStartList[0]:
                self.redStartList[0].remove([action[1], action[2]])
                # print("red list start and goal", self.redStartList, self.redGoalList)
            if [action[1], action[2]] in self.redStartList[1]:
                self.redStartList[1].remove([action[1], action[2]])

            # print("red List recording blue")
            # print(self.blueOccupiedList)
        else:
            self.blueOccupiedList.append([action[1], action[2]])

            if [action[1], action[2]] in self.redStartList[0]:
                self.redStartList[0].remove([action[1], action[2]])
                # print("blue list start and goal", self.blueStartList, self.blueGoalList)
            if [action[1], action[2]] in self.redStartList[1]:
                self.redStartList[1].remove([action[1], action[2]])
                # print("blue list start and goal", self.blueStartList, self.blueGoalList)
            # print("blue List recording blue")
            # print(self.blueOccupiedList)

        start_time = time.time()
        self.evaluation()
        print("--- %s seconds ---" % (time.time() - start_time))

    def evaluation(self):
        """
        evaluate each board state, and return the current value
        negative means good for blue, positive means good for red

        the goal of the game is to create an unbroken chain of hexes that connect to the opposing sides of the board,
        so it would be good to calculate the shortest paths between the opposing sides


        Args:
            position:

        Returns:

        """

        print("red already occupied", self.redOccupiedList)
        red_score = self.get_shortest_path("red")
        print("blue already occupied", self.blueOccupiedList)
        blue_score = self.get_shortest_path("blue")

        # shortest path, start will be each two sides' coordinates, goal will be the same
        # by using A* search, work out the shortest path's, get this path's steps, minus already occupied cell number.
        # then get the shortest path number.

        print("evulating state", blue_score - red_score)
        return blue_score - red_score

    def minimax(self, depth, maximizingPlayer):
        # print("minimax start")
        # if current board is has finished(win or lose or draw) or depth is 0 return

        moves = self.get_all_possible_moves()
        got_removed = False
        got_removed1 = False

        if depth == 0:
            return self.evaluation()

        if maximizingPlayer == "red":
            max_evaluation = MIN

            for move in moves:
                self.redOccupiedList.append(move)

                if move in self.blueStartList[0]:
                    self.blueStartList[0].remove(move)
                    # print(self.blueStartList, self.blueGoalList)
                    got_removed = True
                if move in self.blueStartList[1]:
                    self.blueStartList[1].remove(move)
                    got_removed1 = True

                max_evaluation = max(max_evaluation, self.minimax(depth - 1, "blue"))

                self.redOccupiedList.remove(move)
                if got_removed:
                    self.blueStartList[0].append(move)
                    got_removed = False
                if got_removed1:
                    self.blueStartList[1].append(move)
                    got_removed1 = False

            # print("max is ", max_evaluation)
            return max_evaluation

        else:
            min_evaluation = MAX

            for move in moves:
                self.blueOccupiedList.append(move)

                if move in self.redStartList[0]:
                    self.redStartList[0].remove(move)
                    got_removed = True

                if move in self.redStartList[1]:
                    self.redStartList[1].remove(move)
                    got_removed1 = True

                min_evaluation = min(min_evaluation, self.minimax(depth - 1, "red"))

                self.blueOccupiedList.remove(move)

                if got_removed:
                    self.redStartList[0].append(move)
                    got_removed = False
                if got_removed1:
                    self.redStartList[1].append(move)
                    got_removed1 = False
            # print("min is ", min_evaluation)
            return min_evaluation

    def find_best_move(self):
        got_removed = False
        got_removed1 = False
        moves = self.get_all_possible_moves()
        if self.color == "red":
            bestVal = MIN
            for move in moves:
                # self.redOccupiedList.append(move)

                if move in self.blueStartList[0]:
                    self.blueStartList[0].remove(move)
                    # print(self.blueStartList, self.blueGoalList)
                    got_removed = True
                if move in self.blueStartList[1]:
                    self.blueStartList[1].remove(move)
                    got_removed1 = True

                moveVal = self.minimax(1, "red")

                if got_removed:
                    self.blueStartList[0].append(move)
                    got_removed = False
                if got_removed1:
                    self.blueStartList[1].append(move)
                    got_removed1 = False

                # self.redOccupiedList.remove(move)

                if moveVal > bestVal:
                    best_move = move
                    bestVal = moveVal
        else:
            bestVal = MAX
            for move in moves:
                # self.blueOccupiedList.append(move)
                if move in self.redStartList[0]:
                    self.redStartList[0].remove(move)
                    got_removed = True

                if move in self.redStartList[1]:
                    self.redStartList[1].remove(move)
                    got_removed1 = True

                moveVal = self.minimax(0, "blue")

                if got_removed:
                    self.redStartList[0].append(move)
                    got_removed = False
                if got_removed1:
                    self.redStartList[1].append(move)
                    got_removed1 = False
                # self.blueOccupiedList.remove(move)

                if moveVal < bestVal:
                    bestVal = moveVal
                    best_move = move

        print("The value of the best Move is :", bestVal)
        return best_move

    def get_shortest_path(self, color):
        final = MAX
        if color == "red":

            for i in range(self.START_BOUND):
                # print("length of start length",len(self.redStartList[1]))
                for j in range(len(self.redStartList[i])):
                    for k in range(len(self.redGoalList[i])):
                        # print("start is ,goal is ", self.redStartList[i][j], self.redGoalList[i][k])
                        temp_path = a_star_search(self.all_nodes, self.redStartList[i][j], self.redGoalList[i][k],
                                                  self.blueOccupiedList)
                        # print(temp_path)
                        if temp_path is not None:
                            length = length_of_path(temp_path, self.redOccupiedList)
                        # print(length)
                        if length < final:
                            final = length
                            red_path = temp_path

            # print(red_path)
            # print("final length", final)
            return final
        else:

            for i in range(self.START_BOUND):
                for j in range(len(self.blueStartList[i])):
                    for k in range(len(self.blueGoalList[i])):
                        # print("start is ,goal is ", self.blueStartList[i][j], self.blueGoalList[i][k])
                        temp_path = a_star_search(self.all_nodes, self.blueStartList[i][j], self.blueGoalList[i][k],
                                                  self.redOccupiedList)
                        if temp_path is not None:
                            # print(temp_path)
                            length = length_of_path(temp_path, self.blueOccupiedList)
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

    def minimax_abpuring(self, depth, player, alpha, beta):
        moves = self.get_all_possible_moves()

        for move in moves:
            alpha=max(alpha,min())

