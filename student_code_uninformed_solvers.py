from solver import *
from collections import deque

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
    # self.visited = dict()
    # self.currentState = GameState(self.gm.getGameState(), 0, None)
    # self.visited[self.currentState] = True
    # self.victoryCondition = victoryCondition

    # self.children = []
    # self.nextChildToVisit = GameState.FIRST_CHILD_INDEX
    # self.parent = None
    # self.requiredMovable = movableToReachThisState
    # self.state = state
    # self.depth = depth
    # def dfs_loop(self,movables,to_move):


    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        pass


class SolverBFS(UninformedSolver):

    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)


    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        pass
