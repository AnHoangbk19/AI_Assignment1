import sys
import os
import json
from tracemalloc import start
from turtle import end_fill
from typing import List, Dict, Any
from Constraints import Constraints
from PuzzleSolver import PuzzleSolver as Solver
from PuzzleState import PuzzleState as State
from time import  time
import tracemalloc
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

def process_puzzle(path: str) -> None:
    if not os.path.isfile(path):
        print("{} is not a regular file.".format(path))
        return

    try:
        f = open(path,encoding='utf-8')
        json_object = json.load(f)
    except OSError as error:
        print("An error occurred while opening the file {}".format(path),
              file=sys.stderr)
        print(error.strerror, file=sys.stderr)
        return
    except json.JSONDecodeError as error:
        print("An error occurred while parsing the JSON file {}".format(path),
              file=sys.stderr)
        return
    else:
        f.close()

    errors, instance = Constraints.validate_json(json_object)
    if errors:
        print("The configuration file is not valid.", file=sys.stderr)
        print("Errors:", file=sys.stderr)
        print("\t", end="", file=sys.stderr)
        print("\n\t".join(errors), file=sys.stderr)
        return

    solver: Solver = Solver(instance)
    solutions: List[State] = solver.solve()
    
    first = True
    for index, solution in enumerate(solutions):
        if not first:
            print()
        first = False
        print(solution)
    
def main() -> None:
  process_puzzle('15x15.json')

if __name__ == "__main__":
    star = time()
    tracemalloc.start()
    main()
    end = time()
    print("Time: ",end - star,"s")
    print("Memory useage (current,peak): ",tracemalloc.get_traced_memory())
    tracemalloc.stop()

