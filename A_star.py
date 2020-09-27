import numpy as np
from pprint import pprint

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def generateGrid(dim, prob):
    # dim = 10
    grid = []
    for row in range(dim):
        # Add an empty array that will hold each cell
        # in this row
        grid.append([])
        for column in range(dim):
            grid[row].append(int(np.random.binomial(1, 1- prob, 1)))  # Append a cell
            if row == column == dim - 1:
                grid[row][column] = 0
    grid[0][0] = 0
    grid[dim - 1][dim - 1] = 0
    return grid


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares
            # add (-1, -1), (-1, 1), (1, -1), (1, 1) in the above list for travelling diagonally in the maze.
            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure the children are within the maze boundaries
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # skip if the child node is a blockage i.e. 1
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # if the child node is already in closed list then we ignore it
            if new_node in closed_list:
                continue

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            # square of euclidian distance as heuristics
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            # Manhattan distance heuristic
            #child.h = (abs(end_node.position[0] - child.position[0]) + abs(end_node.position[1] - child.position[1]))
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            if child not in open_list:
                open_list.append(child)
        #print(len(open_list))

def mazepath(maze, path):
    w = len(maze)
    for row in range(w):
        for column in range(w):
            if (row, column) in path:
                maze[row][column] = 0
            else:
                maze[row][column] = 1
    return maze

def main():
    trails = 100
    success = 0
    failure = 0
    for i in range(0, trails):
        maze = generateGrid(10, 0.7)
        #0 is free path and 1 is blocked path
        start = (0, 0)
        end = (9, 9)
        path = astar(maze, start, end)
        if path == None:
            print('No path from source to the goal')
            failure += 1
        elif path != 0:
            print("There is a path from source to goal and the path is")
            success += 1
            maze = mazepath(maze, path)
        pprint(maze)
        i += 1
    success_prob = (success/trails)*100
    print("Success probability with A Star euclidian distance is", success_prob, "%")

if __name__ == '__main__':
    main()



