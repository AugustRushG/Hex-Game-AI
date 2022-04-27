from Augustian.node import a_star_search


class Player:
    redOccupiedList = []
    blueOccupiedList = []

    redGoalList = []
    blueGoalList = []
    redStartList = []
    blueStartList = []

    color = ""
    boardSize = 0

    all_nodes = []

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
                upper.append([n, i])
            start_list = [lower, upper]
            self.redStartList = start_list
            print("red move")

        else:
            self.color = "blue"
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
        if self.color == "red":

            decision = ('PLACE', 2, 1)
            self.redOccupiedList.append((2, 1))
            print(self.redOccupiedList)

        elif self.color == "blue":

            decision = ('PLACE', 2, 3)
            self.blueOccupiedList.append((2, 3))

        print(self.color)

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

    def decision(self, redOccList, blueOccList):
        """
        reads in where has been occupied, decide where to place based on the current board.
        Args:
            redOccList:
            blueOccList:

        Returns:

        """
        if self.color == "red":
            result = ()
        else:
            result = ()
        return result

    def evaluation(self, position):
        """
        evaluate each board state, and return the current value
        negative means good for blue, positive means good for red

        the goal of the game is to create an unbroken chain of hexes that connect to the opposing sides of the board,
        so it would be good to calculate the shortest paths between the opposing sides

        Args:
            position:

        Returns:

        """

        # start is their occupied point

        red_score = 0
        blue_score = 0

        # shortest path, start will be each two sides' coordinates, goal will be the same
        # by using A* search, work out the shortest path's, get this path's steps, minus already occupied cell number.
        # then get the shortest path number.

        return blue_score-red_score

    def minimax(self, depth, maximizingPlayer):
        # if current board is has finished(win or lose or draw) or depth is 0 return
        if depth == 0:
            return
