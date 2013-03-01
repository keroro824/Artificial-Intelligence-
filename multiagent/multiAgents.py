# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

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

    "*** YOUR CODE HERE ***"
    Foodlist = newFood.asList()
    listDis1 = []
    listDis2 = []
    for elem in Foodlist:
        listDis1.append(1.0/util.manhattanDistance(newPos, elem))
    for elem in newGhostStates:
        dis = util.manhattanDistance(newPos, elem.getPosition())
        if dis!=0.0 and dis<3:
            listDis2.append(1.0/dis)
    foodTotal = sum(listDis1)
    ghostTotal = sum(listDis2)
    return successorGameState.getScore()+foodTotal-28*ghostTotal
    

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
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

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
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    move = gameState.getLegalActions(0)
    if Directions.STOP in move:
        move.remove(Directions.STOP)
    List = []
    List2 = []

    for elem in move:
        state = gameState.generateSuccessor(0,elem)
        depth = (self.depth * gameState.getNumAgents())-1
        List.append(self.MINI_MAX(state, depth))
    Score = max(List)
    i=0
    while(i!=len(List)):
        if List[i]==Score:
            List2.append(i)
        i+=1
    return move[random.choice(List2)]
     
  def Terminate(self,depth, state): 
       if (depth<=0 or state.isWin() or state.isLose()):
           return True
       return False
       
  def MINI_MAX(self, state, depth):
    if self.Terminate(depth,state):
        return self.evaluationFunction(state)
    agent = depth % state.getNumAgents()
    if (agent==0):
        score = float("-inf")
    else:
        score = float("inf")
    move = state.getLegalActions(agent)
    for elem in move:
        rec = self.MINI_MAX(state.generateSuccessor(agent, elem), depth - 1)
        if agent==0:
            score =  max(score, rec)
        else:
            score =  min(score, rec)
    return score

    
class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    move = gameState.getLegalActions(0)
    if Directions.STOP in move:
        move.remove(Directions.STOP)
    alpha = float("-inf")
    beta = float("inf")
    List = []
    List2 = []

    for elem in move:
        state = gameState.generateSuccessor(0,elem)
        depth = (self.depth * gameState.getNumAgents())-1
        score = self.ALPHA_BETA(state, depth, alpha, beta)
        List.append(score)
        alpha = max(alpha,score)
    Score = max(List)
    i=0
    while(i!=len(List)):
        if List[i]==Score:
            List2.append(i)
        i+=1
    return move[random.choice(List2)]
      
  def Terminate(self,depth, state): 
       if (depth<=0 or state.isWin() or state.isLose()):
           return True
       return False
       
  def ALPHA_BETA(self, state, depth, alpha, beta):
    if self.Terminate(depth,state):
        return self.evaluationFunction(state)
    agent = depth % state.getNumAgents()
    move = state.getLegalActions(agent)
    for elem in move:
        rec = self.ALPHA_BETA(state.generateSuccessor(agent, elem), depth - 1, alpha, beta)
        if agent==0:
            alpha = max(alpha, rec)
            if beta<=alpha:
                break
        else:
            beta =  min(beta, rec)
            if beta<=alpha: 
                break
    if agent==0:
        return alpha
    return beta


class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    move = gameState.getLegalActions(0)
    if Directions.STOP in move:
        move.remove(Directions.STOP)
    List = []
    List2 = []

    for elem in move:
        state = gameState.generateSuccessor(0,elem)
        depth = (self.depth * gameState.getNumAgents())-1
        List.append(self.EXPECTI_MAX(state, depth))
    Score = max(List)
    i=0
    while(i!=len(List)):
        if List[i]==Score:
            List2.append(i)
        i+=1
    return move[random.choice(List2)]


        
  def Terminate(self,depth, state): 
       if (depth<=0 or state.isWin() or state.isLose()):
           return True
       return False
       
  def EXPECTI_MAX(self, state, depth):
    if self.Terminate(depth,state):
        return self.evaluationFunction(state)
    agent = depth % state.getNumAgents()
    if (agent==0):
        alpha = float("-inf")
    else:
        alpha = 0
    move = state.getLegalActions(agent)
    for elem in move:
        rec = self.EXPECTI_MAX(state.generateSuccessor(agent, elem), depth - 1)
        if agent==0:
            alpha =  max(alpha, rec)
        else:
            alpha+=  rec/len(move)
    return alpha

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <I add the score of the scared time of the ghosts when counting the final 
    score of the currentGameState and use almost exactly the same evaluation function as 
    question one(I thought we have to come up with a very good evaluation function there, so
    I did a lot of work there. The distance of the food and the distance between the current 
    position between pacman and ghost are the two significant factor in deciding the score. 
    And I sum the reciprocal of food distance and then minus the sum of reciprocal of the 
    suitable ghost distance. For scared times, because the longer the time is, the higher 
    winning rate the pacman has. Therefore I use the result add the summation of the scared
    time >
  """
  "*** YOUR CODE HERE ***"

  newPos = currentGameState.getPacmanPosition()
  newFood = currentGameState.getFood()
  newGhostStates = currentGameState.getGhostStates()
  newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
  Foodlist = newFood.asList()
  listDis1 = []
  listDis2 = []
  for elem in Foodlist:
      listDis1.append(1.0/util.manhattanDistance(newPos, elem))
  for elem in newGhostStates:
      dis = util.manhattanDistance(newPos, elem.getPosition())
      if dis!=0.0 and dis<3:
          listDis2.append(1.0/dis)
  foodTotal = sum(listDis1)
  ghostTotal = sum(listDis2)
  scaredScore = sum(newScaredTimes)
  return currentGameState.getScore()+foodTotal-28*ghostTotal+scaredScore*1.2


# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

