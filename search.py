# search.py
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
    return  [s, s, w, s, w, w, s, w]




def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """




    visited = {}
    solution = []
    stack = util.Stack()
    parents = {}


    start = problem.getStartState()
    stack.push((start, 'Undefined', 0))
    visited[start] = 'Undefined'

    # return if start state itself is the goal
    if problem.isGoalState(start):
        return solution

    # loop while stack is not empty and goal is not reached
    goal = False;
    while(stack.isEmpty() != True and goal != True):

        node = stack.pop()

        visited[node[0]] = node[1]
        # check if element is goal
        if problem.isGoalState(node[0]):
            node_sol = node[0]
            goal = True
            break

        for pos in problem.getSuccessors(node[0]):
            if pos[0] not in visited.keys():
                parents[pos[0]] = node[0]
                stack.push(pos)

    # finding and storing the path
    while(node_sol in parents.keys()):
        node_sol_prev = parents[node_sol]
        solution.insert(0, visited[node_sol])
        node_sol = node_sol_prev

    return solution



def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""




    visited = {}
    solution = []
    queue = util.Queue()
    parents = {}

    start = problem.getStartState()
    queue.push((start, 'Undefined', 0))
    visited[start] = 'Undefined'

    if problem.isGoalState(start):
        return solution

    goal = False;
    while(queue.isEmpty() != True and goal != True):
        node = queue.pop()
        visited[node[0]] = node[1]
        if problem.isGoalState(node[0]):
            node_sol = node[0]
            goal = True
            break
        for pos in problem.getSuccessors(node[0]):
            if pos[0] not in visited.keys() and pos[0] not in parents.keys():
                parents[pos[0]] = node[0]
                queue.push(pos)

    while(node_sol in parents.keys()):
        node_sol_prev = parents[node_sol]
        solution.insert(0, visited[node_sol])
        node_sol = node_sol_prev

    return solution



def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    '''This function pushes non-visited nodes onto the priority queue.
    Nodes are popped one by one, and the following steps are performed:
    1. The node is marked as visited.
    2. If it is a goal node, the loop stops, and the solution is obtained by backtracking using stored parents.
    3. If it is not a goal node, it is expanded.
    4. If the successor node is not visited, its cost is calculated.
    5. If the cost of the successor node was calculated earlier while expanding a different node,
       and if the new calculated cost is less than old cost, then the cost and parent are updated,
       and it is pushed onto the priority queue with new cost as priority.'''

    # initializations

    # "visited" contains nodes which have been popped from the queue,
    # and the direction from which they were obtained
    visited = {}
    # "solution" contains the sequence of directions for Pacman to get to the goal state
    solution = []
    # "queue" contains triplets of: (nodes in the fringe list, direction, cost)
    queue = util.PriorityQueue()
    # "parents" contains nodes and their parents
    parents = {}
    # "cost" contains nodes and their corresponding costs
    cost = {}

    # start state is obtained and added to the queue
    start = problem.getStartState()
    queue.push((start, 'Undefined', 0), 0)
    # the direction from which we arrived in the start state is undefined
    visited[start] = 'Undefined'
    # cost of start state is 0
    cost[start] = 0

    # return if start state itself is the goal
    if problem.isGoalState(start):
        return solution

    # loop while queue is not empty and goal is not reached
    goal = False;
    while(queue.isEmpty() != True and goal != True):
        # pop from top of queue
        node = queue.pop()
        # store element and its direction
        visited[node[0]] = node[1]
        # check if element is goal
        if problem.isGoalState(node[0]):
            node_sol = node[0]
            goal = True
            break
        # expand node
        for pos in problem.getSuccessors(node[0]):
            # if successor is not visited, calculate its new cost
            if pos[0] not in visited.keys():
                priority = node[2] + pos[2]
                # if cost of successor was calculated earlier while expanding a different node,
                # if new cost is more than old cost, continue
                if pos[0] in cost.keys():
                    if cost[pos[0]] <= priority:
                        continue
                # if new cost is less than old cost, push to queue and change cost and parent
                queue.push((pos[0], pos[1], priority), priority)
                cost[pos[0]] = priority
                # store successor and its parent
                parents[pos[0]] = node[0]

    # finding and storing the path
    while(node_sol in parents.keys()):
        # find parent
        node_sol_prev = parents[node_sol]
        # prepend direction to solution
        solution.insert(0, visited[node_sol])
        # go to previous node
        node_sol = node_sol_prev

    return solution



def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0




def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    '''This function pushes non-visited nodes onto the priority queue.
    Nodes are popped one by one, and the following steps are performed:
    1. The node is marked as visited.
    2. If it is a goal node, the loop stops, and the solution is obtained by backtracking using stored parents.
    3. If it is not a goal node, it is expanded.
    4. If the successor node is not visited, its cost is calculated using the heuristic function.
    5. If the cost of the successor node was calculated earlier while expanding a different node,
       and if the new calculated cost is less than old cost, then the cost and parent are updated,
       and it is pushed onto the priority queue with new cost as priority.'''

    # initializations

    # "visited" contains nodes which have been popped from the queue,
    # and the direction from which they were obtained
    visited = {}
    # "solution" contains the sequence of directions for Pacman to get to the goal state
    solution = []
    # "queue" contains triplets of: (node in the fringe list, direction, cost)
    queue = util.PriorityQueue()
    # "parents" contains nodes and their parents
    parents = {}
    # "cost" contains nodes and their corresponding costs
    cost = {}

    # start state is obtained and added to the queue
    start = problem.getStartState()
    queue.push((start, 'Undefined', 0), 0)
    # the direction from which we arrived in the start state is undefined
    visited[start] = 'Undefined'
    # cost of start state is 0
    cost[start] = 0

    # return if start state itself is the goal
    if problem.isGoalState(start):
        return solution

    # loop while queue is not empty and goal is not reached
    goal = False;
    while(queue.isEmpty() != True and goal != True):
        # pop from top of queue
        node = queue.pop()
        # store element and its direction
        visited[node[0]] = node[1]
        # check if element is goal
        if problem.isGoalState(node[0]):
            node_sol = node[0]
            goal = True
            break
        # expand node
        for pos in problem.getSuccessors(node[0]):
            # if successor is not visited, calculate its new cost
            if pos[0] not in visited.keys():
                priority = node[2] + pos[2] + heuristic(pos[0], problem)
                # if cost of successor was calculated earlier while expanding a different node,
                # if new cost is more than old cost, continue
                if pos[0] in cost.keys():
                    if cost[pos[0]] <= priority:
                        continue
                # if new cost is less than old cost, push to queue and change cost and parent
                queue.push((pos[0], pos[1], node[2] + pos[2]), priority)
                cost[pos[0]] = priority
                # store successor and its parent
                parents[pos[0]] = node[0]

    # finding and storing the path
    while(node_sol in parents.keys()):
        # find parent
        node_sol_prev = parents[node_sol]
        # prepend direction to solution
        solution.insert(0, visited[node_sol])
        # go to previous node
        node_sol = node_sol_prev

    return solution




# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
