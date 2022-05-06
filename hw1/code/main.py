import time
import copy
import math

def readInput():
    with open("input.txt", 'r') as f:
        lines = f.readlines()
        length = int(lines[0])
        numList = list(map(int, lines[1].split()))
        i = int(lines[2])
    return length, numList, i

def deterministicSelect(length, numList, i):
    startTime = time.time()
    
    output = linearSelect(numList,0,length-1,i)

    # execution time in ms
    executedTime = int((time.time()-startTime) * 1000)

    # save result to random.txt
    with open("deter.txt", "w") as f:
        f.write(str(output)+'\n')
        f.write(str(executedTime)+"ms")

    return output, executedTime

def linearSelect(numList, p, r, i):
    # if length of list is 1, return the only element
    if p == r:
            return numList[p]
    # else if length <=5, insertion sort the list and return i-th smallest
    elif r-p+1 <= 5:
        numList = insertionSort(numList, p, r)
        return numList[p+i-1]
    # else choose not extreme pivot by recursive call
    else:
        numGroups = math.ceil((r-p+1)/5)
        lengthLastGroup = (r-p+1) % 5
        medians = list()

        # group each 5 elements and get median
        for j in range(p, r+1, 5):
            # if last group is not full, median index is different
            if r-j < 4:
                numList = insertionSort(numList, j, j+lengthLastGroup-1)
                medians.append(numList[j + (lengthLastGroup-1)//2])
            else:
                numList = insertionSort(numList, j, j+4)
                medians.append(numList[j+2])
        
        # choose median of medians as pivot recursively
        pivot = linearSelect(medians, 0, numGroups-1, numGroups//2)

        # partition with the pivot and return index of pivot
        q = partitionWithPivot(numList, p, r, pivot)

        # pivot is the k-th smallest
        k = q-p+1

        if i < k:
            return linearSelect(numList, p, q-1, i)
        elif i == k:
            return numList[q]
        else:
            return linearSelect(numList, q+1, r, i-k)

def partitionWithPivot(numList, p, r, pivot):
    # find index of pivot by traveling once
    pivotIdx = findIdx(numList, p, r, pivot)

    # swap pivot with last element and same as partition in deterministic one
    numList[r], numList[pivotIdx] = numList[pivotIdx], numList[r]

    i = p-1
    for j in range(p, r):
        if numList[j] <= pivot:
            i += 1
            numList[i], numList[j] = numList[j], numList[i]
    numList[i+1], numList[r] = numList[r], numList[i+1]
    return i+1

def findIdx(numList, p, r, pivot):
    for i in range(p, r+1):
        if numList[i] == pivot:
            return i

def insertionSort(numList, p, r):
    for i in range(p+1, r+1):
        for j in range(i-1, p-1, -1):
            if numList[j] > numList[j+1]:
                numList[j], numList[j+1] = numList[j+1], numList[j]
            else:
                break
    return numList

def randomizedSelect(length, numList, i):
    startTime = time.time()
    
    output = select(numList,0,length-1,i)

    # execution time in ms
    executedTime = int((time.time()-startTime) * 1000)

    # save result to deter.txt
    with open("random.txt", "w") as f:
        f.write(str(output)+'\n')
        f.write(str(executedTime)+"ms")

    return output, executedTime

def select(numList, p, r, i):
    # if length of list is 1, return the only element
    if p == r:
        return numList[p]

    # else, make partition and return index of pivot
    q = partition(numList, p, r)

    # pivot is the k-th smallest
    k = q-p+1

    if i < k:
        return select(numList, p, q-1, i)
    elif i == k:
        return numList[q]
    else:
        return select(numList, q+1, r, i-k)

def partition(numList, p, r):
    # use last element as pivot
    pivot = numList[r]
    i = p-1
    for j in range(p, r):
        if numList[j] <= pivot:
            i += 1
            numList[i], numList[j] = numList[j], numList[i]
    numList[i+1], numList[r] = numList[r], numList[i+1]
    return i+1

def checker(numList, i, output, mode):
    # record the number of smaller and tie by traveling the list once
    countSmaller = 0
    countTie = 0
    for x in numList:
        if x < output:
            countSmaller += 1
        elif x == output:
            countTie += 1
    
    # the output is correct iff countSmaller < i <= countSmaller + countTie
    # True or False for each algorithm
    result = (i > countSmaller) and (i <= countSmaller + countTie)
    
    # save the result of checker together in result.txt
    if mode == "random":
        with open("result.txt", "w") as f:
            f.write(str(result)+'\n')
    else:
        with open("result.txt", "a") as f:
            f.write(str(result))
    
    return result

def main():
    length, numList, i = readInput()
    
    output, time = randomizedSelect(length, copy.deepcopy(numList), i)
    print("i-th smallest number by randomized selection: ", output)
    print("Execution time by randomized selection: ", time)
    print("Check randomized selection:", checker(numList, i, output, "random"))

    output, time = deterministicSelect(length, copy.deepcopy(numList), i)
    print("i-th smallest number by deterministic selection: ", output)
    print("Execution time by deterministic selection: ", time)
    print("Check deterministic selection:", checker(numList, i, output, "deter"))

main()