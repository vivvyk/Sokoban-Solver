import sys
import SokobanMechanics as m
import numpy as np
import math

def toPerm(matrix):
    '''
    Creates a multiset permutation of a matrix.
    Input: matrix
    Output: 4-tuple containing the multiset permutation, the position of the threes, and the number of rows and columns.
    '''
    threes = []
    permutation = ""
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 3:
                threes.append((i,j)) #Finds position of threes.
            else:
                permutation += str(matrix[i][j]) #Adds to permutation string.
    return (permutation, threes, len(matrix),len(matrix[0]))

def counts(perm):
    '''
    Finds the number of types in a permutation; that is, the number of 1s, 2s, and 0s. Sorts the permutation beforehand into 0,1,2.
    Input: multiset permutation
    Output: number of types, in order starting at 0.
    '''
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

def potential(perm, counts):
    '''
    Finds the potential, or the number of possible multiset permutations.
    Input: multiset permutation.
    Output: potential.
    Source-- Wikipedia: https://en.wikipedia.org/wiki/Permutation#Permutations_of_multisets
    '''
    denominator = 1
    for count in counts:
        denominator *= math.factorial(count)

    return (math.factorial(len(perm)) / denominator)


def rank(perm,inLength,inCount,inPot):
    '''
    Ranks permutation into an integer.
    Input: permutation, length of permutation, number of types, and potential.
    Output: ranked integer.
    Source-- Pavel Savara. Helped by Feston.
    '''
    length = inLength
    count = inCount[:]
    pot = inPot

    rankIndex = 0
    for i in perm:
        offset = 0
        typeNumber = int(i)
        for j in range(typeNumber):
            offset += count[j]

        #Calculations similar to Pavel Savara's unrank function.
        rankIndex += (pot * offset) / length

        pot *= count[typeNumber]
        pot /= length

        length -= 1
        count[typeNumber] -= 1


    return rankIndex

def unrank(rankIndex,inLength,inCount,inPot):
    '''
    Turns ranked integer into a multiset permutation.
    Input: rank integer, length of permutation, number of types, and potential.
    Output: multiset permutation, as an array.
    Source-- Pavel Savara.
    '''
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
    '''
    Turns multiset permutation into matrix.
    Input: permutation, threes position, number of rows, number of columns.
    Output: matrix.
    '''
    #Turns perm into string.
    permstr = ""
    for item in perm:
        permstr += str(item)

    matrix = []
    for i in range(rowNum): #Creates matrix.
        row = [0]*(colNum)
        matrix.append(row)

    for point in threes:
        matrix[point[0]][point[1]] = 3 #Adds threes.

    i = 0
    for ri,row in enumerate(matrix):
        for ci,column in enumerate(row):
            #Adds value if not a 3.
            if matrix[ri][ci] == 3:
                pass
            else:
                matrix[ri][ci] = int(permstr[i])
                i += 1

    return np.array(matrix)
