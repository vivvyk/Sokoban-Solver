import sys
import numpy as np
import Queue
import SokobanMechanics as m
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
            if any((next_vertex == x[1]) for x in path): #If new vertex already in path, ignore this neighbor.
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
            if any((next_vertex == x) for x in path[1]): #If new vertex already in path, ignore this neighbor.
                continue
            if m.is_stuck(next_vertex,goal):
                continue
            new_path = (len(path[1])-1+heuristic(next_vertex,goal), path[1] + [next_vertex])
            frontier.put(new_path)
    return None

def branch(heuristic,start,goal,limit):
    frontier = Queue.PriorityQueue()
    frontier.put((heuristic(start,goal), [start]))
    while frontier.qsize() > 0:
        path = frontier.get()
        last_vertex = path[1][-1]
        if m.is_goal(last_vertex,goal):
            branch(heuristic(last_vertex,goal),start,goal,len(path))
            return path
        for next_vertex in m.neighbors(last_vertex):
            if len(path) == limit:
                continue
            if any((next_vertex == x) for x in path[1]): #If new vertex already in path, ignore this neighbor.
                continue
            if m.is_stuck(next_vertex,goal):
                continue
            new_path = (len(path[1])-1+heuristic(next_vertex,goal), path[1] + [next_vertex])
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


    #print m.boxes(matrix, goals)
    #print m.manhattan(matrix, goals)
    start_time = time.time()
    path = astar(m.manhattan,matrix,goals)
    #matrixPath = []
    print "astar"
    for element in path[1]:
        #matrixPath.append(element[1])
        print np.array(element)
    #    print "\n"
    print path[0]
    print("--- %s seconds ---" % (time.time() - start_time))

    '''
    for element in matrixPath:
        print np.array(element)
        print "\n"

    print cost(matrixPath,m.boxes,goals)
    '''
