#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from evaluator import *  # Adjust with your actual module

def run_nexus_file(file_path):
    try:
        with open(file_path, 'r') as file:
            code = file.read()
        print(f"Running {file_path}...\n")
        execute(code)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"Error while executing the code: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: nexus <file.nx>")
        return

    file_path = sys.argv[1]
    if not file_path.endswith(".nx"):
        print("Error: File extension must be .nx")
        return

    run_nexus_file(file_path)

if __name__ == "__main__":
    main()
