import sys
import numpy as np

def read(levelArray):
    levelArray.pop(0)
    levelArray.pop()

    matrix = []
    goalPositions = [] #AS INDECES
    for (rowNum, item) in enumerate(levelArray):
        item = item.rstrip('\r\n')
        item = item[1:len(item)-1]
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
            row.append(0)

    return (matrix, goalPositions)

def move(matrix, direction):
    if not(direction == "up" or direction == "down" or direction == "right" or direction == "left"):
        print "Invalid"
        return None

    playerPos = (0,0)
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

        if matrix[playerPos[0]+a][playerPos[1]+c] == 3:
            raise Exception

        if playerPos[varIndex]+e+f < 0 or matrix[playerPos[0]+e][playerPos[1]+f] == 3:
            raise Exception

        if matrix[playerPos[0]+a][playerPos[1]+c] == 0:
            matrix[playerPos[0]+a][playerPos[1]+c] = 2
            matrix[playerPos[0]][playerPos[1]] = 0
            return matrix

        if (direction == "left" or direction =="up") and playerPos[varIndex]-2 < 0:
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

def boxes(matrix, goalPositions):

    if is_cornered(matrix, goalPositions):
        return 2 * len(matrix) + 1000

    boxOffGoal = 0
    for goal in goalPositions:
        if matrix[goal[0]][goal[1]] != 1:
            boxOffGoal +=1
    return boxOffGoal

def manhattan(matrix,goalPositions):
    goals = goalPositions[:]
    if is_cornered(matrix,goalPositions):
        return 2 * len(matrix[0]) + 1000

    boxPositions = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 1:
                boxPos = (i,j)
                boxPositions.append(boxPos)
            continue

    manhattanDistanceTotal = 0
    for box in boxPositions:
        minDistance = 2*len(matrix)+1
        for goal in goals:
            distance = abs(goal[0]-box[0]) + abs(goal[1]-box[1])
            if distance < minDistance:
                minDistance = distance

        manhattanDistanceTotal += minDistance

    return manhattanDistanceTotal

def neighbors(vertex):
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
    for goal in goals:
        if matrix[goal[0]][goal[1]] != 1:
            return False
    return True

def is_cornered(matrix,goals):
    if matrix[0][0] == 1 and (0,0) not in goals:
        return True

    elif matrix[len(matrix)-1][0] == 1 and (len(matrix)-1,0) not in goals:
        return True

    elif matrix[0][len(matrix[0])-1] == 1 and (0, len(matrix[0])-1) not in goals:
        return True

    elif matrix[len(matrix)-1][len(matrix[0])-1] == 1 and (len(matrix)-1, len(matrix[0])-1) not in goals:
        return True

    return False

def find_adjacent(matrix,goals):
    for i in range(len(matrix[0])-2):
        if matrix[0][i] == 1 and matrix[0][i+1] == 1:
            if (0,i) not in goals or (0,i+1) not in goals:
                return True

    for i in range(len(matrix[0])-2):
        if matrix[len(matrix)-1][i] == 1 and matrix[len(matrix)-1][i+1] == 1:
            if (len(matrix)-1,i) not in goals or (len(matrix)-1,i+1) not in goals:
                return True

    for i in range(len(matrix)-2):
        if matrix[i][0] == 1 and matrix[i+1][0] == 1:
            if (i,0) not in goals or (i+1,0) not in goals:
                return True

    for i in range(len(matrix)-2):
        if matrix[i][len(matrix[0])-1] == 1 and matrix[i+1][len(matrix[0])-1] == 1:
            if (i,len(matrix[0])-1) not in goals or (i+1,len(matrix[0])-1) not in goals:
                return True

    return False

def is_stuck(matrix,goals):
    if is_cornered(matrix,goals):
        return True

    if find_adjacent(matrix,goals):
        return True

    goalTop = 0
    goalBottom = 0
    goalLeft = 0
    goalRight = 0
    for goal in goals:
        if goal[0] == 0 and matrix[goal[0]][goal[1]] != 1:
            goalTop += 1
        if goal[0] == len(matrix)-1 and matrix[goal[0]][goal[1]] != 1:
            goalBottom += 1
        if goal[1] == 0 and matrix[goal[0]][goal[1]] != 1:
            goalLeft += 1
        if goal[1] == len(matrix[0])-1 and matrix[goal[0]][goal[1]] != 1:
            goalRight += 1

    topCounter = 0
    bottomCounter = 0
    rightCounter = 0
    leftCounter = 0

    for (ind,element) in enumerate(matrix[0]):
        if element == 1 and not((0,ind) in goals):
            topCounter += 1
    if topCounter > goalTop:
        return True

    for (ind,element) in enumerate(matrix[len(matrix)-1]):
        if element == 1 and not((len(matrix)-1,ind) in goals):
            bottomCounter += 1
    if bottomCounter > goalBottom:
        return True

    for (ind,row) in enumerate(matrix):
        if row[0] == 1 and not((ind,0) in goals):
            leftCounter += 1
        if row[len(matrix[0])-1] == 1 and not((ind, len(matrix[0])-1) in goals):
            rightCounter += 1
    if leftCounter > goalLeft or rightCounter > goalRight:
        return True

    return False



if __name__ == "__main__":
    level = sys.stdin.readlines()
    matrix_info = read(level)
    matrix = matrix_info[0]
    goals = matrix_info[1]

    print goals
    print np.array(matrix)

    print manhattan(matrix,goals)
