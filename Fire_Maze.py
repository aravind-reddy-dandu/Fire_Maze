import copy
import itertools
from pprint import pprint
from random import randint

import numpy as np


def generateGrid(dim, prob):
    # dim = 10
    grid = []
    for row in range(dim):
        # Add an empty array that will hold each cell
        # in this row
        grid.append([])
        for column in range(dim):
            grid[row].append(int(np.random.binomial(1, prob, 1)))  # Append a cell
            if row == column == dim - 1:
                grid[row][column] = 0
    grid[0][0] = 1
    grid[dim - 1][dim - 1] = 1
    return grid


# Python program to find the shortest
# path between a given source cell
# to a destination cell.

from collections import deque


# ROW = dim
# COL = dim


# To store matrix cell cordinates
class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Point):
            return (self.x == other.x) and (self.y == self.y)
        return False

    # A data structure for queue used in BFS


class queueNode:
    def __init__(self, pt: Point, dist: int):
        self.pt = pt  # The cordinates of the cell
        self.dist = dist  # Cell's distance from the source


# Check whether given cell(row,col)
# is a valid cell or not
def isValid(mat, row: int, col: int):
    return (row >= 0) and (row < len(mat)) and (col >= 0) and (col < len(mat[0]))


# These arrays are used to get row and column
# numbers of 4 neighbours of a given cell
rowNum = [-1, 0, 0, 1]
colNum = [0, -1, 1, 0]


# Function to find the shortest path between
# a given source cell to a destination cell.
def BFS(mat, src: Point, dest: Point):
    # check source and destination cell
    # of the matrix have value 1
    if mat[src.x][src.y] != 1 or mat[dest.x][dest.y] != 1:
        return -1

    visited = [[False for i in range(len(mat[0]))] for j in range(len(mat))]

    # Mark the source cell as visited
    visited[src.x][src.y] = True

    # Create a queue for BFS
    q = deque()

    # Distance of source cell is 0
    s = queueNode(src, 0)
    q.append(s)  # Enqueue source cell

    # Do a BFS starting from source cell
    while q:

        curr = q.popleft()  # Dequeue the front cell

        # If we have reached the destination cell,
        # we are done
        pt = curr.pt
        if pt.x == dest.x and pt.y == dest.y:
            return curr

            # Otherwise enqueue its adjacent cells
        for i in range(4):
            row = pt.x + rowNum[i]
            col = pt.y + colNum[i]

            # if adjacent cell is valid, has path
            # and not visited yet, enqueue it.
            if isValid(mat, row, col) and mat[row][col] == 1 and not visited[row][col]:
                visited[row][col] = True
                AdjPoint = Point(row, col)
                AdjPoint.prev = pt
                Adjcell = queueNode(AdjPoint, curr.dist + 1)
                q.append(Adjcell)

                # Return -1 if destination cannot be reached
    return -1


# Driver code
def getSol(source, dest, mat):
    # mat = [[1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    #        [0, 1, 1, 0, 1, 1, 1, 1, 0, 0],
    #        [1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
    #        [1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
    #        [0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    #        [1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    #        [1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    #        [1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    #        [1, 1, 1, 1, 1, 0, 0, 0, 1, 1],
    #        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1]]
    dim = len(mat)
    # source = Point(0, 0)
    # dest = Point(dim - 1, dim - 1)
    pprint(mat)
    out = [[0 for col in range(dim)] for row in range(dim)]
    path = []
    out[source.x][source.y] = 1
    out[dest.x][dest.y] = 1
    node = BFS(mat, source, dest)
    if node == -1:
        print("Path doesn't exist")
        return 0
    elif node.dist != -1:
        print("Shortest Path is", node.dist)
    point = node.pt
    while hasattr(point, 'prev'):
        pointN = Point(point.x, point.y)
        point = point.prev
        # print(str(point.x) + ' ' + str(point.y))
        out[point.x][point.y] = 1
        path.append(pointN)
    path.append(Point(source.x, source.y))
    path = list(reversed(path))
    pprint(out)
    return path


def mazeWithFireNaive(dim, fillProb, fireprob):
    # N = 100
    # successCount = 0
    # for _ in itertools.repeat(None, N):
    #     pathExists = simulate(10, 0.8)
    #     successCount = successCount + pathExists
    # print(successCount)
    # dim = 10
    # fillProb = 0.7
    # fireprob = 0.5
    source = Point(0, 0)
    dest = Point(dim - 1, dim - 1)
    cleanMaze = generateGrid(dim, fillProb)
    solution = getSol(source, dest, cleanMaze)
    if solution == 0:
        print('no solution')
    else:
        visited = [[True if b == 0 else False for b in i] for i in cleanMaze]
        visited[0][0] = True
        visited[dim - 1][dim - 1] = True
        count = 0
        for row in range(dim):
            for column in range(dim):
                if visited[row][column]:
                    count = count + 1
        mazeCount = []
        for _ in itertools.repeat(None, simulatonsPerMaze):
            maze = copy.deepcopy(cleanMaze)
            firecell = Point(randint(0, dim - 1), randint(0, dim - 1))
            flag = False
            while visited[firecell.x][firecell.y] or (BFS(maze, Point(0, 0), firecell) == -1):
                visited[firecell.x][firecell.y] = True
                firecell = Point(randint(0, dim - 1), randint(0, dim - 1))
                count = count + 1
                if count == dim * dim:
                    mazeCount.append('Nowhere to put fire')
            visited[firecell.x][firecell.y] = True
            maze[firecell.x][firecell.y] = 3
            print('Fire cell location is (' + str(firecell.x) + ', ' + str(firecell.y) + ')')
            for point in solution:
                # maze = [[3 if b == 2 else b for b in i] for i in maze]
                maze = spreadFire(maze, fireprob, False)
                if maze[point.x][point.y] == 2:
                    pprint(maze)
                    mazeCount.append('dead')
                    print('dead')
                    flag = True
                    break
            if flag:
                continue
            pprint(maze)
            mazeCount.append('alive')
            print('alive')
        return mazeCount


def mazeWithFireRebuild(dim, fillProb, fireprob):
    source = Point(0, 0)
    dest = Point(dim - 1, dim - 1)
    cleanMaze = generateGrid(dim, fillProb)
    initialsolution = getSol(source, dest, cleanMaze)
    if initialsolution == 0:
        print('no solution')
    else:
        visited = [[True if b == 0 else False for b in i] for i in cleanMaze]
        visited[0][0] = True
        visited[dim - 1][dim - 1] = True
        count = 0
        for row in range(dim):
            for column in range(dim):
                if visited[row][column]:
                    count = count + 1
        mazeCount = []
        for _ in itertools.repeat(None, simulatonsPerMaze):
            maze = copy.deepcopy(cleanMaze)
            solution = copy.deepcopy(initialsolution)
            firecell = Point(randint(0, dim - 1), randint(0, dim - 1))
            while visited[firecell.x][firecell.y] or (BFS(maze, Point(0, 0), firecell) == -1):
                visited[firecell.x][firecell.y] = True
                firecell = Point(randint(0, dim - 1), randint(0, dim - 1))
                count = count + 1
                if count == dim * dim:
                    return 'Nowhere to put fire'
            visited[firecell.x][firecell.y] = True
            maze[firecell.x][firecell.y] = 3
            print('Fire cell location is (' + str(firecell.x) + ', ' + str(firecell.y) + ')')
            point = solution[1]
            while maze[point.x][point.y] != 2:
                # maze = [[3 if b == 2 else b for b in i] for i in maze]
                maze = spreadFire(maze, fireprob, False)
                solution = getSol(point, dest, maze)
                maze = [[1 if b == 4 else b for b in i] for i in maze]
                if solution == 0:
                    mazeCount.append('dead')
                    print('dead')
                    break
                point = solution[1]
                if point == dest:
                    pprint(maze)
                    mazeCount.append('alive')
                    print('alive')
                    break
                # elif maze[point.x][point.y] == 2:
                #     pprint(maze)
                #     mazeCount.append('dead')
                #     print('dead')
                #     break
        return mazeCount
        # pprint(maze)
        # return 'alive'


def mazeWithFireThirdStrategy(dim, fillProb, fireprob):
    source = Point(0, 0)
    dest = Point(dim - 1, dim - 1)
    cleanMaze = generateGrid(dim, fillProb)
    initialsolution = getSol(source, dest, cleanMaze)
    if initialsolution == 0:
        print('no solution')
    else:
        visited = [[True if b == 0 else False for b in i] for i in cleanMaze]
        visited[0][0] = True
        visited[dim - 1][dim - 1] = True
        count = 0
        for row in range(dim):
            for column in range(dim):
                if visited[row][column]:
                    count = count + 1
        mazeCount = []
        for _ in itertools.repeat(None, simulatonsPerMaze):
            maze = copy.deepcopy(cleanMaze)
            solution = copy.deepcopy(initialsolution)
            firecell = Point(randint(0, dim - 1), randint(0, dim - 1))
            while visited[firecell.x][firecell.y] or (BFS(maze, Point(0, 0), firecell) == -1):
                visited[firecell.x][firecell.y] = True
                firecell = Point(randint(0, dim - 1), randint(0, dim - 1))
                count = count + 1
                if count == dim * dim:
                    return 'Nowhere to put fire'
            visited[firecell.x][firecell.y] = True
            maze[firecell.x][firecell.y] = 3
            print('Fire cell location is (' + str(firecell.x) + ', ' + str(firecell.y) + ')')
            point = solution[1]
            while maze[point.x][point.y] != 2:
                maze = spreadFire(maze, fireprob, False)
                maze = spreadFire(maze, fireprob, True)
                maze = spreadFire(maze, fireprob, True)
                # maze = spreadFire(maze, fireprob, True)
                solution = getSol(point, dest, maze)
                maze = [[1 if b == 4 else b for b in i] for i in maze]
                if solution == 0:
                    solution = getSol(point, dest, maze)
                    if solution == 0:
                        mazeCount.append('dead')
                        print('dead')
                        break
                point = solution[1]
                if point == dest:
                    pprint(maze)
                    mazeCount.append('alive')
                    print('alive')
                    break
                # elif maze[point.x][point.y] == 2:
                #     pprint(maze)
                #     mazeCount.append('dead')
                #     print('dead')
                #     break
        return mazeCount
        # pprint(maze)
        # return 'alive'


def spreadFire(mat, fireprob, fake):
    dim = len(mat)
    mat = [[3 if b == 2 else b for b in i] for i in mat]
    mat = [[5 if b == 4 else b for b in i] for i in mat]
    for row in range(dim):
        for column in range(dim):
            pt = Point(row, column)
            firecount = 0
            for i in range(4):
                rowloc = pt.x + rowNum[i]
                colloc = pt.y + colNum[i]
                if isValid(mat, rowloc, colloc) and (mat[rowloc][colloc] == 3 or mat[rowloc][colloc] == 5):
                    firecount = firecount + 1
            prob = 1 - pow((1 - fireprob), firecount)
            check = int(np.random.binomial(1, prob, 1))
            if fake:
                if check == 1 and mat[row][column] == 1:
                    mat[row][column] = 4
            else:
                if check == 1 and mat[row][column] == 1:
                    mat[row][column] = 2
    mat = [[2 if b == 3 else b for b in i] for i in mat]
    mat = [[4 if b == 5 else b for b in i] for i in mat]
    return mat


# print(mazeWithFireNaive())

def Run_1_2():
    global simulatonsPerMaze
    N = 10
    simulatonsPerMaze = 10
    storageDict = {}
    for i in [5]:
        fireprob = i / 10
        successCount = 0
        fairTrails = 0
        for _ in itertools.repeat(None, N):
            response = mazeWithFireNaive(10, 0.7, fireprob)
            print(response)
            if response is None:
                continue
            for result in response:
                if result == 'alive':
                    successCount = successCount + 1
                    fairTrails = fairTrails + 1
                elif result == 'dead':
                    fairTrails = fairTrails + 1
        print('Fair trails are ' + str(fairTrails))
        print('Success Count is ' + str(successCount))
        print('Winning probability is ' + str(successCount / fairTrails))
        print(str(fireprob) + ',' + str(fairTrails) + ',' + str(successCount) + ',' + str(successCount / fairTrails))
        storageDict[str(fireprob)] = str(fireprob) + ',' + str(fairTrails) + ',' + str(successCount) + ',' + str(
            successCount / fairTrails)
    for prob in storageDict.values():
        print(prob)


# Run_1_2()
