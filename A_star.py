import numpy as np
import random
from statistics import mean
from pprint import pprint
from copy import copy, deepcopy

class Node():
    # Node class for the A star algorithm
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.c = 0
        self.h = 0
        self.t = 0

    def __eq__(self, other):
        return self.position == other.position

def generateGrid(dim, prob):
    # 0 is free path and 1 is blocked path
    # dim = 10
    grid = []
    for row in range(dim):
        # Add an empty array that will hold each cell
        # in this row
        grid.append([])
        for column in range(dim):
            grid[row].append(int(np.random.binomial(1, 1 - prob, 1)))  # Append a cell
            if row == column == dim - 1:
                grid[row][column] = 0
    grid[0][0] = 0
    grid[dim - 1][dim - 1] = 0
    return grid


def astar(maze, start, end):

    # generate the start and end nodes
    StartNode = Node(None, start)
    StartNode.c = StartNode.h = StartNode.t = 0
    EndNode = Node(None, end)
    EndNode.c = EndNode.h = EndNode.t = 0

    # initializing open and closed lists
    OpenList = []
    ClosedList = []

    # append Start Node to open list
    OpenList.append(StartNode)

    # Keep looping until we find the end node
    while len(OpenList) > 0:

        # extracting the current node
        CurrNode = OpenList[0]
        CurrIndex = 0
        for index, item in enumerate(OpenList):
            if item.t < CurrNode.t:
                CurrNode = item
                CurrIndex = index

        # Pop-ing the current off the open list and appending it to the closed list
        OpenList.pop(CurrIndex)
        ClosedList.append(CurrNode)
        ExploredNodes = len(ClosedList)

        # if we find the goal then:
        if CurrNode == EndNode:
            path = []
            current = CurrNode
            while current is not None:
                path.append(current.position)
                current = current.parent
            return [path[::-1], ExploredNodes]           # we return the reversed path as output

        # We generate the children for the node which was popped from the open list.
        Children = []
        for NewPosition in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares
            # add (-1, -1), (-1, 1), (1, -1), (1, 1) in the above list for travelling diagonally in the maze.
            # knowing the node position
            NodePosition = (CurrNode.position[0] + NewPosition[0], CurrNode.position[1] + NewPosition[1])

            # Verifying if the children are within the boundaries. If they arent then we skip those children
            if NodePosition[0] > (len(maze) - 1) or NodePosition[0] < 0 or NodePosition[1] > (len(maze[len(maze)-1]) -1) or NodePosition[1] < 0:
                continue

            # skip the Child node if there is a blockage i.e. 1
            if maze[NodePosition[0]][NodePosition[1]] != 0:
                continue

            # generate a new node
            NewNode = Node(CurrNode, NodePosition)

            # if the Child node is already in closed list then we ignore it
            if NewNode in ClosedList:
                continue

            # Append the node into children of the node which was popped
            Children.append(NewNode)

        # Loop through Children
        for Child in Children:

            # Child is on the closed list
            for ClosedChild in ClosedList:
                if Child == ClosedChild:
                    continue

            # generating the c, h, and t values for the child
            Child.c = CurrNode.c + 1
            # square of euclidian distance as heuristics
            #Child.h = ((Child.position[0] - EndNode.position[0]) ** 2) +
            # ((Child.position[1] - EndNode.position[1]) ** 2)
            # Manhattan distance heuristic
            Child.h = (abs(EndNode.position[0] - Child.position[0]) + abs(EndNode.position[1] - Child.position[1]))
            Child.t = Child.c + Child.h

            # if the child is already in the open list and the child's
            # current position is greater than current open node position then we skip it
            for OpenNode in OpenList:
                if Child == OpenNode and Child.c > OpenNode.c:
                    continue

            # if child is not in the open list then we add them to it.
            if Child not in OpenList:
                OpenList.append(Child)
    return [None, ExploredNodes]

def mazepath(maze_path, path):
    w = len(maze_path)  # displays the path of the maze with all cells being 1 and path cells as 0.
    for row in range(w):
        for column in range(w):
            if (row, column) in path:
                maze_path[row][column] = 0
            else:
                maze_path[row][column] = 1
    return maze_path


def thinmaze(maze,prob):
    w = len(maze)
    l1 = []
    l2 = []
    c = []
    maze1 = deepcopy(maze)
    for row in range(w):
        for column in range(w):
            if maze[row][column] == 1:
                c = (row, column)
                l1.append(c)      # we append all the (row,column) values where there is a block in a list
    count = round((len(l1))*prob)
    for i in range(0, count):
        a = random.choice(l1) # we randomly pop a point from l1 and add it in a new list l2 for count number of times
        l2.append(a)
        l1.remove(a)
        i += 1
    for row in range(w):
        for column in range(w):
            if (row, column) in l2:
                maze[row][column] = 0   # free (the row,column) in the list l2 and we get a thin maze
    return maze

def thin_heuristic(thin_maze, start_node, end_node):
    thinPath = astar(thin_maze, start_node, end_node)
    return len(thinPath) if thinPath != None else 0

def astar_thinning(maze,thin_maze, start, end):

    # generate the start and end nodes
    StartNode = Node(None, start)
    StartNode.c = StartNode.h = StartNode.t = 0
    EndNode = Node(None, end)
    EndNode.c = EndNode.h = EndNode.t = 0

    # initializing open and closed lists
    OpenList = []
    ClosedList = []

    # append Start Node to open list
    OpenList.append(StartNode)

    # Keep looping until we find the end node
    while len(OpenList) > 0:

        # extracting the current node
        CurrNode = OpenList[0]
        CurrIndex = 0
        for index, item in enumerate(OpenList):
            if item.t < CurrNode.t:
                CurrNode = item
                CurrIndex = index

        # Pop-ing the current off the open list and appending it to the closed list
        OpenList.pop(CurrIndex)
        ClosedList.append(CurrNode)
        ExploredNodesAfterThinning = len(ClosedList)

        # if we find the goal then:
        if CurrNode == EndNode:
            path = []
            current = CurrNode
            while current is not None:
                path.append(current.position)
                current = current.parent
            return [path[::-1], ExploredNodesAfterThinning]      # we return the reversed path as output

        # We generate the children for the node which was popped from the open list.
        Children = []
        for NewPosition in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares
            # add (-1, -1), (-1, 1), (1, -1), (1, 1) in the above list for travelling diagonally in the maze.
            # knowing the node position
            NodePosition = (CurrNode.position[0] + NewPosition[0], CurrNode.position[1] + NewPosition[1])

            # Verifying if the children are within the boundaries. If they arent then we skip those children
            if NodePosition[0] > (len(maze) - 1) or NodePosition[0] < 0 or NodePosition[1] > (len(maze[len(maze)-1]) -1) or NodePosition[1] < 0:
                continue

            # skip the Child node if there is a blockage i.e. 1
            if maze[NodePosition[0]][NodePosition[1]] != 0:
                continue

            # generate a new node
            NewNode = Node(CurrNode, NodePosition)

            # if the Child node is already in closed list then we ignore it
            if NewNode in ClosedList:
                continue
            # Append the node into children of the node which was popped
            Children.append(NewNode)

        # Loop through the Children
        for Child in Children:
            # Child is on the closed list
            for ClosedChild in ClosedList:
                if Child == ClosedChild:
                    continue
            # generating the c, h, and t values for the child
            Child.c = CurrNode.c + 1
            # Thin MAZE heuristic
            Child.h = thin_heuristic(thin_maze, Child.position, EndNode.position)
            Child.t = Child.c + Child.h

            # Child is already in the open list
            for OpenNode in OpenList:
                if Child == OpenNode and Child.c > OpenNode.c:
                    continue
            # if child is not in the open list then we add them to it.
            if Child not in OpenList:
                OpenList.append(Child)
    return [None, ExploredNodesAfterThinning]


def main():
    trails = 1000
    # removing (rho*100) % of the obstacles from the maze
    L1 = []
    L2 = []
    for r in range(1, 10):
        rho = round(r*(0.1), 1)
        for i in range(1, trails + 1):
            maze = generateGrid(10, 0.7)
            start = (0, 0)
            end = (9, 9)
            path_and_ExploredNodes = astar(maze, start, end)
            path = path_and_ExploredNodes[0]
            Explored_Nodes = path_and_ExploredNodes[1]
            if path == None:
                continue
            else:
                L1.append(Explored_Nodes)
                maze1 = mazepath(maze, path)
                #pprint(maze1)
            # removing a fraction of obstacles in the maze
            thin_maze = thinmaze(maze, rho)
            thin_path_and_ExploredNodes = astar_thinning(maze,thin_maze, start, end)
            thin_path = thin_path_and_ExploredNodes[0]
            Explored_Nodes_thinning = thin_path_and_ExploredNodes[1]
            if thin_path == None:
                continue
            else:
                maze2 = mazepath(maze, thin_path)
                L2.append(Explored_Nodes_thinning)
                #pprint(maze2)
            i += 1
        Avg_NodesExplored = round(mean(L1))
        Avg_NodesExplored_AfterThinning = round(mean(L2))
        print("RHO value:", rho)
        print("Nodes explored before thinning:", Avg_NodesExplored)
        print("Nodes explored after thinning:", Avg_NodesExplored_AfterThinning)

if __name__ == '__main__':
    thin_path = []
    main()



