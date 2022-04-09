import sys
import os
import json
from typing import List, Dict, Any
from Rangbuoc import Constraints
from Solver import PuzzleSolver as Solver
from TrangThai import PuzzleState as State

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

def process_puzzle(path: str) -> None:
    if not os.path.isfile(path):
        
        return

    try:
        f = open(path,encoding='utf-8')
        json_object = json.load(f)
   
    except json.JSONDecodeError as error:
        return
    else:
        f.close()

    errors, instance = Constraints.kiem_tra_dau_vao(json_object)
   
    solver: Solver = Solver(instance)
    solutions: List[State] = solver.solve()
    
    first = True
    for index, solution in enumerate(solutions):
        if not first:
            print()
        first = False
        print(solution)
    
def main() -> None:
  process_puzzle('test.json')

if __name__ == "__main__":
    main()

