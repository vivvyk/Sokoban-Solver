import sys
import SokobanMechanics as m
import numpy as np
import math

def toPerm(matrix):
    threes = []
    permutation = ""
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 3:
                threes.append((i,j))
            else:
                permutation += str(matrix[i][j])
    return (permutation, threes, len(matrix),len(matrix[0]))

def counts(perm):
    perm = sorted(perm)
    counts = []
    for (i,item) in enumerate(perm):
        if i == 0:
            counts.append(1)
        elif item != perm[i-1]:
            counts.append(1)
        else:
            counts[-1] += 1
    return counts

def potential(perm, counts): #Source: Wikipedia
    denominator = 1
    for count in counts:
        denominator *= math.factorial(count)

    return (math.factorial(len(perm)) / denominator)


def rank(perm,inLength,inCount,inPot): #Source: Pavel Savara, helped by Michael Chang
    length = inLength
    count = inCount[:]
    pot = inPot

    rankIndex = 0
    for i in perm:
        offset = 0
        typeNumber = int(i)
        for j in range(typeNumber):
            offset += count[j]

        '''Calculations similar to Pavel Savara's unrank function.'''
        rankIndex += (pot * offset) / length

        pot *= count[typeNumber]
        pot /= length

        length -= 1
        count[typeNumber] -= 1


    return rankIndex

def unrank(rankIndex,inLength,inCount,inPot): #Source: Pavel Savara
    length = inLength
    count = inCount[:]
    pot = inPot

    perm = [0] * inLength

    for i in range(length):
        selector = (rankIndex * length) / pot
        offset = 0
        typeNumber = offset

        while (offset + count[typeNumber]) <= selector:
            offset += count[typeNumber]
            typeNumber += 1

        rankIndex -= (pot * offset) / length

        pot *= count[typeNumber]
        pot /= length

        length -= 1
        count[typeNumber] -= 1

        perm[i] = typeNumber

    return perm

def toMatrix(perm, threes, rowNum, colNum):
    permstr = ""
    for item in perm:
        permstr += str(item)
    matrix = []
    for i in range(rowNum):
        row = [0]*(colNum)
        matrix.append(row)

    for point in threes:
        matrix[point[0]][point[1]] = 3

    i = 0
    for ri,row in enumerate(matrix):
        for ci,column in enumerate(row):
            if matrix[ri][ci] == 3:
                pass
            else:
                matrix[ri][ci] = int(permstr[i])
                i += 1

    return np.array(matrix)


if __name__ == "__main__":
    level = sys.stdin.readlines()
    matrix_info = m.read(level)
    matrix = matrix_info[0]
    goals = matrix_info[1]

    print goals
    print np.array(matrix)

    perm = [0,0,1,2]

    r= rank(perm,len(perm),counts(perm),potential(perm,counts(perm)))
    print unrank(r,len(perm),counts(perm),potential(perm,counts(perm)))
