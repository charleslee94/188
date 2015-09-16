# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import sys
import logic

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def getGhostStartStates(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostSearchProblem)
        """
        util.raiseNotDefined()

    def terminalTest(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()
        
    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionSearchProblem
        """
        util.raiseNotDefined()

    def result(self, state, action):
        """
        Given a state and an action, returns resulting state and step cost, which is
        the incremental cost of moving to that successor.
        Returns (next_state, cost)
        """
        util.raiseNotDefined()

    def actions(self, state):
        """
        Given a state, returns available actions.
        Returns a list of actions
        """        
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

    def getWidth(self):
        """
        Returns the width of the playable grid (does not include the external wall)
        Possible x positions for agents will be in range [1,width]
        """
        util.raiseNotDefined()

    def getHeight(self):
        """
        Returns the height of the playable grid (does not include the external wall)
        Possible y positions for agents will be in range [1,height]
        """
        util.raiseNotDefined()

    def isWall(self, position):
        """
        Return true if position (x,y) is a wall. Returns false otherwise.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def atLeastOne(expressions) :
    """
    Given a list of logic.Expr instances, return a single logic.Expr instance in CNF (conjunctive normal form)
    that represents the logic that at least one of the expressions in the list is true.
    >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print logic.pl_true(atleast1,model1)
    False
    >>> model2 = {A:False, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    >>> model3 = {A:True, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    """
    "*** YOUR CODE HERE ***"
    expr = expressions[0]
    for exp in expressions:
        expr = expr | exp
    return expr


def atMostOne(expressions) :
    """
    Given a list of logic.Expr instances, return a single logic.Expr instance in CNF (conjunctive normal form)
    that represents the logic that at most one of the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    expr = expressions[0] | ~expressions[0]
    for exp0 in expressions:
        for exp1 in expressions:
            if exp0 != exp1:
                expr = (~exp0 | ~exp1) & expr
    return expr


def exactlyOne(expressions) :
    """
    Given a list of logic.Expr instances, return a single logic.Expr instance in CNF (conjunctive normal form)
    that represents the logic that exactly one of the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    return atLeastOne(expressions) & atMostOne(expressions)


def extractActionSequence(model, actions):
    """
    Convert a model in to an ordered list of actions.
    model: Propositional logic model stored as a dictionary with keys being
    the symbol strings and values being Boolean: True or False
    Example:
    >>> model = {"North[3]":True, "P[3,4,1]":True, "P[3,3,1]":False, "West[1]":True, "GhostScary":True, "West[3]":False, "South[2]":True, "East[1]":False}
    >>> actions = ['North', 'South', 'East', 'West']
    >>> plan = extractActionSequence(model, actions)
    >>> print plan
    ['West', 'South', 'North']
    """
    timeCnt = 0
    actionList = []
    while timeCnt<=len(actionList):
        for key in model.keys():
            strKey = str(key)
            index = strKey[strKey.index('[')+1 : strKey.index(']')]
            action = strKey[0 : strKey.index('[')]
            if (index == str(timeCnt)) & model[key] & (action in actions):
                actionList.append(action)
        timeCnt+=1
    return actionList


def positionLogicPlan(problem):
    """
    Given an instance of a PositionSearchProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    "*** YOUR CODE HERE ***"
    Directions = ['North', 'South', 'East', 'West']
    start = problem.getStartState()
    goal = problem.getGoalState()
    states = []
    for x in range(0, problem.getWidth()+1):
        for y in range(0, problem.getHeight()+1):
            if not problem.isWall((x,y)):
                states.append((x,y))

    for step in range(util.manhattanDistance(start, goal), 51):
        cnf = []
        cnf.append(logic.PropSymbolExpr('P',start[0],start[1], 0))
        cnf.append(logic.PropSymbolExpr('P',goal[0],goal[1], step))   
        for timeStep in range(0, step + 1):
            cnf.append(exactlyOne([logic.PropSymbolExpr(action,timeStep) for action in Directions]))
            cnf.append(exactlyOne([logic.PropSymbolExpr('P',state[0],state[1], timeStep) for state in states]))
            for state in states:

                actions = problem.actions(state)
                for action in actions:
                    nextState = problem.result(state, action)[0]
                    expr0 = logic.PropSymbolExpr('P',state[0],state[1], timeStep)
                    expr1 = logic.PropSymbolExpr(action,timeStep)
                    expr2 = logic.PropSymbolExpr('P',nextState[0],nextState[1], timeStep+1)
                    cnf.append(logic.to_cnf((expr0 & expr1) >> expr2))

        for state in states:
            lst = []
            exp = None
            for timeStep in range(step + 1):
                lst.append(logic.PropSymbolExpr('P',state[0],state[1],timeStep))
                exp = atMostOne(lst)
            cnf.append(exp)
            newlist = [x for x in list(Directions) if x not in list(problem.actions(state))]
            for action in newlist:
                for timeStep in range(step+1):
                    expr0 = logic.PropSymbolExpr('P',state[0],state[1], timeStep)
                    expr1 = ~logic.PropSymbolExpr(action,timeStep)
                    cnf.append(logic.to_cnf( expr0 >> expr1))

        success = logic.pycoSAT(cnf)
        if success:
            return extractActionSequence(success, Directions)


def foodLogicPlan(problem):
    """
    Given an instance of a FoodSearchProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are gameDirections.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    "*** YOUR CODE HERE ***"
    states = []
    food = []
    gameDirections = ['North', 'South', 'East', 'West']
    fGrid = problem.getStartState()[1]


    for i in range(0,problem.getWidth()+1):
        for j in range(0, problem.getHeight()+1):
            if not problem.isWall((i,j)):
                states.append((i,j))
            if fGrid[i][j]:
                food.append((i,j))
            

    for tLimit in xrange(len(food), 51):
        cnf = []
        for state in states:
            actions = problem.actions((state, fGrid))
            for action in actions:
                for time in xrange(tLimit):
                    nextState = problem.result((state, fGrid), action)[0]
                    expression = (logic.PropSymbolExpr('P', state[0], state[1], time) & logic.PropSymbolExpr(action, time)) >> logic.PropSymbolExpr('P', nextState[0][0], nextState[0][1], time+1)
                    cnf.append(logic.to_cnf(expression))
            for action in list(set(gameDirections)-set(actions)):
                for time in xrange(tLimit):
                    expression = logic.PropSymbolExpr('P', state[0], state[1], time) >> ~logic.PropSymbolExpr(action, time)
                    cnf.append(logic.to_cnf(expression))
        cnf.append(logic.PropSymbolExpr('P', problem.getStartState()[0][0], problem.getStartState()[0][1], 0))
            
        for time in range(0, tLimit):
            cnf.append(exactlyOne([logic.PropSymbolExpr(action,time) for action in gameDirections]))
            cnf.append(exactlyOne([logic.PropSymbolExpr('P', state[0], state[1], time) for state in states]))
            
        for f in food:
            cnf.append(atLeastOne([logic.PropSymbolExpr('P', f[0], f[1], time) for time in range(0, tLimit)]))
    
        model = logic.pycoSAT(cnf)
        if model:
            return extractActionSequence(model, gameDirections)


def foodGhostLogicPlan(problem):
    """
    Given an instance of a FoodGhostSearchProblem, return a list of actions that help Pacman
    eat all of the food and avoid patrolling ghosts.
    Ghosts only move east and west. They always start by moving East, unless they start next to
    and eastern wall. 
    Available actions are gameDirections.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    "*** YOUR CODE HERE ***"
    states = []
    food = []
    gameDirections = ['North', 'South', 'East', 'West']
    fGrid = problem.getStartState()[1]


    for i in range(0,problem.getWidth()+1):
        for j in range(0, problem.getHeight()+1):
            if not problem.isWall((i,j)):
                states.append((i,j))
            if fGrid[i][j]:
                food.append((i,j))
            
    
    for tLimit in range(len(food), 51):
        cnf = []
        for state in states:
            actions = problem.actions((state, fGrid))
            for action in actions:
                for time in range(0, tLimit):
                    nextState = problem.result((state, fGrid), action)[0]
                    expression = (logic.PropSymbolExpr('P', state[0], state[1], time) & logic.PropSymbolExpr(action, time)) >> logic.PropSymbolExpr('P', nextState[0][0], nextState[0][1], time+1)
                    cnf.append(logic.to_cnf(expression))
            for action in list(set(gameDirections)-set(actions)):
                for time in range(0, tLimit):
                    expression = logic.PropSymbolExpr('P', state[0], state[1], time) >> ~logic.PropSymbolExpr(action, time)
                    cnf.append(logic.to_cnf(expression))
        cnf.append(logic.PropSymbolExpr('P', problem.getStartState()[0][0], problem.getStartState()[0][1], 0))
        
        for time in range(0, tLimit):
            cnf.append(exactlyOne([logic.PropSymbolExpr(action,time) for action in gameDirections]))
            cnf.append(exactlyOne([logic.PropSymbolExpr('P', state[0], state[1], time) for state in states]))
            
        for f in food:
            cnf.append(atLeastOne([logic.PropSymbolExpr('P', f[0], f[1], time) for time in range(0, tLimit)]))
        
      
        for x in range(0, len(problem.getGhostStartStates())):
            ghostState = problem.getGhostStartStates()[x]
            ghostPos = ghostState.getPosition()
            cnf.append(logic.PropSymbolExpr('G' + str(x), ghostPos[0], ghostPos[1], 0))
            
            if not problem.isWall((ghostPos[0]+1, ghostPos[1])):
                cnf.append(logic.PropSymbolExpr('G' + str(x), ghostPos[0]+1, ghostPos[1], 1))
            else:
                cnf.append(logic.PropSymbolExpr('G' + str(x), ghostPos[0]-1, ghostPos[1], 1))
                
            ghosts = []
            trav = ghostPos[0]
            ghostY = ghostPos[1]
            while(not problem.isWall((trav, ghostY))):
                ghosts.append((trav, ghostY))
                trav -= 1
            trav = ghostPos[0] + 1
            while(not problem.isWall((trav, ghostY))):
                ghosts.append((trav, ghostY))
                trav += 1
            
            for time in range(0, tLimit + 2):
                for pos in ghosts:
                    east = (pos[0]+1, pos[1])
                    west = (pos[0]-1, pos[1])
                    if problem.isWall(west):
                        expression = logic.PropSymbolExpr('G' + str(x), pos[0], pos[1], time) >> logic.PropSymbolExpr('G' + str(x), pos[0]+1, pos[1], time+1)
                        cnf.append(logic.to_cnf(expression))
                    elif problem.isWall(east):
                        expression = logic.PropSymbolExpr('G' + str(x), pos[0], pos[1], time) >> logic.PropSymbolExpr('G' + str(x), pos[0]-1, pos[1], time+1)
                        cnf.append(logic.to_cnf(expression))
                    elif time != 0:
                        expression = (logic.PropSymbolExpr('G' + str(x), pos[0]-1, pos[1], time -1) & logic.PropSymbolExpr('G' + str(x), pos[0], pos[1], time)) >>logic.PropSymbolExpr('G'+str(x), pos[0]+1, pos[1], time+1)
                        cnf.append(logic.to_cnf(expression))
                        expression = (logic.PropSymbolExpr('G' + str(x), pos[0]+1, pos[1], time-1) & logic.PropSymbolExpr('G' + str(x), pos[0], pos[1], time)) >>logic.PropSymbolExpr('G' + str(x), pos[0]-1, pos[1], time+1)
                        cnf.append(logic.to_cnf(expression))
            for time in range(0, tLimit-1):
                for pos in ghosts:
                    temp = [logic.PropSymbolExpr('P', pos[0], pos[1], time+1)] + [logic.PropSymbolExpr('G' + str(x), pos[0], pos[1], time)]
                    cnf.append(atMostOne(temp))
                    temp = [logic.PropSymbolExpr('P', pos[0], pos[1], time)] + [logic.PropSymbolExpr('G' + str(x), pos[0], pos[1], time)]
                    cnf.append(atMostOne(temp))
        model = logic.pycoSAT(cnf)
        if model:
            return extractActionSequence(model, gameDirections)


# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan
fglp = foodGhostLogicPlan

# Some for the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)



