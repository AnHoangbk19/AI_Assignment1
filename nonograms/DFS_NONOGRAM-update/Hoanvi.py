from typing import List, Dict
from TrangThai import PuzzleState as State
from Rangbuoc import Constraints    
    
class Permutation:
    def __init__(self, rang_buoc: Constraints) -> None:
        self.rang_buoc = rang_buoc
        self.dem: Dict[int, List[List[bool]]] = dict()

    def sinh_hoan_vi(self, hang: int) -> List[bool]:
        if hang in self.dem:
            return self.dem[hang]

        blocks: List[int] = self.rang_buoc.rows[hang]
        if not blocks:
            return [[State.EMPTY for _ in range(self.rang_buoc.width)]]

        vi_tri = [0]
        for block in range(1, len(blocks)):
            vi_tri.append(vi_tri[-1] + blocks[block - 1] + 1)
        self.dem[hang] = []
        self.hoan_vi_tiep_theo(hang, vi_tri, len(vi_tri) - 1)
        return self.cache[hang]

    def vi_tri_cho_hang(self, row: int, vi_tri: List[int]) -> List[bool]:
        blocks = [State.EMPTY for _ in range(self.rang_buoc.so_cot)]
        for index, pos in enumerate(vi_tri):
            length = self.rang_buoc.chi_so_hang[row][index]
            blocks[pos:pos+length] = [State.BLOCK for _ in range(length)]
        return blocks

    def di_chuyen_block(self, row: int, vi_tri: List[int], chi_so_block: int) -> bool:
        if chi_so_block + 1 == len(vi_tri):
            return vi_tri[chi_so_block] + self.rang_buoc.chi_so_hang[row][chi_so_block] < self.rang_buoc.so_cot
        
        return vi_tri[chi_so_block] + self.rang_buoc.chi_so_hang[row][chi_so_block] + 1 < vi_tri[chi_so_block + 1]

    def hoan_vi_tiep_theo(self, row: int, positions: List[int], block_index: int) -> None:
        self.dem[row].append(self.vi_tri_cho_hang(row, positions))
        if block_index < 0:
            return

        while self.di_chuyen_block(row, positions, block_index):
            positions[block_index] += 1
            self.hoan_vi_tiep_theo(row, [p for p in positions], block_index - 1)
        

        
