import array

def checker(inputSeq, outputSeq):
    arr = array.array('i',(0 for i in range(10000)))
    checkerOutputSeq = []

    for line in inputSeq:
        lineSplit = line.split()
        command, num = lineSplit[0], int(lineSplit[1])
        
        if command == 'I':
            if arr[num] == 0:
                arr[num] = 1
                checkerOutputSeq.append(num)
            else:
                checkerOutputSeq.append(0)

        elif command == "D" :
            if arr[num] == 1:
                arr[num] = 0
                checkerOutputSeq.append(num)
            else:
                checkerOutputSeq.append(0)

        elif command == "S":
            sum = 0
            for i in range(1, 10000):
                sum += arr[i]
                if sum == num:
                    break
            if sum < num:
                checkerOutputSeq.append(0)
            else:
                checkerOutputSeq.append(i)
        
        elif command == "R":
            if arr[num] == 1:
                rank = 0
                for i in range(1, num+1):
                    rank += arr[i]
                checkerOutputSeq.append(rank)
            else:
                checkerOutputSeq.append(0)

    result = True

    if len(checkerOutputSeq) != len(outputSeq):
        result = False

    for i in range(len(checkerOutputSeq)):
        if(str(checkerOutputSeq[i]) != outputSeq[i]):
            result = False
            break

    with open("checker.txt", 'w') as f:
        f.write(str(result))
        
    return result