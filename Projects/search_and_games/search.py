# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def iterativeDeepeningSearch(problem):
    """
    Perform DFS with increasingly larger depth.

    Begin with a depth of 1 and increment depth by 1 at every step.
    """
    "*** YOUR CODE HERE ***"
    i = 1
    print problem.isGoalState((1,1))
    while True:
        result = DLS(problem, i)
        print i
        print result
        print
        if result is not "cutoff":
            return result
        i = i+1
    return "Error with searching"

def DLS(problem, depth):
    discovered = set()
    node = (problem.getStartState(), [], 0, 0)
    fringe = util.Stack()
    fringe.push(node)
    while not fringe.isEmpty():
        node = fringe.pop()
        if problem.isGoalState(node[0]):
            return node[1]
        if node[3] < depth:
            for i in problem.getSuccessors(node[0]):
                if i[0] not in discovered:
                    discovered.add(i[0])
                    tempList = list(node[1])
                    tempList.append(i[1])
                    tempDepth = node[3] + 1
                    tempNode = (i[0], tempList, 1, tempDepth)
                    fringe.push(tempNode)
    return "cutoff"

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    [2nd Edition: p 73, 3rd Edition: p 82]
    """
    discovered = set([])
    frontier = util.Queue()
    node = (problem.getStartState(), [], 0, 0)
    frontier.push(node)
    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.isGoalState(node[0]):
            return node[1]
        if node[0] not in discovered:
            discovered.add(node[0])
            for i in problem.getSuccessors(node[0]):
                tempList = list(node[1])
                tempList.append(i[1])
                tempCost = node[2] + i[2]
                tempNode = (i[0], tempList, tempCost)
                frontier.push(tempNode)
    return "Error with searching"

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    discovered = set([])
    frontier = util.PriorityQueue()
    node = (problem.getStartState(), [], 0)
    frontier.push(node, heuristic(problem.getStartState(), problem))
    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.isGoalState(node[0]):
            print str(node[1])
            return node[1]
        if node[0] not in discovered:
            discovered.add(node[0])
            for i in problem.getSuccessors(node[0]):
                tempList = list(node[1])
                tempList.append(i[1])
                tempCost = node[2] + i[2]
                tempNode = (i[0], tempList, tempCost)
                frontier.push(tempNode, heuristic(i[0], problem) + tempCost)
    return "Error with searching"


# Abbreviations
bfs = breadthFirstSearch
astar = aStarSearch
ids = iterativeDeepeningSearch