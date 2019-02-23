from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        peg1facts = self.kb.kb_ask(parse_input("fact: (on ?d peg1)"))
        peg2facts = self.kb.kb_ask(parse_input("fact: (on ?d peg2)"))
        peg3facts = self.kb.kb_ask(parse_input("fact: (on ?d peg3)"))

        temp1=[]
        if not peg1facts:
            pass
        else:
            for answer in peg1facts:
                if (not answer):
                    continue
                reply = str(answer)
                #print(reply)
                #print(int(reply[-1]))
                temp1.append(int(reply[-1]))
        temp1.sort()
        temp2=[]
        if not peg2facts:
            pass
        else:
            for answer in peg2facts:
                if (not answer):
                    continue
                reply = str(answer)
                #print(reply)
                #print(int(reply[-1]))
                temp2.append(int(reply[-1]))
        p3 = list()
        temp2.sort()
        temp3=[]
        if not peg3facts:
            pass
        else:
            for answer in peg3facts:
                if (not answer):
                    continue
                reply = str(answer)
                #print(reply)
                #print(int(reply[-1]))
                temp3.append(int(reply[-1]))
        temp3.sort()
        #print((tuple(temp1),tuple(temp2),tuple(temp3)))
        return(tuple(temp1),tuple(temp2),tuple(temp3))


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        if GameMaster.isMovableLegal(self,movable_statement):
            terms = movable_statement.terms
            disk = str(terms[0].term.element)
            origin = str(terms[1].term.element)
            target = str(terms[2].term.element)
            pegnum = int(origin[-1])

            #if the target has a top, retract that it's the top
            oldtop = self.kb.kb_ask(parse_input("fact: (top ?disk "+target+")"))
            if(oldtop):
                self.kb.kb_retract(parse_input("fact: (top " + oldtop[0].bindings[0].constant.element + " " + target + ")"))

            #retract that the disk is on the origin
            self.kb.kb_retract(parse_input("fact: (on "+disk+" "+origin+")"))
            #retract that the target is empty
            self.kb.kb_retract(parse_input("fact: (empty "+target+")"))
            #retract that the disk is on the top of the origin
            self.kb.kb_retract(parse_input("fact: (top " + disk + " " + origin + ")"))
            #assert that the disk is the top of the target
            self.kb.kb_assert(parse_input("fact: (top " + disk + " " + target + ")"))
            #assert that the disk is on the target
            self.kb.kb_assert(parse_input("fact: (on "+disk+" "+target+")"))

            gms = self.getGameState()
            if not gms[pegnum - 1]:
                self.kb.kb_assert(parse_input("fact: (empty "+origin+")"))
            else:
                self.kb.kb_assert(parse_input("fact: (top disk"+str(gms[pegnum-1][0])+ " "+origin+")"))

            return


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        row1facts=self.kb.kb_ask(parse_input("fact: (pos ?t ?c pos1)"))
        row2facts=self.kb.kb_ask(parse_input("fact: (pos ?t ?c pos2)"))
        row3facts=self.kb.kb_ask(parse_input("fact: (pos ?t ?c pos3)"))

        #print(row1facts)
        row1=[None]*3
        row2=[None]*3
        row3=[None]*3

        #for i in range(3):
        for i in range(3):

            tmp1=str(row1facts[i].bindings_dict["?t"])[-1]
            tmp1c=str(row1facts[i].bindings_dict["?c"])[-1]

            tmp2=str(row2facts[i].bindings_dict["?t"])[-1]
            tmp2c=str(row2facts[i].bindings_dict["?c"])[-1]

            tmp3=str(row3facts[i].bindings_dict["?t"])[-1]
            tmp3c=str(row3facts[i].bindings_dict["?c"])[-1]

            if tmp1 == "y":
                tmp1=-1
            if tmp2 == "y":
                tmp2=-1
            if tmp3 == "y":
                tmp3=-1

            row1[int(tmp1c)-1]=int(tmp1)
            row2[int(tmp2c)-1]=int(tmp2)
            row3[int(tmp3c)-1]=int(tmp3)

        #print((tuple(row1),tuple(row2),tuple(row3)))
        return(tuple(row1),tuple(row2),tuple(row3))


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        if GameMaster.isMovableLegal(self,movable_statement):
            terms = movable_statement.terms
            tile = str(terms[0].term.element)
            ocol = str(terms[1].term.element)
            orow = str(terms[2].term.element)
            tcol = str(terms[3].term.element)
            trow = str(terms[4].term.element)

            #retract position of tile at the original coords
            self.kb.kb_retract(parse_input("fact: (pos "+ tile + " "+ ocol +" "+orow+")"))
            #assert position of tile at the target coords
            self.kb.kb_assert(parse_input("fact: (pos "+tile + " "+ tcol +" "+trow+")"))
            #retract position of empty at the target coords
            self.kb.kb_retract(parse_input("fact: (pos empty " + tcol+ " "+ trow +")"))
            #assert position of empty at the original coords
            self.kb.kb_assert(parse_input("fact: (pos empty " + ocol+ " "+orow +")"))
        #pass
        return

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
