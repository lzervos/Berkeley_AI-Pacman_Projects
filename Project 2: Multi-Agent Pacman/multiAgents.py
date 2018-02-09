# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

### Between the "agents" minimax,alpha beta ,expectimax there are small differences(one is an evolution of the other)

from util import manhattanDistance
from game import Directions
import random, util,sys

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
        Food=newFood.asList()
        gPos=successorGameState.getGhostPositions()                         ###We have the position of the food and the ghost positions
        FoodDist=[]                                                         ###We have the distance between the pacman,the food and the ghost
        GhostDist=[]

        for food in Food:
            FoodDist.append(manhattanDistance(food,newPos))
        for ghost in gPos:
            GhostDist.append(manhattanDistance(ghost,newPos))

        if currentGameState.getPacmanPosition()==newPos:
            return(-(float("inf")))

        for dist in GhostDist:                                              ###If the ghost is too near(next to pacman) we return(-float("inf")) like we have lost
            if dist<2:
                return (-(float("inf")))                                    ###When there is no food left we return float("inf") like we have won
        if len(FoodDist)==0:                                                ##Finally we return 1000/sum(FoodDist) + 10000/len(FoodDist) as the evaluation of the state
            return float("inf")                                             ###It is not necessary that we put 1000 or 10000 ,the only need is to be large enough contrary to sum(foodDist)
                                                                            ###and len(foodDist) respectively
        return 1000/sum(FoodDist) +10000/len(FoodDist)


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

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        def max_value(gameState,depth):
            Actions=gameState.getLegalActions(0)
            if len(Actions)==0 or gameState.isWin() or gameState.isLose() or depth==self.depth:             ###The trvial situations(state)
                return(self.evaluationFunction(gameState),None)
            w=-(float("inf"))                                                                               ###We are trying to implement the 2 sides of the minimax algorithm the max and the min
            Act=None
            for action in Actions:                                                                          ###In that way that the 2 functions are calling each other is like building the tree(diagrams from tha class)
                sucsValue=min_value(gameState.generateSuccessor(0,action),1,depth)                          #We have the available moves and we are seeking for the "best" one
                sucsValue=sucsValue[0]                                                                      #It is working exactly as the theory of minimax algorithm commands
                if(sucsValue>w):                                                                            #Here we have as start -infinite
                    w,Act=sucsValue,action
            return(w,Act)

        def min_value(gameState,agentID,depth):
            Actions=gameState.getLegalActions(agentID)
            if len(Actions) == 0:
                return(self.evaluationFunction(gameState),None)
            l=float("inf")                                                                                  ###As we see in contrast with max we begin from +infinte
            Act=None
            for action in Actions:
                if(agentID==gameState.getNumAgents() -1):
                    sucsValue=max_value(gameState.generateSuccessor(agentID,action),depth + 1)
                else:
                    sucsValue=min_value(gameState.generateSuccessor(agentID,action),agentID+1,depth)        ###We are doing exactly the opposite from the max "function"
                sucsValue=sucsValue[0]
                if(sucsValue<l):
                    l,Act=sucsValue,action
            return(l,Act)
        max_value=max_value(gameState,0)[1]
        return max_value                                                                                    ###We are starting from the max and it goes as a tree max min max min

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def max_value(gameState,depth,a,b):
            Actions = gameState.getLegalActions(0) # Get actions of pacman
            if len(Actions)==0 or gameState.isWin() or gameState.isLose() or depth==self.depth:
                return (self.evaluationFunction(gameState), None)

            w=-(float("inf"))
            Act=None
                                                                                                            ###We can see that the alpha beta agent is almost the same as the minimax with the difference
                                                                                                            ###that now we have the pruning if w>a or w<b in the 2 "edges"
            for action in Actions:
                sucsValue=min_value(gameState.generateSuccessor(0,action),1,depth,a,b)
                sucsValue=sucsValue[0]
                if w<sucsValue:
                    w,Act=sucsValue,action
                if w>b:
                    return (w,Act)
                a=max(a,w)
            return (w,Act)

        def min_value(gameState,agentID,depth,a,b):
            " Cases checking "
            Actions=gameState.getLegalActions(agentID) # Get the actions of the ghost
            if len(Actions) == 0:
                return (self.evaluationFunction(gameState),None)
                                                                                                            ###As we know from theory the alpha beta algorithms is an improved version
                                                                                                            ###of the minimax in order to "pull through" some time,to have a better time
                                                                                                            ###complexity
            l = float("inf")
            Act = None
            for action in Actions:
                if (agentID == gameState.getNumAgents() - 1):
                    sucsValue = max_value(gameState.generateSuccessor(agentID,action),depth + 1,a,b)
                else:
                    sucsValue = min_value(gameState.generateSuccessor(agentID,action),agentID + 1,depth,a,b)
                sucsValue=sucsValue[0]
                if (sucsValue<l):
                    l,Act=sucsValue,action

                if (l<a):
                    return (l,Act)

                b=min(b,l)

            return(l,Act)                                                                                      ###I think there is nothing else to be said about this agent

        a=-(float("inf"))
        b=float("inf")
        max_value=max_value(gameState,0,a,b)[1]
        return max_value


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
        def max_value(gameState,depth):
            Actions=gameState.getLegalActions(0)
            if len(Actions)==0 or gameState.isWin() or gameState.isLose() or depth==self.depth:   ###The max "function" is exactly the same with the minimax and the difference is at
                return (self.evaluationFunction(gameState),None)                                  ##exp,min "function" that now we have the probability

            w=-(float("inf"))
            Act=None

            for action in Actions:
                sucsValue=exp_value(gameState.generateSuccessor(0,action),1,depth)
                sucsValue=sucsValue[0]
                if(w<sucsValue):
                    w,Act=sucsValue,action                                                          ###Now the expectimax algorithm is the same as the minimax but now we have
                                                                                                    ###also the probability we insert about each move that we maybe do as we 've been taught
                                                                                                    ###in theory,similar things we have in chess and all the other games
            return(w,Act)

        def exp_value(gameState,agentID,depth):
            Actions=gameState.getLegalActions(agentID)
            if len(Actions)==0:
                return (self.evaluationFunction(gameState),None)

            l=0
            Act=None
            for action in Actions:
                if(agentID==gameState.getNumAgents() -1):
                    sucsValue=max_value(gameState.generateSuccessor(agentID,action),depth+1)
                else:
                    sucsValue=exp_value(gameState.generateSuccessor(agentID,action),agentID+1,depth)
                sucsValue=sucsValue[0]
                prob=sucsValue/len(Actions)
                l+=prob
            return(l,Act)

        max_value=max_value(gameState,0)[1]
        return max_value

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pacPosition=currentGameState.getPacmanPosition()                                                     ###Now we do not want only the pacman,the food and the ghost positions
    gList=currentGameState.getGhostStates()                                                              ###but also the capsules
    Food=currentGameState.getFood()
    Capsules=currentGameState.getCapsules()

    if currentGameState.isWin():
        return float("inf")
    if currentGameState.isLose():
        return float("-inf")

    foodDistList=[]
    for food in Food.asList():
        foodDistList+=[util.manhattanDistance(food,pacPosition)]
    minFDist=min(foodDistList)                                                                              ###We have a better evaluation function,what it means?
    GhDistList=[]                                                                                           ###It means that we have take into account more parameters in order to have a better evalution function
    ScGhDistList=[]                                                                                         ###Of course every parameter has its own "gravity,importance" like chess the strategical advantages
    for ghost in gList:                                                                                     ###are less important than the tactical,material ones
        if ghost.scaredTimer==0:
            GhDistList+=[util.manhattanDistance(pacPosition,ghost.getPosition())]
        elif ghost.scaredTimer>0:
            ScGhDistList+=[util.manhattanDistance(pacPosition,ghost.getPosition())]
    minGhDist=-1
    if len(GhDistList) > 0:
        minGhDist=min(GhDistList)                                                                             #We have the min distance of a ghost,the min distance of a scaredGhost,the amount of the capsules,the food and the min distance of a food.
    minScGhDist=-1                                                                                            #As we see they do not hve all the same role-importance in the estimation -evaluation of a state
    if len(ScGhDistList)>0:
        minScGhDist=min(ScGhDistList)
    score=scoreEvaluationFunction(currentGameState)
    score-= 1.5 * minFDist + 2 * (1.0/minGhDist) + 2 * minScGhDist + 20 * len(Capsules) + 4 * len(Food.asList())
    return score
# Abbreviation
better = betterEvaluationFunction
