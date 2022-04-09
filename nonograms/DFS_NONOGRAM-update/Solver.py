from typing import List
from TrangThai import PuzzleState as State
from Rangbuoc import Constraints
from Hoanvi import Permutation
import copy
import time

class PuzzleSolver:
    def __init__(self, rang_buoc: Constraints) -> None:
        self.rang_buoc : Constraints = rang_buoc
        self.hoan_vi: Permutation = Permutation(rang_buoc)
    def duyet_theo_chieu_sau(self, row: int) -> None:
        self.nodes += 1
        if row > self.max_row:
            self.max_row = row
        if not self.state.kiem_tra_dap_an(row):
            return
        if row + 1 == self.rang_buoc.so_cot:
            self.solutions.append(copy.deepcopy(self.state))
            return
        for hoan_vi in self.hoan_vi.sinh_hoan_vi(row+1):
            self.state.set_row(row+1, hoan_vi)
            self.duyet_theo_chieu_sau(row+1)
        self.state.set_row(row+1, [None for _ in range(self.rang_buoc.so_cot)])
    def solve(self) -> List[State]:
        self.state : State = State(self.rang_buoc)
        self.solutions : List[State] = []
        self.nodes = -1
        self.max_row = 0
        self.duyet_theo_chieu_sau(-1)
        return self.solutions