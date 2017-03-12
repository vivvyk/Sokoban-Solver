import Enhancements as e

def boxes(matrix, goalPositions):
    '''
    Computes the boxes heuristic, which marks the number of boxes off goal position.
    Input: matrix and goal positions
    Output: number of boxes off goal
    '''
    if e.is_cornered(matrix, goalPositions): #Uses is_cornered to check for stuck boxes
        return 2 * len(matrix) + 1000 #A very large integer.

    boxOffGoal = 0
    for goal in goalPositions:
        if matrix[goal[0]][goal[1]] != 1:
            boxOffGoal +=1
    return boxOffGoal

def manhattan(matrix,goalPositions):
    '''
    Computes the total manhattan distance, which marks the distance from boxes to goals.
    Input: matrix and goal positions
    Output: total manhattan distance
    '''
    goals = goalPositions[:]

    if e.is_cornered(matrix,goals):
        return 2 * len(matrix[0]) + 1000 #A very large integer

    boxPositions = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 1:
                boxPos = (i,j) #Marks box indeces
                boxPositions.append(boxPos)
            continue

    manhattanDistanceTotal = 0
    for box in boxPositions:
        minDistance = 2*len(matrix)+1
        for goal in goals:
            distance = abs(goal[0]-box[0]) + abs(goal[1]-box[1]) #Finds distance
            if distance < minDistance: #Finds smallest distance
                minDistance = distance

        manhattanDistanceTotal += minDistance

    return manhattanDistanceTotal
