# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        fmd = newFood.height + newFood.width
        mDistGhost = fmd
        for ghost in successorGameState.getGhostStates():
          mDistGhost = min(mDistGhost, manhattanDistance(newPos, ghost.getPosition()))
        foodlist = newFood.asList()
        fdist= []
        opfdist = 0
        if not len(foodlist) == 0:
          for food in foodlist:
            fdist.append(manhattanDistance(newPos, food))
            opfdist = min(fdist)
        if mDistGhost > 3:
          priority = [0, 10000000, 1000] #ghostdist, food left, food dist
        else:
          priority = [100000, 0, 0]
        fval = fmd - len(foodlist)
        fdval = fmd - opfdist
        score = priority[0] * mDistGhost + priority[1] * fval + priority[2] * fdval
        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent & AlphaBetaPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 7)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        return self.maxPac(self.depth, gameState)[1]

    def maxPac(self, depth, currentGameState):
      curmax = None
      pActions = currentGameState.getLegalActions(0)
      if len(pActions) == 0 or currentGameState.isWin():
        curmax = (self.evaluationFunction(currentGameState), None)
      else:
        for action in pActions:
          next = currentGameState.generateSuccessor(0, action)
          stateval = self.minGhost(depth, 1, next)[0]
          if curmax==None or stateval >  curmax[0]:
            curmax = (stateval, action)
      return curmax

    def minGhost(self, depth, agentNumber, currentGameState):
      curmin = None
      gActions = currentGameState.getLegalActions(agentNumber)
      if len(gActions) == 0 or currentGameState.isLose():  #Terminal State: NO LEGAL MOVES
        curmin = (self.evaluationFunction(currentGameState), None)
      else:
        for action in gActions:
          nxt = currentGameState.generateSuccessor(agentNumber, action)
          stateval = 0
          if agentNumber + 1 == currentGameState.getNumAgents(): 
            if depth == 1: 
              stateval = self.evaluationFunction(nxt)
            else: 
              stateval = self.maxPac(depth - 1, nxt)[0]
          else: 
            stateval = self.minGhost(depth, agentNumber + 1, nxt)[0]
          if curmin==None or stateval<curmin[0]:
            curmin = (stateval, action)
      return curmin

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 8)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        return self.maxPac(self.depth, gameState)[1]

    def maxPac(self, depth, currentGameState):
        curmax = None
        pActions = currentGameState.getLegalActions(0)
        if len(pActions) == 0 or currentGameState.isWin():
          curmax = (self.evaluationFunction(currentGameState), None)
        else:
          for action in pActions:
            next = currentGameState.generateSuccessor(0, action)
            stateval = self.expectG(depth, 1, next)
            if curmax==None or stateval >  curmax[0]:
              curmax = (stateval, action)
        return curmax

    def expectG(self, depth, agentNumber, currentGameState):
          exp = 0
          gActions = currentGameState.getLegalActions(agentNumber)
          if len(gActions) == 0:
            return self.evaluationFunction(currentGameState)
          if currentGameState.isLose():
            exp = self.evaluationFunction(currentGameState)
          for action in gActions:
            nxt = currentGameState.generateSuccessor(agentNumber, action)
            stateval = 0
            if agentNumber + 1 == currentGameState.getNumAgents(): 
              if depth == 1: 
                stateval = self.evaluationFunction(nxt)
              else: 
                stateval = self.maxPac(depth - 1, nxt)[0]
            else: 
              stateval = self.expectG(depth, agentNumber + 1, nxt)
            exp += stateval
          average = exp/len(gActions)
          return average

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 9).

      DESCRIPTION: <write something here so we know what you did>
      Takes current score (which factors in the time)
      Checks ghosts 
        Distance away from not scared ghosts  (more is better)
        Distance away from scared ghosts (less is better)
      Checks food 
        Distance away from closest food (less is better)
        Amount of food (less is better)
      Checks power pellets
        Distance away from closest power pellet (less is better)
      Checks if surrounded by walls
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghosts = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghosts]
    score = currentGameState.getScore()
    notScaredDistances = []
    scaredDistances = []
    for ghost in ghosts:
      if ghost.scaredTimer<=0:
        notScaredDistances.append(manhattanDistance(pos, ghost.getPosition()))
      else:
        scaredDistances.append(manhattanDistance(pos, ghost.getPosition()))
    foodList = food.asList()
    foodDistances = []
    for fpos in foodList:
      foodDistances.append(manhattanDistance(pos, fpos))
    powPell = currentGameState.getCapsules()
    capDistance = []
    ghostCapDistance = []
    for capsule in powPell:
      for ghost in ghosts:
        ghostCapDistance.append(manhattanDistance(ghost.getPosition(), capsule))
      if ghostCapDistance:
        capDistance.append(manhattanDistance(pos, capsule))
      else:
          capDistance.append(manhattanDistance(pos, capsule))
    
    

    if scaredDistances:
      score = score + 1.0/min(scaredDistances)
    elif notScaredDistances:
      if min(notScaredDistances)<3:
        return 0


      
    
    if foodDistances:
      score = score + 1.0/min(foodDistances)
    if foodList:
      score = score + 1.0/len(foodList)
    if capDistance:
      score = score + 1.0/min(capDistance) + min(ghostCapDistance)
    return score

# Abbreviation
better = betterEvaluationFunction
