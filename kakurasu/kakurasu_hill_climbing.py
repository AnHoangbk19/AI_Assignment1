from asyncio.windows_events import NULL
from enum import Enum, unique, Flag
from tkinter.tix import Tree
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
        x = 0
        for i in range(self.rowNum):
            x += (i + 1)
        y = 0
        for i in range(self.colNum):
            y += (i + 1)
        self.upRow = y
        self.upRowNoLast = self.upRow - self.rowNum
        self.upCol = x
        self.upColNoLast = self.upCol - self.colNum

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

    # Check if n_th row is incomplete or not
    def isIncompleteRow(self, n):
        res = []
        for i in range(self.colNum):
            if self.boardGrid[n][i] == Color.GREY:
                res.append(i)
        return res

    # Check if m_th col is incomplete or not
    def isIncompleteCol(self, m):
        res = []
        for i in range(self.rowNum):
            if self.boardGrid[i][m] == Color.GREY:
                res.append(i)
        return res

    # Check if the board is incomplete or not
    def isIncompleteBoard(self):
        for i in range(self.colNum):
            for j in range(self.rowNum):
                if self.boardGrid[i][j] == Color.GREY:
                    return False
        return True


# sumUpBoard() returns lists that store sumup values (by adding sum values with WHITE cell) of rows ans cols
def sumUpBoard(board):
    sumUpRows = board.sumRows.copy()
    sumUpCols = board.sumCols.copy()
    for i in range(board.rowNum):
        for j in range(board.colNum):
            if board.boardGrid[i][j] == Color.WHITE:
                sumUpRows[i] += j + 1
                sumUpCols[j] += i + 1
    return [sumUpRows, sumUpCols]


# sumDownBoard() returns lists that store sumdown values (by substracting sum values with BLACK cell) of rows ans cols
def sumDownBoard(board):
    sumDownRows = board.sumRows.copy()
    sumDownCols = board.sumCols.copy()
    for i in range(board.rowNum):
        for j in range(board.colNum):
            if board.boardGrid[i][j] == Color.BLACK:
                sumDownRows[i] -= j + 1
                sumDownCols[j] -= i + 1
    return [sumDownRows, sumDownCols]


# subset_sum() return list of posibble combinations reach given sum (target)
def subset_sum(numbers, target, partial, res):
    s = sum(partial)
    # check if the partial sum is equals to target
    if s == target:
        res.append(partial)
        print("sum(%s)=%s" % (partial, target))
    if s >= target:
        return  # if we reach the number why bother to continue

    for i in range(len(numbers)):
        n = numbers[i]
        remaining = numbers[i+1:]
        subset_sum(remaining, target, partial + [n], res)
    return res


# findCommon2() return list of common elements of 2 lists
def findCommon2(ar1, ar2, n1, n2):
    res = []
    i, j = 0, 0
    while (i < n1 and j < n2):
        if (ar1[i] == ar2[j]):
            res.append(ar1[i])
            i += 1
            j += 1
        elif ar1[i] < ar2[j]:
            i += 1
        else:
            j += 1
    return res


# findCommon3() return list of common elements of 3 lists
def findCommon3(ar1, ar2, ar3, n1, n2, n3):
    res = []
    i, j, k = 0, 0, 0
    while (i < n1 and j < n2 and k < n3):
        if (ar1[i] == ar2[j] and ar2[j] == ar3[k]):
            res.append(ar1[i])
            i += 1
            j += 1
            k += 1
        elif ar1[i] < ar2[j]:
            i += 1
        elif ar2[j] < ar3[k]:
            j += 1
        else:
            k += 1
    return res


# findNextState() applies heuristics to searchs for a possible move to a better state
def findNextState(board):
    isBetter = False
    # Try summing up rows and cols to find move
    # print("Sum up board: ", sumUp)  # FOR CHECKING
    # Check rows if there is a move
    sumUp = sumUpBoard(board)
    for i in range(len(sumUp[0])):
        if ((board.upRow - sumUp[0][i]) == 1):
            if board.boardGrid[i][0] == Color.GREY:
                board.boardGrid[i][0] = Color.WHITE
                isBetter = True
            for j in range(1, board.rowNum):
                if board.boardGrid[i][j] == Color.GREY:
                    board.boardGrid[i][j] = Color.BLACK
                    isBetter = True
        elif ((board.upRow - sumUp[0][i]) == 2):
            if board.boardGrid[i][0] == Color.GREY:
                board.boardGrid[i][0] = Color.BLACK
                isBetter = True
            if board.boardGrid[i][1] == Color.GREY:
                board.boardGrid[i][1] = Color.WHITE
                isBetter = True
            for j in range(2, board.rowNum):
                if board.boardGrid[i][j] == Color.GREY:
                    board.boardGrid[i][j] = Color.BLACK
                    isBetter = True
        elif sumUp[0][i] > board.upRowNoLast:
            num = board.upRow - sumUp[0][i]
            for j in range(num, board.colNum):
                if board.boardGrid[i][j] == Color.GREY:
                    board.boardGrid[i][j] = Color.BLACK
                    isBetter = True
        # board1.printBoard()  # FOR CHECKING
    # Check cols if there is a move
    sumUp = sumUpBoard(board)
    for i in range(len(sumUp[1])):
        if ((board.upCol - sumUp[1][i]) == 1):
            if board.boardGrid[0][i] == Color.GREY:
                board.boardGrid[0][i] = Color.WHITE
                isBetter = True
            for j in range(1, board.colNum):
                if board.boardGrid[j][i] == Color.GREY:
                    board.boardGrid[j][i] = Color.BLACK
                    isBetter = True
        elif ((board.upRow - sumUp[1][i]) == 2):
            if board.boardGrid[0][i] == Color.GREY:
                board.boardGrid[0][i] = Color.BLACK
                isBetter = True
            if board.boardGrid[1][i] == Color.GREY:
                board.boardGrid[1][i] = Color.WHITE
                isBetter = True
            for j in range(2, board.colNum):
                if board.boardGrid[j][i] == Color.GREY:
                    board.boardGrid[j][i] = Color.BLACK
                    isBetter = True
        elif sumUp[1][i] > board.upColNoLast:
            num = board.upCol - sumUp[1][i]
            for j in range(num, board.colNum):
                if board.boardGrid[j][i] == Color.GREY:
                    board.boardGrid[j][i] = Color.BLACK
                    isBetter = True
        # board1.printBoard()  # FOR CHECKING
    # Try summing down rows and cols to find move
    # print("Sum down board: ", sumDown)  # FOR CHECKING
    # Check rows if there is a move
    sumDown = sumDownBoard(board)
    for i in range(len(sumDown[0])):
        if sumDown[0][i] == 1:
            if board.boardGrid[i][0] == Color.GREY:
                board.boardGrid[i][0] = Color.BLACK
                isBetter = True
            for j in range(1, board.rowNum):
                if board.boardGrid[i][j] == Color.GREY:
                    board.boardGrid[i][j] = Color.WHITE
                    isBetter = True
        elif sumDown[0][i] == 2:
            if board.boardGrid[i][0] == Color.GREY:
                board.boardGrid[i][0] = Color.WHITE
                isBetter = True
            if board.boardGrid[i][1] == Color.GREY:
                board.boardGrid[i][1] = Color.BLACK
                isBetter = True
            for j in range(2, board.rowNum):
                if board.boardGrid[i][j] == Color.GREY:
                    board.boardGrid[i][j] = Color.WHITE
                    isBetter = True
        elif sumDown[0][i] < board.rowNum:
            for j in range(sumDown[0][i], board.rowNum):
                if board.boardGrid[i][j] == Color.GREY:
                    board.boardGrid[i][j] = Color.WHITE
                    isBetter = True
        # board1.printBoard()  # FOR CHECKING
    # Check cols if there is a move
    sumDown = sumDownBoard(board)
    for i in range(len(sumDown[1])):
        if sumDown[1][i] == 1:
            if board.boardGrid[0][i] == Color.GREY:
                board.boardGrid[0][i] = Color.BLACK
                isBetter = True
            for j in range(1, board.colNum):
                if board.boardGrid[j][i] == Color.GREY:
                    board.boardGrid[j][i] = Color.WHITE
                    isBetter = True
        elif sumDown[1][i] == 2:
            if board.boardGrid[0][i] == Color.GREY:
                board.boardGrid[0][i] = Color.WHITE
                isBetter = True
            if board.boardGrid[1][i] == Color.GREY:
                board.boardGrid[1][i] = Color.BLACK
                isBetter = True
            for j in range(2, board.colNum):
                if board.boardGrid[j][i] == Color.GREY:
                    board.boardGrid[j][i] = Color.WHITE
                    isBetter = True
        elif sumDown[1][i] < board.colNum:
            for j in range(sumDown[1][i], board.colNum):
                if board.boardGrid[j][i] == Color.GREY:
                    board.boardGrid[j][i] = Color.WHITE
                    isBetter = True
        # board1.printBoard()  # FOR CHECKING
    # Above stricts are appliable then return
    if isBetter == True:
        return isBetter
    # If they are not, use the last one
    else:
        # Check rows if there is a move
        sumDown = sumDownBoard(board)
        for i in range(board.rowNum):
            pos = board.isIncompleteRow(i)
            if len(pos) != 0:
                for x in range(len(pos)):
                    pos[x] += 1
                print("Empty pos at row ", i + 1, ":", pos)  # FOR CHECKING
                combins = []
                subset_sum(pos, sumDown[0][i], [], combins)
                if len(combins) == 1:
                    for y in combins[0]:
                        if board.boardGrid[i][y - 1] == Color.GREY:
                            board.boardGrid[i][y - 1] = Color.BLACK
                            isBetter = True
                    for j in range(board.colNum):
                        if board.boardGrid[i][j] == Color.GREY:
                            board.boardGrid[i][j] = Color.WHITE
                elif len(combins) == 2:
                    commonVals = findCommon2(
                        combins[0], combins[1], len(combins[0]), len(combins[1]))
                    for y in commonVals:
                        if board.boardGrid[i][y - 1] == Color.GREY:
                            board.boardGrid[i][y - 1] = Color.BLACK
                            isBetter = True
                elif len(combins) == 3:
                    commonVals = findCommon3(
                        combins[0], combins[1], combins[2], len(combins[0]), len(combins[1]), len(combins[2]))
                    for y in commonVals:
                        if board.boardGrid[i][y - 1] == Color.GREY:
                            board.boardGrid[i][y - 1] = Color.BLACK
                            isBetter = True
        # Check cols if there is a move
        sumDown = sumDownBoard(board)
        for i in range(board.colNum):
            pos = board.isIncompleteCol(i)
            if len(pos) != 0:
                for x in range(len(pos)):
                    pos[x] += 1
                print("Empty pos at col ", i + 1, ":", pos)  # FOR CHECKING
                combins = []
                subset_sum(pos, sumDown[1][i], [], combins)
                if len(combins) == 1:
                    for y in combins[0]:
                        if board.boardGrid[y - 1][i] == Color.GREY:
                            board.boardGrid[y - 1][i] = Color.BLACK
                            isBetter = True
                    for j in range(board.rowNum):
                        if board.boardGrid[j][i] == Color.GREY:
                            board.boardGrid[j][i] = Color.WHITE
                elif len(combins) == 2:
                    commonVals = findCommon2(
                        combins[0], combins[1], len(combins[0]), len(combins[1]))
                    for y in commonVals:
                        if board.boardGrid[y - 1][i] == Color.GREY:
                            board.boardGrid[y - 1][i] = Color.BLACK
                            isBetter = True
                elif len(combins) == 3:
                    commonVals = findCommon3(
                        combins[0], combins[1], combins[2], len(combins[0]), len(combins[1]), len(combins[2]))
                    for y in commonVals:
                        if board.boardGrid[y - 1][i] == Color.GREY:
                            board.boardGrid[y - 1][i] = Color.BLACK
                            isBetter = True
    return isBetter


if __name__ == "__main__":
    # board1 = Board(6, 6, [13, 18, 17, 18, 9, 17], [16, 16, 9, 12, 20, 16])
    # board1 = Board(6, 6, [15, 14, 3, 13, 20, 10], [11, 13, 8, 14, 15, 12])
    # board1 = Board(7, 7, [3, 13, 1, 13, 4, 11, 5], [9, 3, 5, 2, 13, 10, 6])
    # board1 = Board(7, 7, [1, 18, 17, 24, 21, 9, 8],
    #                [12, 15, 27, 11, 16, 9, 14])
    # board1 = Board(8, 8, [35, 27, 27, 32, 25, 31, 32, 24], [
    #                35, 31, 34, 15, 25, 31, 33, 28])
    # board1 = Board(8, 8, [14, 24, 14, 30, 16, 22, 10, 17], [
    #                2, 6, 6, 34, 9, 21, 25, 16])
    # board1 = Board(9, 9, [23, 33, 35, 42, 40, 42, 30, 38, 41], [
    #                41, 40, 29, 25, 39, 41, 38, 38, 42])
    # board1 = Board(9, 9, [5, 11, 23, 23, 17, 32, 17, 18, 10], [
    #                25, 32, 10, 1, 5, 21, 37, 12, 21])
    board1 = Board(10, 10, [36, 31, 29, 17, 20, 14, 33, 37, 17, 22], [
                   41, 50, 48, 44, 8, 3, 42, 25, 26, 9])
    board1.printBoard()
    # print("Row number: ", board1.rowNum)
    # print("Col number: ", board1.colNum)
    # print("Sum rows: ", board1.sumRows)
    # print("Sum cols: ", board1.sumCols)
    # print("Up rows: ", board1.upRow, "-", board1.upRowNoLast)
    # print("Up cols: ", board1.upCol, "-", board1.upColNoLast)

    # findNextState(board1)
    # board1.printBoard()
    # findNextState(board1)
    # board1.printBoard()
    isBetter = True
    while isBetter:
        isBetter = findNextState(board1)
        board1.printBoard()
