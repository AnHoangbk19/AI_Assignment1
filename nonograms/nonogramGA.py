import numpy as np
import random
from numpy import char, random, sort
import sys

class nonogramSol:
    def __init__(self,arrlines,arrcolumns,points):
        self.arrlines = arrlines
        self.arrcolumns = arrcolumns
        self.points = points
        self.eval = self.fitness(points)
    def fitness(self,points):
        eval = 0
        nLines = len(self.arrlines)
        nColumns = len(self.arrcolumns)
        for i in range(nLines):
            n = len(self.arrlines[i])
            columnIndex = 0
            ruleIndex = 0
            while columnIndex < nColumns or  ruleIndex < n:
                count = 0
                if ruleIndex < n:
                    currRule = self.arrlines[i][ruleIndex]
                else:
                    currRule = 0     
                while columnIndex < nColumns and points[i][columnIndex] == False:
                    columnIndex += 1    
                while columnIndex < nColumns and points[i][columnIndex] == True:
                    columnIndex += 1
                    count +=1   
                eval += abs(count - currRule)
                ruleIndex +=1
        for i in range(nColumns):
            n = len(self.arrcolumns[i])
            lineIndex = 0
            ruleIndex = 0
            while lineIndex < nLines or ruleIndex < n:
                count = 0
                if ruleIndex < n:
                    currRule = self.arrcolumns[i][ruleIndex]
                else:
                    currRule = 0
                while lineIndex < nLines and points[lineIndex][i] == False:
                    lineIndex +=1
                while lineIndex < nLines and points[lineIndex][i] == True :
                    lineIndex +=1
                    count +=1
                eval += abs(count - currRule)
                ruleIndex +=1
        return eval
def readfile(filename):
    with open(filename) as f:
        lines = True
        arrlines = []
        arrcolumns = []
        for i in f:
            if i == '-\n':
                lines = False
                continue
            temp = []
            for x in i.split():
                temp += [int(x)]
            if lines:
                arrlines += [temp]
            else:
                arrcolumns +=[temp]
    return arrlines , arrcolumns
def createpopulation(arrlines, arrcolumns, nPop):
    nLines = len(arrlines)
    nColumns = len(arrcolumns)
    sol = []
    for i in range(nPop):
        temp = np.random.randint(2, size = (nLines, nColumns), dtype= bool)
        sol += [nonogramSol(arrlines,arrcolumns,temp)]
    return sol
def check(sol):
    for i in sol:
        if i.eval == 0:
            return True
    return False
def crossover(sol,arrlines,arrcolumns,pc):
    n = len(sol)
    nLines = len(arrlines)
    nColumns = len(arrcolumns)
    worstRule = nLines*nColumns*2
    sumRule = 0
    res =[]
    for i in sol:
        sumRule += (worstRule - i.eval)
    prob = []
    for i in sol:
        temp = (worstRule - i.eval)/sumRule
        prob += [temp]
        #print(i.eval,temp)
    #print("-----------------------------------------------")
    for i in range(n):
        child1 = np.zeros((nLines,nColumns),dtype=bool)
        child2 = np.zeros((nLines,nColumns),dtype=bool)
        parent1, parent2 = random.choice(sol, p=prob, size=2)
        for l in range(nLines):
            for c in range(nColumns):
                if random.random() <= pc:
                    child1[l][c] = parent1.points[l][c]
                    child2[l][c] = parent2.points[l][c]
                else:
                    child1[l][c] = parent2.points[l][c]
                    child2[l][c] = parent1.points[l][c]
        res += [nonogramSol(arrlines,arrcolumns,child1),nonogramSol(arrlines,arrcolumns,child2)]
    return res
def mution(sol,arrlines,arrcolumns,pm):
    res = []
    nLines = len(arrlines)
    nColumns = len(arrcolumns)
    for i in sol:
        temp = np.zeros((nLines,nColumns),dtype=bool)
        for l in range(nLines):
            for c in range(nColumns):
                if random.random() > pm:
                    temp[l][c] = i.points[l][c]
                else:
                    temp[l][c] = not i.points[l][c]
        res += [nonogramSol(arrlines,arrcolumns,temp)]
    return res
def select(sol,nPop):
    res = []
    n = len(sol)
    temp = sorted(sol,key = lambda x : x.eval)
    nbest = int(7*nPop/10) 
    nrandom = nPop - nbest
    bestsol = temp[:nbest]
    othersol = temp[nbest:]
    randsol = np.ndarray.tolist(random.choice(othersol,size = nrandom))
    res = bestsol + randsol
    return res
def bestsol(sol):
    for i in sol:
        if i.eval == 0:
            return i
    return sol[0]
def GeneticAlgorithm(arrlines,arrcolumns,nPop,pc,pm):
    ite = 0
    sol = createpopulation(arrlines,arrcolumns,nPop)
    while check(sol) == False:
        sol2 = crossover(sol,arrlines,arrcolumns,pc)
        sol3 = mution(sol2,arrlines,arrcolumns,pm)
        sol = select(sol3,nPop)
        ite +=1
        print("iteration: ",ite)
        print(bestsol(sol).eval)
        printnonogram(bestsol(sol),arrlines,arrcolumns)
        print("==================")
    return bestsol(sol)
        
    
def main(filename = 'demo.txt', nPop = 100,pc = 0.7,pm =0.02):
    if len(sys.argv) > 1:
        filename = sys.argv[0]
    if len(sys.argv) > 2:
        nPop = sys.argv[1]
    if len(sys.argv) > 3:
        pc = sys.argv[2]
    if len(sys.argv) > 4:
        pm = sys.argv[3]
    l,c = readfile(filename)
    mysol = GeneticAlgorithm(l,c,nPop,pc,pm)
    print("Final Solution: ")
    printnonogram(mysol,l,c)

def printnonogram(sol,arrlines,arrcolumns):
    nLines = len(arrlines)
    nColumns = len(arrcolumns)
    res = np.zeros((nLines,nColumns),dtype = str)
    for l in range(nLines):
        for c in range(nColumns):
            if sol.points[l][c]:
                res[l][c] = "*"
            else:
                res[l][c] = "_"
    print(res)
if __name__ == "__main__":
    main()
