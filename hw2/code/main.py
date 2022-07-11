import argparse
from OSTree import OSTree
from checker import checker
from time import time

def readInput(input):
    lines = []
    with open(input, 'r') as f:
        lines = f.readlines()
    for line in lines:
        print(line.strip())
    return lines

def saveOutputFile(inputSeq, outputSeq):
    with open("output.txt", 'w') as f:
        for i in range(len(inputSeq)):
            if i == 0:
                f.write(inputSeq[i].strip())
            else:
                f.write("\n" + inputSeq[i].strip())

        for j in range(len(outputSeq)):
            f.write("\n" + outputSeq[j].strip())

def runCommand(tree, command, num):

    if command == 'I':
        output = tree.insert(num)
    elif command == "D" :
        output = tree.delete(num)
    elif command == "S":
        output = tree.osSelect(num)
    elif command == "R":
        output = tree.osRank(num)
    
    print(f'Output for {command} {str(num)}: {output}')
    return output

def main(args):
    input = args.input
    inputSeq = readInput(input)
    outputSeq = []
    
    tree = OSTree()

    for line in inputSeq:
        lineSplit = line.split()
        command, num = lineSplit[0], int(lineSplit[1])

        output = runCommand(tree, command, num)
        outputSeq.append(str(output))
    
    saveOutputFile(inputSeq, outputSeq)
    checkerResult = checker(inputSeq, outputSeq)
    print(f'Checker Result: {checkerResult}')


if __name__ == '__main__':
    start = time()
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True)
    args = parser.parse_args()
    main(args)
    print(f'Executed Time: {round(time() - start, 2)}s')