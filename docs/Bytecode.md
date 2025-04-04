
# Bytecode Generation in Nexus

The bytecode generation component is responsible for translating the Abstract Syntax Tree (AST) produced by the parser into a sequence of bytecode instructions that can be executed by a virtual machine or interpreter.

## Overview

Bytecode is a low-level representation of the program that is easier to execute than the original source code. The bytecode generation process involves traversing the AST and generating corresponding bytecode instructions for each node in the tree.

## Bytecode Instructions

The following table documents the bytecode instructions defined in the `bytecode_gen.py` file. Each instruction operates on a stack-based virtual machine.

| **Instruction** | **Opcode** | **Stack Behavior** | **Description**                                                                                                           |
| --------------------- | ---------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| **HALT**        | `0`            | -                        | Terminates the execution of the bytecode.                                                                                       |
| **NOP**         | `1`            | -                        | No operation; a placeholder for future instructions.                                                                            |
| **PUSH**        | `2`            | `[] -> [value]`        | Pushes a value onto the stack.                                                                                                  |
| **POP**         | `3`            | `[value] -> []`        | Pops a value off the stack.                                                                                                     |
| **ADD**         | `4`            | `[a, b] -> [a + b]`    | Pops the top two values, adds them, and pushes the result.                                                                      |
| **SUB**         | `5`            | `[a, b] -> [a - b]`    | Pops the top two values, subtracts the second from the first, and pushes the result.                                            |
| **MUL**         | `6`            | `[a, b] -> [a * b]`    | Pops the top two values, multiplies them, and pushes the result.                                                                |
| **NEG**         | `7`            | `[a] -> [-a]`          | Negates the top value on the stack.                                                                                             |
| **DIV**         | `8`            | `[a, b] -> [a / b]`    | Pops the top two values, divides the first by the second, and pushes the result.                                                |
| **MOD**         | `9`            | `[a, b] -> [a % b]`    | Pops the top two values, computes the modulus, and pushes the result.                                                           |
| **POW**         | `10`           | `[a, b] -> [a ** b]`   | Pops the top two values, raises the first to the power of the second, and pushes the result.                                    |
| **LT**          | `11`           | `[a, b] -> [a < b]`    | Pops the top two values, checks if the first is less than the second, and pushes `1` if true, `0` otherwise.                |
| **GT**          | `12`           | `[a, b] -> [a > b]`    | Pops the top two values, checks if the first is greater than the second, and pushes `1` if true, `0` otherwise.             |
| **EQ**          | `13`           | `[a, b] -> [a == b]`   | Pops the top two values, checks equality, and pushes `1` if true, `0` otherwise.                                            |
| **NEQ**         | `14`           | `[a, b] -> [a != b]`   | Pops the top two values, checks inequality, and pushes `1` if true, `0` otherwise.                                          |
| **LE**          | `15`           | `[a, b] -> [a <= b]`   | Pops the top two values, checks if the first is less than or equal to the second, and pushes `1` if true, `0` otherwise.    |
| **GE**          | `16`           | `[a, b] -> [a >= b]`   | Pops the top two values, checks if the first is greater than or equal to the second, and pushes `1` if true, `0` otherwise. |
| **AND**         | `17`           | `[a, b] -> [a and b]`  | Pops the top two values, performs logical AND, and pushes the result.                                                           |
| **OR**          | `18`           | `[a, b] -> [a or b]`   | Pops the top two values, performs logical OR, and pushes the result.                                                            |
| **BAND**        | `19`           | `[a, b] -> [a & b]`    | Pops the top two values, performs bitwise AND, and pushes the result.                                                           |
| **BOR**         | `20`           | `[a, b] -> [a \| b]`    | Pops the top two values, performs bitwise OR, and pushes the result.                                                            |
| **BXOR**        | `21`           | `[a, b] -> [a ^ b]`    | Pops the top two values, performs bitwise XOR, and pushes the result.                                                           |
| **SHL**         | `22`           | `[a, b] -> [a << b]`   | Pops the top two values, performs bitwise left shift, and pushes the result.                                                    |
| **SHR**         | `23`           | `[a, b] -> [a >> b]`   | Pops the top two values, performs bitwise right shift, and pushes the result.                                                   |
| **NOT**         | `24`           | `[a] -> [not a]`       | Pops the top value, performs logical NOT, and pushes the result.                                                                |
| **BNOT**        | `25`           | `[a] -> [~a]`          | Pops the top value, performs bitwise NOT, and pushes the result.                                                                |
| **ASCII**       | `26`           | `[a] -> [ord(a)]`      | Pops the top value, converts it to its ASCII code, and pushes the result.                                                       |
| **CHAR**        | `27`           | `[a] -> [chr(a)]`      | Pops the top value, converts it to a character, and pushes the result.                                                          |
| **VARBIND**     | `28`           | `[value] -> []`        | Binds a value to a variable in the current scope.                                                                               |
| **DISPLAY**     | `29`           | `[value] -> []`        | Displays the top value on the stack.                                                                                            |
| **DISPLAYL**    | `30`           | `[value] -> []`        | Displays the top value on the stack with a newline.                                                                             |
| **JUMP**        | `31`           | `[] -> []`             | Unconditionally jumps to a specified address.                                                                                   |
| **BEQ**         | `32`           | `[a, b] -> []`         | Pops two values, jumps to a specified address if they are equal.                                                                |
| **BNE**         | `33`           | `[a, b] -> []`         | Pops two values, jumps to a specified address if they are not equal.                                                            |
| **CALL**        | `34`           | `[] -> []`             | Calls a function at a specified address.                                                                                        |
| **RET**         | `35`           | `[] -> []`             | Returns from a function.                                                                                                        |

## The `do_codegen` Function

The core function responsible for generating bytecode is `do_codegen`. This function takes an AST node and a list (or bytearray) to which it appends the generated bytecode instructions. The function uses pattern matching to determine the type of AST node and generates the appropriate bytecode.

```python
def do_codegen(t, code):
```

- `t`: The AST node to be processed.
- `code`: A list or bytearray that accumulates the generated bytecode instructions.
- **Number Nodes**: For `Number` nodes, the function appends the `PUSH` instruction followed by the numeric value.
- **Binary Operations**: For binary operations (e.g., addition, subtraction, multiplication), the function recursively calls `do_codegen` on the left and right operands, then appends the corresponding operation instruction (e.g., `ADD`, `SUB`, `MUL`).
- **Unary Operations**: Currently, unary operations are not explicitly handled in the provided code, but can be added similarly.

## The `codegen` Function

The `codegen` function is responsible for initiating the bytecode generation process for an entire program represented as an AST.

```python
def codegen(ast):
```

- `ast`: The root node of the Abstract Syntax Tree.

## Example Usage

To generate bytecode for a simple program, you would typically follow these steps:

1. Parse the source code to produce an AST.
2. Call the `codegen` function with the AST to generate the bytecode.
3. Execute the generated bytecode using a virtual machine or interpreter.

### Sample Code

```python
/~ define a prog and generate AST ~/
bytecode = codegen(ast)
```
