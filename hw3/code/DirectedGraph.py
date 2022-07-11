from Vertex import Vertex
import numpy as np
from LinkedList import LinkedList
import copy

class DirectedGraph:
    def __init__(self, args):
        inputLines = self.readInput(args.inputPath)
        self.numV = int(inputLines[0])
        self.vertices = self.makeVertices() # list of vertices
        self.type = args.type
        self.adj = self.makeAdj(inputLines) # adj_mat or adj_list or adj_arr

    def makeAdj(self, inputLines):
        if self.type == "adj_mat":
            return self.makeAdjMat(inputLines)
        elif self.type == "adj_list":
            return self.makeAdjList(inputLines)
        elif self.type == "adj_arr":
            return self.makeAdjArr(inputLines)
        else:
            raise Exception('Inadequate graph type.')

    def makeAdjMat(self, inputLines):
        adjMat = np.zeros((self.numV, self.numV))
        for i in range(1, self.numV+1):
            lineSplit = list(map(int, inputLines[i].split()))
            if lineSplit[0] == 0:
                continue
            for j in range(1, lineSplit[0] + 1):
                adjMat[i-1, lineSplit[j] - 1] = 1
        return adjMat

    def makeAdjList(self, inputLines):
        adjList = []
        for i in range(1, self.numV+1):
            adjList.append(LinkedList())
            lineSplit = list(map(int, inputLines[i].split()))
            if lineSplit[0] == 0:
                continue
            for j in range(1, lineSplit[0] + 1):
                adjList[i-1].add(lineSplit[j])
        return adjList

    def makeAdjArr(self, inputLines):
        adjArr = []
        vertexDegree = []
        sumDegree = 0 # to make degree array cumulative

        for i in range(1, self.numV+1):
            lineSplit = list(map(int, inputLines[i].split()))
            sumDegree += lineSplit[0]
            vertexDegree.append(sumDegree)
            if lineSplit[0] == 0:
                continue
            adjArr.extend(lineSplit[1:])
    
        self.vertexDegree = vertexDegree # adj_arr requires another array to store degree of vertex
        return adjArr

    def readInput(self, inputPath):
        lines = []
        with open(inputPath, 'r') as f:
            lines = f.readlines()
        return lines

    def makeVertices(self):
        vertices = []
        for i in range(1, self.numV + 1):
            vertices.append(Vertex(i))
        return vertices

    def DFS(self):
        self.verticesStack = [] # to evade storing finish time to all vertices.
        for i in range(self.numV):
            if self.vertices[i].visited == False:
                self.aDFS(self.vertices[i])

    def aDFS(self, v):        
        v.visited = True
        adj = self.findAdjVertices(v.number)
        if adj:
            for j in self.findAdjVertices(v.number):
                if self.vertices[j-1].visited == False:
  
                    self.aDFS(self.vertices[j-1])
        self.verticesStack.append(v) # vertices are sorted ascending order finsih time.

    def findAdjVertices(self, num):
        if self.type == "adj_mat":
            adjVertices = []
            for j in range(self.numV):
                if self.adj[num-1, j]:
                    adjVertices.append(j+1)
            return adjVertices

        elif self.type == "adj_list":
            adjVertices = []
            currNode = self.adj[num-1].head
            while currNode is not None:
                adjVertices.append(currNode.number)
                currNode = currNode.next
            return adjVertices

        elif self.type == "adj_arr":
            beginIdx = -1
            if num == 1:
                beginIdx = 0
            else:
                beginIdx = self.vertexDegree[num-2]
            endIdx = self.vertexDegree[num-1]
            return self.adj[beginIdx:endIdx]
        
    def findAdjVerticesTransposed(self, num):     
        if self.type == "adj_mat":
            adjVertices = []
            for j in range(self.numV):
                if self.transposedAdj[num-1, j]:
                    adjVertices.append(j+1)
            return adjVertices

        elif self.type == "adj_list":
            adjVertices = []
            currNode = self.transposedAdj[num-1].head
            while currNode is not None:
                adjVertices.append(currNode.number)
                currNode = currNode.next
            return adjVertices

        elif self.type == "adj_arr":
            beginIdx = -1
            if num == 1:
                beginIdx = 0
            else:
                beginIdx = self.vertexDegreeTransposed[num-2]
            endIdx = self.vertexDegreeTransposed[num-1]
            return self.transposedAdj[beginIdx:endIdx]

    def findSCC(self):
        self.DFS() # first DFS
        self.transposedAdj = self.transposeAdj()
        self.DFSReversed() # second DFS
        return(self.SCC)
    
    def DFSReversed(self):
        self.SCC = []

        for i in range(self.numV):
            self.vertices[i].visited = False
        
        for i in range(self.numV-1, -1, -1):
            v = self.verticesStack[i] # should be accessed reversely, which makes it a stack.
            if v.visited == False:
                self.currSCC = []
                self.aDFSReversed(v)
                self.SCC.append(self.currSCC)

    def aDFSReversed(self, v):
        v.visited = True
        self.currSCC.append(v.number)
        for j in self.findAdjVerticesTransposed(v.number):
            if self.vertices[j-1].visited == False:
                self.aDFSReversed(self.vertices[j-1])
    
    def transposeAdj(self):
        if self.type == "adj_mat":
            return self.adj.T

        elif self.type == "adj_list":
            adjListTransposed = []
            for i in range(1, self.numV+1):
                adjListTransposed.append(LinkedList())
            for i in range(1, self.numV+1):
                currNode = self.adj[i-1].head
                while currNode is not None:
                    j = currNode.number
                    adjListTransposed[j-1].add(i)
                    currNode = currNode.next
            return adjListTransposed

        elif self.type == "adj_arr":
            vertexDegreeTransposed = [0] * self.numV
            adjArrTransposed = [-1] * len(self.adj)
            
            # first travel: make degree array
            for n in self.adj:
                vertexDegreeTransposed[n-1] += 1
            for k in range(1, self.numV):
                vertexDegreeTransposed[k] += vertexDegreeTransposed[k-1]

            self.vertexDegreeTransposed = copy.deepcopy(vertexDegreeTransposed)
            
            # second travel: complete transpose
            i = 1
            for j in range(len(self.adj)):
                while j >= self.vertexDegree[i-1]:
                    i += 1

                idx = vertexDegreeTransposed[self.adj[j]-1] - 1
                while adjArrTransposed[idx] != -1:
                    vertexDegreeTransposed[self.adj[j]-1] -= 1
                    idx -= 1
                adjArrTransposed[idx] = i

            return adjArrTransposed