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

    def dfs_loop(self,available_moves,childindex):
        while childindex < len(available_moves):
            flg=False #init bool flag to find matched state
            self.gm.makeMove(available_moves[childindex]) #move to child
            tc=childindex+1 #init new index
            gs2 = self.gm.getGameState() #store gs
            v = list(self.visited.keys()) #store keys of visted
            for s in v: #set flag true if match
                if s.state==gs2: flg=True
            if flg == True:
                self.gm.reverseMove(available_moves[childindex])
                childindex=tc
            else:
                gs3 = GameState(gs2, self.currentState.depth+1, available_moves[childindex])
                self.currentState.nextChildToVisit = tc
                self.currentState = gs3
                self.currentState.children.append(gs3)
                #break
                #forgot to update parent!
                gs3.parent = self.currentState
                break
        return


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

        #check if current state is victory condition
        if(self.currentState.state == self.victoryCondition):
            self.visited[self.currentState]=True
            return True
        else:
            available_moves = self.gm.getMovables()
            childindex = self.currentState.nextChildToVisit
            self.visited[self.currentState] = True
            self.dfs_loop(available_moves,childindex)


        return False





class SolverBFS(UninformedSolver):

    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.m=0
        self.q=deque()
    #m=0
    #q=deque()
    def traverse(self,s,f):
        if f:
            l=[]
            while s.parent:
                self.gm.reverseMove(s.requiredMovable)
                l.append(s.requiredMovable)
                s=s.parent
            return l

        else:
            while self.currentState.parent:
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent
            return
        return

    def bfs_loop(self,g):
        #traverse back to root
        self.traverse(self.currentState,False)
        #record traverse to goal
        actionlist=self.traverse(g,True)

        while actionlist:
            j=actionlist[-1]
            actionlist=actionlist[:-1]
            self.gm.makeMove(j)
            o=self.gm.getGameState()
            for i in self.currentState.children:
                if i.state==o:
                    self.currentState=i
                    self.visited[i]=True
                    break

        return self.currentState.state==self.victoryCondition


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
        self.q.append(self.currentState)
        if(self.currentState.state == self.victoryCondition):
            self.visited[self.currentState]=True
            return True
        else:
            available_moves = self.gm.getMovables()
            childlist=[]
            #fill out child and currnode attributes
            #also get all children and put em in the childlist
            if available_moves:
                for i in available_moves:
                    self.gm.makeMove(i)
                    tempchild=GameState(self.gm.getGameState(),0,i)
                    self.currentState.children.append(tempchild)
                    tempchild.parent = self.currentState
                    childlist.append(tempchild)
                    self.gm.reverseMove(i)
                #enqueue all states not yet visited to queue
                for i in childlist:
                    if i in self.visited: continue
                    else: self.q.append(i)
            g=None
            it=0
            resultbool=False
            for i in self.q:
                it+=1
                if i not in self.visited:
                    self.m=it
                    resultbool=self.bfs_loop(i)
                    break
            return resultbool
            #return False
