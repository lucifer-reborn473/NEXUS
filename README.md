# Compiler Project

This project is a simple compiler that includes a lexer, parser, and evaluator for a custom programming language. The language supports basic constructs such as variables, arithmetic operations, conditional statements, and loops, including the implementation of while loops.

## Project Structure

```
compiler-project
├── src
│   ├── lexer.py          # Lexer implementation for tokenizing source code
│   ├── parser.py         # Parser for constructing the abstract syntax tree (AST)
│   ├── evaluator.py       # Evaluator for executing the AST
│   ├── context.py        # Manages execution context and variable storage
│   ├── tokens.py         # Defines token types used by the lexer and parser
│   ├── main.py           # Entry point for the compiler
│   └── examples
│       └── sample-code.txt # Example code demonstrating language features
├── tests
│   ├── test_lexer.py     # Unit tests for the lexer
│   ├── test_parser.py     # Unit tests for the parser
│   ├── test_evaluator.py  # Unit tests for the evaluator
│   └── test_examples.py    # Tests for example code output
├── requirements.txt       # Lists dependencies required to run the project
└── README.md              # Documentation for the project
```

## Features

- **Lexer**: Tokenizes the input source code, recognizing keywords, operators, and other tokens, including the new "while" keyword.
- **Parser**: Constructs an abstract syntax tree (AST) from the tokens, with support for parsing while statements.
- **Evaluator**: Executes the AST, including logic for while loops that repeatedly evaluate the body statement as long as the condition is true.
- **Context Management**: Handles variable storage and scope management during execution.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd compiler-project
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the compiler with an example code:
   ```
   python src/main.py src/examples/sample-code.txt
   ```

## Example Usage

The `sample-code.txt` file contains examples demonstrating the usage of while loops and other language features. You can modify this file to test different constructs and see how the compiler evaluates them.

## Running Tests

To ensure the compiler works as expected, run the unit tests:
```
pytest tests/
```

This will execute all tests in the `tests` directory, verifying the functionality of the lexer, parser, evaluator, and example code.