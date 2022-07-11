from DirectedGraph import DirectedGraph
import argparse
from time import time
import sys

def printOutput(scc, executedTime, type):
    print(f"Strongly Connected Components with {type}:")
    for comp in scc:
        print(comp)
    print(f"Execution Time: {executedTime}ms")

def saveOutput(scc, executedTime, outputPath):
    with open(outputPath, 'w') as f:
        for i in range(len(scc)):
            line = ""
            for j in range(len(scc[i])):
                line += str(scc[i][j])
                if j + 1 < len(scc[i]):
                    line += " "
            line += "\n"
            f.write(line)
        f.write(str(executedTime) + "ms")

def sortSCC(scc):
    for comp in scc:
        comp.sort()
    scc.sort(key = lambda x: str(x[0]))
    return scc

def main(args):
    graph = DirectedGraph(args)
    
    beginTime = time()
    scc = graph.findSCC()
    endTime = time() - beginTime

    scc = sortSCC(scc)

    printOutput(scc, round(endTime * 1000), args.type)
    saveOutput(scc, round(endTime * 1000), args.outputPath)


if __name__ == '__main__':
    sys.setrecursionlimit(10000)
    parser = argparse.ArgumentParser(description='Find strongly connected components of a directed graph.')
    parser.add_argument('inputPath')
    parser.add_argument('outputPath')
    parser.add_argument('type')
    args = parser.parse_args()
    main(args)