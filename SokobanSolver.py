import sys
import numpy as np
import Queue
import SokobanMechanics as m
import Rank_Unrank as r
import time


def bestFS(heuristic,start,goal):
    frontier = Queue.PriorityQueue()
    frontier.put([(heuristic(start,goal), start)])
    while frontier.qsize() > 0:
        path = frontier.get()
        last_vertex = path[-1][1]
        if m.is_goal(last_vertex,goal):
            return path
        for next_vertex in m.neighbors(last_vertex):
            if any((next_vertex == x[1]) for x in path):
                continue
            new_path = path + [(heuristic(next_vertex,goal), next_vertex)]
            frontier.put(new_path)
    return None

def astar(heuristic,start,goal):
    frontier = Queue.PriorityQueue()
    frontier.put((heuristic(start,goal), [start]))
    while frontier.qsize() > 0:
        path = frontier.get()
        last_vertex = path[1][-1]
        if m.is_goal(last_vertex,goal):
            return path
        for next_vertex in m.neighbors(last_vertex):
            if any((next_vertex == x) for x in path[1]):
                continue
            if m.is_stuck(next_vertex,goal):
                continue
            new_path = (len(path[1])-1+heuristic(next_vertex,goal), path[1] + [next_vertex])
            frontier.put(new_path)
    return None

def astar_Rank(heuristic,start,goal):
    (perm,threes,rowNum,colNum) = r.toPerm(matrix)
    length = len(perm)
    countArray = r.counts(perm)
    pot =  r.potential(perm,countArray)

    is_visited = [False] * pot
    is_visited[r.rank(perm,length,countArray,pot)] = True

    frontier = Queue.PriorityQueue()
    frontier.put((heuristic(start,goal), [r.rank(perm,length,countArray,pot)]))

    while frontier.qsize() > 0:
        path = frontier.get()
        last_vertex = path[1][-1]
        tempPerm = r.unrank(last_vertex,length,countArray,pot)
        tempMatrix = r.toMatrix(tempPerm,threes,rowNum,colNum)
        if m.is_goal(tempMatrix,goal):
            matPath = []
            for item in path[1]:
                unperm = r.unrank(item,length,countArray,pot)
                matPath.append(r.toMatrix(unperm,threes,rowNum,colNum))
            return matPath
        for next_vertex in m.neighbors(tempMatrix):
            if m.is_stuck(tempMatrix,goal):
                continue
            perm = r.toPerm(next_vertex)[0]
            rankedMat= r.rank(perm,length,countArray,pot)
            if is_visited[rankedMat] == True:
                continue
            else:
                is_visited[rankedMat] = True
            new_path = (len(path[1])-1+heuristic(next_vertex,goal), path[1] + [rankedMat])
            frontier.put(new_path)

    return None



if __name__ == "__main__":
    #Look out for 3 and 19
    level = sys.stdin.readlines()
    matrix_info = m.read(level)
    matrix = matrix_info[0]
    goals = matrix_info[1]

    print np.array(matrix)
    print goals
    print "\n"

    start_time = time.time()
    path = astar_Rank(m.manhattan,matrix,goals)

    print "astar"
    for element in path:
        print element
        print "\n"


    print("--- %s seconds ---" % (time.time() - start_time))
