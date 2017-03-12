import sys
import numpy as np
import Queue
import SokobanMechanics as m
import Rank_Unrank as r
import Heuristics as h
import Enhancements as e
import time


def bestFS(heuristic,start,goal):
    '''
    Best First Search: puts path into PriorityQueue based on heuristic.
    Input: heuristic function, start matrix, goal positions.
    Output: path leading to solution.
    '''
    frontier = Queue.PriorityQueue() #Initializes queue.
    frontier.put([(heuristic(start,goal), start)])
    while frontier.qsize() > 0:
        path = frontier.get()
        last_vertex = path[-1][1]
        if m.is_goal(last_vertex,goal):
            return path
        for next_vertex in m.neighbors(last_vertex):
            if any((next_vertex == x[1]) for x in path): #Cycle detection.
                continue
            new_path = path + [(heuristic(next_vertex,goal), next_vertex)] #Recalculates heuristic.
            frontier.put(new_path)
    return None

def astar(heuristic,start,goal):
    '''
    A* search: adds path to queue based on cost and heuristic. Every move is assigned a cost of 1.
    Input: heuristic function, start matrix, goal positions.
    Output: path leading to solution.
    '''
    frontier = Queue.PriorityQueue()
    frontier.put((heuristic(start,goal), [start]))
    while frontier.qsize() > 0:
        path = frontier.get()
        last_vertex = path[1][-1]
        if m.is_goal(last_vertex,goal):
            return path
        for next_vertex in m.neighbors(last_vertex):
            if any((next_vertex == x) for x in path[1]): #Cycle detection.
                continue
            if e.is_stuck(next_vertex,goal): #Checks if stuck.
                continue
            new_path = (len(path[1])-1+heuristic(next_vertex,goal), path[1] + [next_vertex]) #Computes f = cost(path) + h(next_vertex)
            frontier.put(new_path)
    return None

def astar_Rank(heuristic,start,goal):
    '''
    A* search with multiple path pruning using rank and unrank. Creates an is_visited array that is indexed by rank.
    Input: heuristic function, start matrix, goal positions.
    Output: path leading to solution.
    '''
    (perm,threes,rowNum,colNum) = r.toPerm(matrix) #Turns matrix to permutation.
    length = len(perm) #Stores length
    countArray = r.counts(perm) #Stores counts
    pot =  r.potential(perm,countArray) #Stores potential.

    is_visited = [False] * pot #Creates is_visited array, which is the size of the number of permutations.
    is_visited[r.rank(perm,length,countArray,pot)] = True #Sets start node to vistied.

    frontier = Queue.PriorityQueue()
    frontier.put((heuristic(start,goal), [r.rank(perm,length,countArray,pot)]))

    while frontier.qsize() > 0:
        path = frontier.get()
        last_vertex = path[1][-1]
        tempPerm = r.unrank(last_vertex,length,countArray,pot) #Unranks for is_goal and neighbors.
        tempMatrix = r.toMatrix(tempPerm,threes,rowNum,colNum)
        if m.is_goal(tempMatrix,goal):
            #Unranks and tuns path into matrices.
            matPath = []
            for item in path[1]:
                unperm = r.unrank(item,length,countArray,pot)
                matPath.append(r.toMatrix(unperm,threes,rowNum,colNum))
            return matPath
        for next_vertex in m.neighbors(tempMatrix):
            if e.is_stuck(tempMatrix,goal): #Checks if stuck.
                continue
            perm = r.toPerm(next_vertex)[0] #Ranks next_vertex.
            rankedMat= r.rank(perm,length,countArray,pot)
            if is_visited[rankedMat] == True: #Multiple path pruning.
                continue
            else:
                is_visited[rankedMat] = True #Sets is_visited to true.
            new_path = (len(path[1])-1+heuristic(next_vertex,goal), path[1] + [rankedMat])
            frontier.put(new_path)

    return None

def b_Bound(start,goal):
    '''
    Branch and bound, returns optimal solution by looking for paths smaller than a known solution.
    Input: start matrix and goal positions.
    Output: path leading to goal.
    '''
    (perm,threes,rowNum,colNum) = r.toPerm(matrix)
    length = len(perm)
    countArray = r.counts(perm)
    pot =  r.potential(perm,countArray)

    is_visited = [False] * pot
    is_visited[r.rank(perm,length,countArray,pot)] = True

    frontier = []
    frontier.append([r.rank(perm,length,countArray,pot)])

    minLength = len(start) * 10000 #Creates large starting distance.

    while len(frontier) > 0:
        path = frontier.pop()
        if len(path) > minLength or len(path)+1 > minLength: #Checks if path taken out is larger than smallest known path.
            continue
        last_vertex = path[-1]
        tempPerm = r.unrank(last_vertex,length,countArray,pot)
        tempMatrix = r.toMatrix(tempPerm,threes,rowNum,colNum)
        if m.is_goal(tempMatrix,goal):
            #marks length of shortest known path.
            shortestPath = path[:]
            minLength = len(shortestPath)
            continue
        for next_vertex in m.neighbors(tempMatrix):
            if e.is_stuck(tempMatrix,goal):
                continue
            perm = r.toPerm(next_vertex)[0]
            rankedMat= r.rank(perm,length,countArray,pot)
            if rankedMat in path: #Cycle detection.
                continue
            new_path = path + [rankedMat]
            frontier.append(new_path)


    #Turns into a path of matrices.
    if shortestPath is None:
        return None

    matPath = []
    for item in shortestPath:
        unperm = r.unrank(item,length,countArray,pot)
        matPath.append(r.toMatrix(unperm,threes,rowNum,colNum))

    return matPath



if __name__ == "__main__":
    #Reads in level from standard input
    #Simply comment in any function you want to run.
    level = sys.stdin.readlines()
    (matrix,goals) = m.read(level)

    print np.array(matrix)
    print goals
    print "\n"

    start_time = time.time()

    #Search algorithms, heuristic is set to manhattan.
    path1 = bestFS(h.manhattan,matrix,goals)
    path2 = astar(h.manhattan,matrix,goals)
    path3 = astar_Rank(h.manhattan,matrix,goals)
    path4 = b_Bound(matrix,goals)


    print "Best First Search"
    for i,element in enumerate(path1):
        print i
        print np.array(element[1])
        print "\n"

    print "A*"
    for i,element in enumerate(path2[1]):
        print i
        print np.array(element)
        print "\n"

    print "A*/PathPruning"
    for i,element in enumerate(path3):
        print i
        print np.array(element)
        print "\n"


    print "Branch and Bound"
    for i,element in enumerate(path4):
        print i
        print np.array(element)
        print "\n"

    print("%s seconds" % (time.time() - start_time))
