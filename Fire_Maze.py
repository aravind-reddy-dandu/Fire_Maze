import copy
import itertools
from pprint import pprint
from random import randint
from collections import deque
import numpy as np


def generateGrid(dim, prob):
    grid = []
    for row in range(dim):
        grid.append([])
        for column in range(dim):
            grid[row].append(int(np.random.binomial(1, prob, 1)))
            if row == column == dim - 1:
                grid[row][column] = 0
    grid[0][0] = 1
    grid[dim - 1][dim - 1] = 1
    return grid


class Location:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Location):
            return (self.x == other.x) and (self.y == self.y)
        return False


class QueuePoint:
    def __init__(self, pt: Location, dist: int):
        self.pt = pt
        self.dist = dist


def isCellValid(mat, row: int, col: int):
    return (row >= 0) and (row < len(mat)) and (col >= 0) and (col < len(mat[0]))


rowMov = [-1, 0, 0, 1]
colMov = [0, -1, 1, 0]


def breadthFirstSearch(maze, source: Location, goal: Location):
    if maze[source.x][source.y] != 1 or maze[goal.x][goal.y] != 1:
        return -1
    q = deque()
    visited = [[False for i in range(len(maze[0]))] for j in range(len(maze))]
    visited[source.x][source.y] = True
    s = QueuePoint(source, 0)
    q.append(s)
    while q:
        current = q.popleft()
        pt = current.pt
        if pt.x == goal.x and pt.y == goal.y:
            return current
        for i in range(4):
            row = pt.x + rowMov[i]
            col = pt.y + colMov[i]
            if isCellValid(maze, row, col) and maze[row][col] == 1 and not visited[row][col]:
                visited[row][col] = True
                AdjPoint = Location(row, col)
                AdjPoint.prev = pt
                Adjcell = QueuePoint(AdjPoint, current.dist + 1)
                q.append(Adjcell)
    return -1


def getSolution(source, dest, mat):
    # maze = [[1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
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
    out = [[0 for col in range(dim)] for row in range(dim)]
    path = []
    out[source.x][source.y] = 1
    out[dest.x][dest.y] = 1
    node = breadthFirstSearch(mat, source, dest)
    if node == -1:
        print("Path doesn't exist")
        return 0
    elif node.dist != -1:
        print("Shortest Path is", node.dist)
    point = node.pt
    while hasattr(point, 'prev'):
        pointN = Location(point.x, point.y)
        point = point.prev
        out[point.x][point.y] = 1
        path.append(pointN)
    path.append(Location(source.x, source.y))
    path = list(reversed(path))
    # pprint(out)
    return path


def mazeWithFireNaive(dim, fillProb, fireprob):
    source = Location(0, 0)
    dest = Location(dim - 1, dim - 1)
    cleanMaze = generateGrid(dim, fillProb)
    solution = getSolution(source, dest, cleanMaze)
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
            firecell = Location(randint(0, dim - 1), randint(0, dim - 1))
            flag = False
            while visited[firecell.x][firecell.y] or (breadthFirstSearch(maze, Location(0, 0), firecell) == -1):
                visited[firecell.x][firecell.y] = True
                firecell = Location(randint(0, dim - 1), randint(0, dim - 1))
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
    source = Location(0, 0)
    dest = Location(dim - 1, dim - 1)
    cleanMaze = generateGrid(dim, fillProb)
    initialsolution = getSolution(source, dest, cleanMaze)
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
            firecell = Location(randint(0, dim - 1), randint(0, dim - 1))
            while visited[firecell.x][firecell.y] or (breadthFirstSearch(maze, Location(0, 0), firecell) == -1):
                visited[firecell.x][firecell.y] = True
                firecell = Location(randint(0, dim - 1), randint(0, dim - 1))
                count = count + 1
                if count == dim * dim:
                    return 'Nowhere to put fire'
            visited[firecell.x][firecell.y] = True
            maze[firecell.x][firecell.y] = 3
            print('Fire cell location is (' + str(firecell.x) + ', ' + str(firecell.y) + ')')
            point = solution[1]
            while maze[point.x][point.y] != 2:
                maze = spreadFire(maze, fireprob, False)
                solution = getSolution(point, dest, maze)
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
        return mazeCount


def spreadFire(mat, fireprob, fake):
    dim = len(mat)
    mat = [[3 if b == 2 else b for b in i] for i in mat]
    mat = [[5 if b == 4 else b for b in i] for i in mat]
    for row in range(dim):
        for column in range(dim):
            pt = Location(row, column)
            firecount = 0
            for i in range(4):
                rowloc = pt.x + rowMov[i]
                colloc = pt.y + colMov[i]
                if isCellValid(mat, rowloc, colloc) and (mat[rowloc][colloc] == 3 or mat[rowloc][colloc] == 5):
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


def test_strategies():
    global simulatonsPerMaze
    N = 1000
    simulatonsPerMaze = 10
    dim = 10
    fillProb = 0.7
    storageDict = {}
    for i in [5]:
        fireprob = i / 10
        successCount = 0
        fairTrails = 0
        for _ in itertools.repeat(None, N):
            response = mazeWithFireRebuild(dim, fillProb, fireprob)
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

# test_strategies()
