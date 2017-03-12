import sys
import numpy as np

def read(levelArray):
    '''
    Reads level
    Input: level, Puzzlescript format
    Output: matrix representation of level, goal positions
    '''
    levelArray.pop(0) #Gets rid of top and bottom row
    levelArray.pop()

    matrix = []
    goalPositions = [] #AS INDECES
    for (rowNum, item) in enumerate(levelArray):
        item = item.rstrip('\r\n')
        item = item[1:len(item)-1] #Gets rid of left and right rows
        row = []
        for (colNum,character) in enumerate(item):
            if character == ".":
                goalPositions.append((rowNum,colNum))
                row.append(0)
            elif character == "+":
                goalPositions.append((rowNum,colNum))
                row.append(2)
            elif character == "*":
                goalPositions.append((rowNum,colNum))
                row.append(1)
            elif character == " ":
                row.append(0)
            elif character == "$":
                row.append(1)
            elif character == "@":
                row.append(2)
            elif character == "#":
                row.append(3)
        matrix.append(row)

    for row in matrix:
        if any((len(row) != len(x)) for x in matrix):
            row.append(0) #If no space at end of row.

    return (matrix, goalPositions)

def move(matrix, direction):
    '''
    Moves player within level.
    Input: matrix and desired direction
    Output: new matrix
    '''
    if not(direction == "up" or direction == "down" or direction == "right" or direction == "left"): #Makes sure input is valid
        print "Invalid"
        return None

    playerPos = (0,0) #Finds player
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 2:
                playerPos = (i,j)
                break
    try:
        a = 0
        b = 0
        c = 0
        d = 0
        e = 0
        f = 0
        varIndex = 0
        if direction == "down":
            a = 1
            b = 2
        elif direction == "right":
            c = 1
            d = 2
        elif direction == "up":
            a = -1
            e = -1
            b = -2
        elif direction == "left":
            c = -1
            f = -1
            d = -2
            varIndex = 1

        if matrix[playerPos[0]+a][playerPos[1]+c] == 3: #Catches walls
            raise Exception

        if playerPos[varIndex]+e+f < 0 or matrix[playerPos[0]+e][playerPos[1]+f] == 3: #Catches walls
            raise Exception

        if matrix[playerPos[0]+a][playerPos[1]+c] == 0:
            matrix[playerPos[0]+a][playerPos[1]+c] = 2
            matrix[playerPos[0]][playerPos[1]] = 0
            return matrix

        if (direction == "left" or direction =="up") and playerPos[varIndex]-2 < 0: #Prevents from looping around
            raise Exception

        elif matrix[playerPos[0]+a][playerPos[1]+c] == 1 and matrix[playerPos[0]+b][playerPos[1]+d] != 1 and matrix[playerPos[0]+b][playerPos[1]+d] != 3:
            matrix[playerPos[0]+b][playerPos[1]+d] = 1
            matrix[playerPos[0]+a][playerPos[1]+c] = 2
            matrix[playerPos[0]][playerPos[1]] = 0
            return matrix

        return None

    except:
        return None

    return None

def neighbors(vertex):
    '''
    Finds all neighbors of a state.
    Input: matrix
    Output: neigbors of matrix
    '''
    neighbor_list = []
    v1 = np.copy(vertex)
    v2 = np.copy(vertex)
    v3 = np.copy(vertex)
    v4 = np.copy(vertex)
    if move(v1,"up") is not None:
        neighbor_list.append(np.ndarray.tolist(v1))
    if move(v2,"down") is not None:
        neighbor_list.append(np.ndarray.tolist(v2))
    if move(v3,"right") is not None:
        neighbor_list.append(np.ndarray.tolist(v3))
    if move(v4,"left") is not None:
        neighbor_list.append(np.ndarray.tolist(v4))
    return neighbor_list

def is_goal(matrix,goals):
    '''
    Verifies if matrix is a goal state.
    Input: matrix and goal positions
    Output: Boolean
    '''
    for goal in goals:
        if matrix[goal[0]][goal[1]] != 1:
            return False
    return True
