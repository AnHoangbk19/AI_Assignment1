from enum import Enum, unique, Flag
from turtle import color
import numpy as np


# Class Color represents a cell in board, GREY cells are unsolved cells
@unique
class Color(Enum):
    WHITE = 0
    GREY = 1
    BLACK = 2


# Class Board is an rowNum rows by colNum columns grid of Color
class Board:
    # Constructor  
    
    def __init__(self, rowNum, colNum, sumRows, sumCols):
        self.rowNum = rowNum  # Row number
        self.colNum = colNum  # Column number
        self.sumRows = sumRows.copy()  # A list stores sum of each row of board
        self.sumCols = sumCols.copy()  # A list stores sum of each column of board
        # Two dimensions list represents rowNum x colNum board grid
        self.boardGrid = np.full((self.rowNum, self.colNum), Color.GREY)
    
    def sumRow(self):
        res = []
        for i in range(self.rowNum):
            for j in range(self.colNum):
                tempt = 0
                if self.boardGrid[i][j] == Color.BLACK:
                    tempt += 1
            res += [tempt]
        return res
    
    def sumBoard(self):
        rowSum = [0 for i in range(self.rowNum)]
        colSum = [0 for i in range(self.colNum)]
        for i in range(self.rowNum):
            for j in range(self.colNum):
                if self.boardGrid[i][j] == Color.BLACK:
                    rowSum[i] += j + 1
                    colSum[j] += i + 1
        return [rowSum, colSum]
    
    def islegitBoard(self):
        res = self.sumBoard()
        rowSum = res[0]
        colSum = res[1]
        flag = True
        for i in range(self.rowNum):
            if rowSum[i] > self.sumRows[i]:
                flag = False
                return flag
        for i in range(self.colNum):
            if colSum[i] > self.sumCols[i]:
                flag = False
                return flag
        return flag        

    def isFinalAnswer(self):
        res = self.sumBoard()
        rowSum = res[0]
        colSum = res[1]
        flag = True
        for i in range(self.rowNum):
            if rowSum[i] == self.sumRows[i]:
                flag = False
        for i in range(self.colNum):
            if colSum[i] == self.sumCols[i]:
                flag = False
        return flag

    def Gridcopy(self, board):
        for i in range(self.rowNum):
            for j in range(self.colNum):
                self.boardGrid[i][j] = board.boardGrid[i][j]

    # Print the board
    def printBoard(self):
        for i in range(self.rowNum):
            for j in range(self.colNum):
                if self.boardGrid[i][j] == Color.BLACK:
                    print("1", end="\t")
                elif self.boardGrid[i][j] == Color.GREY:
                    print("?", end="\t")
                else:
                    print("0", end="\t")
            print(self.sumRows[i])
        for x in range(len(self.sumCols)):
            print(self.sumCols[x], end="\t")
        print("")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

class Board_state:
    def __init__(self, board, CurCol):
        self.board = board
        self.CurCol = CurCol
    def print_BS(self):
        self.board.printBoard()
        
    
def find_combi(numlist, target, maxE):
    print("enter finding combination")
    ele_list = [x + 1 for x in range(maxE)]
    cur = 0
    selected_num = []
    iterator_list = []
    while(1):
        if sum(selected_num) + ele_list[cur] == target:
            numlist += [selected_num + [ele_list[cur]]]
        elif sum(selected_num) + ele_list[cur] < target:
            if cur < maxE - 1:
                selected_num += [ele_list[cur]]
                iterator_list += [cur]
        else:
            if selected_num:
                selected_num.pop()
                cur = iterator_list.pop()
            else:
                break
        cur += 1
        if cur == maxE:
            if selected_num:
                selected_num.pop()
                cur = iterator_list.pop() + 1
            else:
                break
            
def color_board(board, numlist, col):
    for i in range(board.rowNum):
        if (i + 1) in numlist:
            board.boardGrid[i][col] = Color.BLACK
        else:
            board.boardGrid[i][col] = Color.WHITE           
                
def find_next_state(board_list):
    while(board_list):
        print("start printing current state:\n")
        Board_state1 = board_list.pop()
        board1 = Board_state1.board
        board1.printBoard()
        col = Board_state1.CurCol
        if col == board1.rowNum:
            return board1
        numlists = []
        find_combi(numlists, board1.sumCols[col], board1.rowNum)
        for x in numlists:
            board2 = Board(board1.rowNum, board1.colNum, board1.sumRows, board1.sumCols)
            board2.Gridcopy(board1)
            color_board(board2, x, col)
            if board2.islegitBoard():
                board_list += [Board_state(board2, col + 1)]
        print("end of printing\n")
    return NULL
                    
                
            
if __name__ == "__main__":
    
    boardlist = []
    # board1 = Board(9, 9, [17, 28, 35, 11, 31, 9, 13, 42, 18], [28, 12, 44, 15, 34, 13, 11, 17, 35])
    # board1 = Board(9, 9, [12, 8, 9, 15, 1, 15, 11, 5, 13], [6, 8, 9, 9, 8, 9, 10, 12, 11])
    # board1 = Board(8, 8, [16, 27, 9, 24, 9, 22, 21, 11], [27, 17, 22, 25, 32, 1, 12, 16]) #ID: 1,356,089
    # board1 = Board(9, 9, [23, 33, 35, 42, 40, 42, 30, 38, 41], [
    #                 41, 40, 29, 25, 39, 41, 38, 38, 42])
    # board1 = Board(7, 7, [3, 13, 1, 13, 4, 11, 5], [9, 3, 5, 2, 13, 10, 6])
    board1 = Board(6, 6, [17, 18, 12, 10, 12, 11], [15, 18, 16, 6, 6, 17])
    board_list = [Board_state(board1, 0)]
    board2 = find_next_state(board_list)
    if board2:
        board2.printBoard()
    else:
        print("Not found")
