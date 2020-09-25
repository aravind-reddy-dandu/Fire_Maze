import copy
import itertools
from pprint import pprint
from random import randint
import numpy as np

import Fire_Maze
from Fire_Maze import Point

simulatonsPerMaze = 10


def mazeWithFireThirdStrategy(dim, fillProb, fireprob):
    source = Point(0, 0)
    dest = Point(dim - 1, dim - 1)
    cleanMaze = Fire_Maze.generateGrid(dim, fillProb)
    initialsolution = Fire_Maze.getSol(source, dest, cleanMaze)
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
            heat = 15
            solution = copy.deepcopy(initialsolution)
            firecell = Point(randint(0, dim - 1), randint(0, dim - 1))
            while visited[firecell.x][firecell.y] or (Fire_Maze.BFS(maze, Point(0, 0), firecell) == -1):
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
                maze = Fire_Maze.spreadFire(maze, fireprob, False)
                solution = 0
                while solution == 0 and heat > 0:
                    maze = spreadFakeFire(maze, heat, fireprob)
                    solution = Fire_Maze.getSol(point, dest, maze)
                    heat = heat - 1
                heat = heat + 1
                maze = [[1 if b == 4 else b for b in i] for i in maze]
                if solution == 0:
                    solution = Fire_Maze.getSol(point, dest, maze)
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


def mazeWithFireNaive(dim, fillProb, fireprob):
    source = Point(0, 0)
    heat = 15
    dest = Point(dim - 1, dim - 1)
    cleanMaze = Fire_Maze.generateGrid(dim, fillProb)
    initialSol = Fire_Maze.getSol(source, dest, cleanMaze)
    if initialSol == 0:
        return 'No solution for maze'
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
        while visited[firecell.x][firecell.y] or (Fire_Maze.BFS(maze, Point(0, 0), firecell) == -1):
            visited[firecell.x][firecell.y] = True
            firecell = Point(randint(0, dim - 1), randint(0, dim - 1))
            count = count + 1
            if count == dim * dim:
                mazeCount.append('Nowhere to put fire')
        visited[firecell.x][firecell.y] = True
        maze[firecell.x][firecell.y] = 3
        solution = 0
        while solution == 0 and heat > 0:
            maze = spreadFakeFire(maze, heat, fireprob)
            solution = Fire_Maze.getSol(source, dest, maze)
            heat = heat - 1
        if solution == 0:
            continue
        maze = [[1 if b == 4 else b for b in i] for i in maze]
        print('Fire cell location is (' + str(firecell.x) + ', ' + str(firecell.y) + ')')
        for point in solution:
            # maze = [[3 if b == 2 else b for b in i] for i in maze]
            maze = Fire_Maze.spreadFire(maze, fireprob, False)
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


def spreadFakeFire(maze, heat, fireprob):
    maze = [[1 if b == 4 else b for b in i] for i in maze]
    if heat > 0:
        for _ in itertools.repeat(None, heat):
            maze = Fire_Maze.spreadFire(maze, fireprob, True)
    return maze


def Run():
    global simulatonsPerMaze
    N = 200
    simulatonsPerMaze = 10
    storageDict = {}
    dim = 10
    fillprob = 0.7
    for i in [5]:
        fireprob = i / 10
        successCount = 0
        fairTrails = 0
        for _ in itertools.repeat(None, N):
            response = mazeWithFireThirdStrategy(dim=dim, fillProb=fillprob, fireprob=fireprob)
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


Run()
