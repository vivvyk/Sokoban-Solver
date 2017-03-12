def is_cornered(matrix,goals):
    '''
    Tests if a box is in a corner and not on a goal.
    Input: matrix and goal positions
    Output: boolean
    '''
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
    '''
    Finds if two boxes along the edge are together, with one or both not on a goal. This is a stuck position.
    Input: matrix and goal positions.
    Output: boolean
    '''
    #Tests Top Row
    for i in range(len(matrix[0])-2):
        if matrix[0][i] == 1 and matrix[0][i+1] == 1: #Checks one position and the next position
            if (0,i) not in goals or (0,i+1) not in goals:
                return True
    #Tests Bottom Row
    for i in range(len(matrix[0])-2):
        if matrix[len(matrix)-1][i] == 1 and matrix[len(matrix)-1][i+1] == 1:
            if (len(matrix)-1,i) not in goals or (len(matrix)-1,i+1) not in goals:
                return True

    #Tests Left Column
    for i in range(len(matrix)-2):
        if matrix[i][0] == 1 and matrix[i+1][0] == 1:
            if (i,0) not in goals or (i+1,0) not in goals:
                return True

    #Tests Right Column
    for i in range(len(matrix)-2):
        if matrix[i][len(matrix[0])-1] == 1 and matrix[i+1][len(matrix[0])-1] == 1:
            if (i,len(matrix[0])-1) not in goals or (i+1,len(matrix[0])-1) not in goals:
                return True

    return False

def is_stuck(matrix,goals):
    '''
    Examines the "edges," or topmost, leftmost, bottommost, and rightmost sides of the matrix. These are common locations for boxes being stuck.
    Input: matrix and goal positions
    Output: boolean
    '''
    if is_cornered(matrix,goals): #If a box is cornered, it is stuck.
        return True

    if find_adjacent(matrix,goals): #If there are adjacent boxes, they are stuck.
        return True

    #Counts goals
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

    #Counts number of boxes on an edge that are not on goals, and tests if the number of boxes on an edge is greater than the number of goals.
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

    for (ind,row) in enumerate(matrix): #Does right and left at same time.
        if row[0] == 1 and not((ind,0) in goals):
            leftCounter += 1
        if row[len(matrix[0])-1] == 1 and not((ind, len(matrix[0])-1) in goals):
            rightCounter += 1
    if leftCounter > goalLeft or rightCounter > goalRight:
        return True

    return False
