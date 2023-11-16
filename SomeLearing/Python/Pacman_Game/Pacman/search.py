# search.py
# ---------
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from util import PriorityQueue


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

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
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
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    from util import Stack

    st = Stack()
    visited = []
    path = []

    # if the start state is goal, return the path.
    startPosition = problem.getStartState()
    if problem.isGoalState(startPosition):
        return path

    # push the start position to the stack with 0 cost.
    st.push((startPosition, path, 0))

    while not st.isEmpty():
        currentNode = st.pop()
        position, path = currentNode[0], currentNode[1]

        # If the current position is goal, return the path.
        if problem.isGoalState(position):
            return path

        if position not in visited:
            visited.append(position)

        # Gets successors of the current node.
        successors = problem.getSuccessors(position)

        # push the current node's children to the stack if they are not visited.
        for item in successors:
            currentPosition, currentPath, currentPrice = item[0], item[1], item[2]
            if currentPosition not in visited:
                newPosition = currentPosition
                newPath = path + [currentPath]
                st.push((newPosition, newPath, currentPrice))

    util.raiseNotDefined()


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    from util import Queue

    # Creates an empty Queue.
    queue = Queue()

    visited = []
    path = []
    action_cost = 0  # Cost of each movement.

    # if the start state is goal, return the path.
    startPosition = problem.getStartState()
    if problem.isGoalState(startPosition):
        return path

    # push the start position to the Queue.
    queue.push((startPosition, path, action_cost))

    while not queue.isEmpty():

        currentNode = queue.pop()
        position = currentNode[0]
        path = currentNode[1]

        # push the current position to the visited list if it is not visited.
        if position not in visited:
            visited.append(position)

        # Returns the final path if the current position is goal.
        if problem.isGoalState(position):
            return path

        # Gets successors of the current node.
        successors = problem.getSuccessors(position)

        # push the current node's successors to the Queue if they are not visited.
        # We check both visited and open list.
        for item in successors:
            currentPosition, currentPath, currentPrice = item[0], item[1], item[2]
            if currentPosition not in visited and currentPosition not in (node[0] for node in queue.list):
                newPosition = currentPosition
                newPath = path + [currentPath]
                queue.push((newPosition, newPath, currentPrice))

    util.raiseNotDefined()


def uniformCostSearch(problem: SearchProblem):

    pq = PriorityQueue()

    visited = []
    path = []

    startPosition = problem.getStartState()
    if problem.isGoalState(startPosition):
        return path

    # push the start position to the PriorityQueue.
    pq.push((startPosition, path), 0)

    while not pq.isEmpty():

        currentNode = pq.pop()
        position = currentNode[0]
        path = currentNode[1]

        # push the current position to the visited list if it is not visited.
        if position not in visited:
            visited.append(position)

        # Returns the final path if the current position is goal.
        if problem.isGoalState(position):
            return path

        # Gets successors of the current node.
        successors = problem.getSuccessors(position)

        # We defined a function in order to get the priority of an existing node in the open list.
        def getPriorityOfNode(pq, node):
            for item in pq.heap:
                if item[2][0] == node:
                    return problem.getCostOfActions(item[2][1])

        # push the current node's successors to the PriorityQueue if they are neither in the visited list nor in the open list.
        for item in successors:
            currentPosition, currentPath = item[0], item[1]
            if currentPosition not in visited and (currentPosition not in (node[2][0] for node in pq.heap)):
                newPath = path + [currentPath]
                newPriority = problem.getCostOfActions(newPath)
                pq.push((currentPosition, newPath), newPriority)

            # If the successor is already in the open list, we check its priority.
            elif currentPosition not in visited and (currentPosition in (node[2][0] for node in pq.heap)):
                oldPriority = getPriorityOfNode(pq, currentPosition)
                newPriority = problem.getCostOfActions(newPath)

                # Updates priority of the successor if the value of new priority is less than that of the old one.
                if oldPriority > newPriority:
                    newPath = path + [currentPath]
                    pq.update((currentPosition, newPath), newPriority)

    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    # Creates an empty PriorityQueue.
    pq = PriorityQueue()

    visited = []
    path = []

    startPosition = problem.getStartState()
    if problem.isGoalState(startPosition):
        return path

    pq.push((startPosition, path), 0)

    while not pq.isEmpty():
        currentNode = pq.pop()
        position, path = currentNode[0], currentNode[1]

        # Returns the final path if the current position is goal.
        if problem.isGoalState(position):
            return path

        # push the current position to the visited list if it is not visited.
        if position not in visited:
            visited.append(position)

            # Gets successors of the current node.
            successors = problem.getSuccessors(position)

            # push the current children to the queue if they're not visited.
            for item in successors:
                currentPosition, currentPath = item[0], item[1]
                if currentPosition not in visited:
                    newPosition = currentPosition
                    newPath = path + [currentPath]
                    newPriority = problem.getCostOfActions(
                        newPath) + heuristic(newPosition, problem)
                    pq.push((newPosition, newPath), newPriority)

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch