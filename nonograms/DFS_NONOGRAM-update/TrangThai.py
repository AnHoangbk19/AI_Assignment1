from Rangbuoc import Constraints
from typing import Union, List

class PuzzleState:
    EMPTY = False
    BLOCK = True

    def __init__(self, rang_buoc: Constraints) -> None:
        self.rang_buoc = rang_buoc
        self._state = [
            [None for _ in range(rang_buoc.so_cot)] for _ in range(rang_buoc.so_hang)
        ]

    def kiem_tra_gioi_han(self, row: int, column: int) -> bool:
        return (0 <= row < self.rang_buoc.so_hang) and \
               (0 <= column < self.rang_buoc.so_hang)

    def set(self, row: int, column: int, value: Union[bool, None]) -> None:
        assert self.kiem_tra_gioi_han(row, column)
        self._state[row][column] = value

    def set_row(self, row: int, values: List[bool]) -> None:
        assert len(values) == self.rang_buoc.so_cot
        self._state[row] = values

    def get(self, row: int, column: int) -> Union[bool, None]:
        assert self.kiem_tra_gioi_han(row, column)
        return self._state[row][column]

    def __str__(self) -> str:
        return "\n".join(
            [ "┌" + "".join('─' for _ in range(self.rang_buoc.so_cot)) + "┐" ] + \
            [ "│" + "".join(
                        "x" if self._state[i][j] else " " for j in range(self.rang_buoc.so_cot) 
                    ) + "│"
                    for i in range(self.rang_buoc.height) ] + \
            [ "└" + "".join('─' for _ in range(self.rang_buoc.so_cot)) + "┘"]
        )
        
    def kiem_tra_dap_an(self, so_hang_xong: int) -> bool:
        if so_hang_xong <= 0:
            return True

        so_hang_xong += 1
        
        for i in range(self.rang_buoc.so_cot):
            rang_buoc_cot = self.rang_buoc.chi_so_cot[i]
            if len(rang_buoc_cot) == 0:
                for j in range(so_hang_xong):
                    if self.get(j, i):
                        return False
                continue

            in_block = False
            block_index = 0
            num_cells = None 
            for j in range(so_hang_xong):
                if self.get(j, i): 
                    if in_block:
                        num_cells -= 1  
                        if num_cells < 0:
                            return False
                    else:
                        if block_index >= len(rang_buoc_cot):
                            return False 
                        num_cells = rang_buoc_cot[block_index] - 1
                        block_index += 1
                        in_block = True
                elif in_block:
                    if num_cells != 0: 
                        return False 
                    in_block = False
            
            if so_hang_xong == self.rang_buoc.so_hang and block_index != len(rang_buoc_cot):
                return False 
            o_con_lai = self.rang_buoc.so_hang - so_hang_xong
            rang_buoc_con_lai = rang_buoc_cot[block_index:]
            if sum(rang_buoc_con_lai) + len(rang_buoc_con_lai) - 1 > o_con_lai:
                return False
        return True 
