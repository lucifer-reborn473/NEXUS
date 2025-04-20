#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from evaluator import *  
import time
from tqdm import tqdm
from pprint import pprint
from bytecode_eval_new import *

def run_nexus_file(file_path,display_ast=False):
    """Runs the given Nexus file and tracks execution time."""
    start_time = time.time()
    try:
        with open(file_path, 'r') as file:
            code = file.read()
        if display_ast:
            print(f"Displaying AST for {file_path}:\n")
            tree = parse(code)
            pprint(tree)
            print('\n')
        print(f"Running {file_path}...\n")
        start_time = time.perf_counter_ns()
        run_program(code)
        end_time = time.perf_counter_ns()
        execution_time_us = (end_time - start_time) / 1000  # Convert nanoseconds to microseconds
        print(f"\nProgram execution completed in {execution_time_us:.2f} microseconds.")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"Error while executing the code: {e}")
   
def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: nexus <file.nx> [--ast]")
        return

    file_path = sys.argv[1]
    if not file_path.endswith(".nx"):
        print("Error: File extension must be .nx")
        return

    display_ast = len(sys.argv) == 3 and sys.argv[2] == "--ast"
    run_nexus_file(file_path, display_ast)

if __name__ == "__main__":
    main()
