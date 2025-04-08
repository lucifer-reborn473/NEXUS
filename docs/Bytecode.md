# Bytecode Generation in Nexus

The bytecode generation component is responsible for translating the Abstract Syntax Tree (AST) produced by the parser into a sequence of bytecode instructions that can be executed by a virtual machine or interpreter.

## Overview

Bytecode is a low-level representation of the program that is easier to execute than the original source code. The bytecode generation process involves traversing the AST and generating corresponding bytecode instructions for each node in the tree.

## Bytecode Instructions

The following table documents the bytecode instructions defined in the `bytecode_gen.py` file. Each instruction operates on a stack-based virtual machine.
| **Instruction**       | **Opcode** | **Stack Behavior**                | **Description**                                                                |
|-----------------------|------------|-----------------------------------|--------------------------------------------------------------------------------|
| **HALT**              | `0`        | `-`                               | Terminates program execution                                                   |
| **NOP**               | `1`        | `-`                               | No operation; placeholder instruction                                          |
| **PUSH**              | `2`        | `[] → [value]`                    | Pushes a value onto the stack                                                  |
| **POP**               | `3`        | `[value] → []`                    | Removes the top value from the stack                                           |
| **ADD**               | `4`        | `[a, b] → [a+b]`                  | Adds two values and pushes result                                              |
| **SUB**               | `5`        | `[a, b] → [a-b]`                  | Subtracts second value from first                                              |
| **MUL**               | `6`        | `[a, b] → [a*b]`                  | Multiplies two values                                                          |
| **NEG**               | `7`        | `[a] → [-a]`                      | Negates a value                                                                |
| **DIV**               | `8`        | `[a, b] → [a/b]`                  | Divides first value by second                                                  |
| **MOD**               | `9`        | `[a, b] → [a%b]`                  | Computes remainder of division                                                 |
| **POW**               | `10`       | `[a, b] → [a^b]`                  | Raises first value to power of second                                          |
| **LT**                | `11`       | `[a, b] → [a<b]`                  | Tests if first value is less than second                                       |
| **GT**                | `12`       | `[a, b] → [a>b]`                  | Tests if first value is greater than second                                    |
| **EQ**                | `13`       | `[a, b] → [a==b]`                 | Tests if values are equal                                                      |
| **NEQ**               | `14`       | `[a, b] → [a!=b]`                 | Tests if values are not equal                                                  |
| **LE**                | `15`       | `[a, b] → [a<=b]`                 | Tests if first value is less than or equal to second                           |
| **GE**                | `16`       | `[a, b] → [a>=b]`                 | Tests if first value is greater than or equal to second                        |
| **AND**               | `17`       | `[a, b] → [a&&b]`                 | Logical AND operation                                                          |
| **OR**                | `18`       | `[a, b] → [a||b]`                 | Logical OR operation                                                           |
| **BAND**              | `19`       | `[a, b] → [a&b]`                  | Bitwise AND operation                                                          |
| **BOR**               | `20`       | `[a, b] → [a|b]`                  | Bitwise OR operation                                                           |
| **BXOR**              | `21`       | `[a, b] → [a^b]`                  | Bitwise XOR operation                                                          |
| **SHL**               | `22`       | `[a, b] → [a<<b]`                 | Bitwise left shift                                                             |
| **SHR**               | `23`       | `[a, b] → [a>>b]`                 | Bitwise right shift                                                            |
| **NOT**               | `24`       | `[a] → [!a]`                      | Logical NOT operation                                                          |
| **BNOT**              | `25`       | `[a] → [~a]`                      | Bitwise NOT operation                                                          |
| **ASCII**             | `26`       | `[a] → [ord(a)]`                  | Converts character to ASCII code                                               |
| **CHAR**              | `27`       | `[a] → [chr(a)]`                  | Converts ASCII code to character                                               |
| **VARBIND**           | `28`       | `[value] → []`                    | Binds value to variable                                                        |
| **DISPLAY**           | `29`       | `[value] → []`                    | Displays value without newline                                                 |
| **DISPLAYL**          | `30`       | `[value] → []`                    | Displays value with newline                                                    |
| **ASSIGN**            | `31`       | `[value] → []`                    | Assigns value to existing variable                                             |
| **CALLARRAY**         | `32`       | `[arr, idx] → [val]`              | Gets value at array index                                                      |
| **PUSHFRONT**         | `33`       | `[arr, val] → []`                 | Adds element to start of array                                                 |
| **PUSHBACK**          | `34`       | `[arr, val] → []`                 | Adds element to end of array                                                   |
| **POPFRONT**          | `35`       | `[arr] → [val]`                   | Removes and returns first element from array                                   |
| **POPBACK**           | `36`       | `[arr] → [val]`                   | Removes and returns last element from array                                    |
| **ASSIGNTOARRAY**     | `37`       | `[arr, idx, val] → []`            | Sets value at array index                                                      |
| **CALLHASHVAL**       | `38`       | `[hash, key] → [val]`             | Gets value for key in hash map                                                 |
| **ADDHASHPAIR**       | `39`       | `[hash, key, val] → []`           | Adds key-value pair to hash map                                                |
| **REMOVEHASHPAIR**    | `40`       | `[hash, key] → []`                | Removes key from hash map                                                      |
| **ASSIGNHASHVAL**     | `41`       | `[hash, key, val] → []`           | Updates value for key in hash map                                              |
| **ASSIGNFULLARRAY**   | `42`       | `[arr, vals] → []`                | Assigns multiple values to array                                               |
| **INSERTAT**          | `43`       | `[arr, idx, val] → []`            | Inserts value at array index                                                   |
| **REMOVEAT**          | `44`       | `[arr, idx] → [val]`              | Removes and returns value at array index                                       |
| **GETLENGTH**         | `45`       | `[container] → [length]`          | Gets length of container (array/hash)                                          |
| **CLEARARRAY**        | `46`       | `[arr] → []`                      | Empties an array                                                               |
| **JUMP**              | `47`       | `[] → []`                         | Unconditional jump                                                             |
| **JUMP_IF_TRUE**      | `48`       | `[cond] → []`                     | Jumps if condition is true                                                     |
| **JUMP_IF_FALSE**     | `49`       | `[cond] → []`                     | Jumps if condition is false                                                    |
| **LABEL**             | `50`       | `[] → []`                         | Defines a jump target (placeholder)                                            |
| **FEED**              | `51`       | `[prompt] → [input]`              | Reads user input                                                               |
| **FUNC_DEF**          | `52`       | `[] → []`                         | Defines a function                                                             |
| **FUNC_CALL**         | `53`       | `[args] → [result]`               | Calls a function                                                               |
| **RETURN**            | `54`       | `[result] → [result]`             | Returns from function                                                          |
| **BREAK**             | `55`       | `[] → []`                         | Breaks out of a loop                                                           |
| **MOVEON**            | `56`       | `[] → []`                         | Continues to next iteration of loop                                            |
| **COMPOUND_ASSIGN**   | `57`       | `[var, val] → []`                 | Combines operation with assignment (+=, -=, etc.)                              |


## The `codegen` Function

The `codegen` function is responsible for initiating the bytecode generation process for an entire program represented as an AST.

```python
def codegen(ast):
```

- `ast`: The root node of the Abstract Syntax Tree.

## Example Bytecode Generation

This section provides an example of how bytecode is generated for a simple program.

### Example Code

```text
var x = 10;

if x > 5 then {
    displayl "x is greater than 5";
} else {
    displayl "x is 5 or less";
} end;

while (x > 0) {
    displayl x;
    x = x - 1;
}
```

### Bytecode Breakdown

#### Variable Declaration: `var x = 10;`

```text
[<OpCode.PUSH: 2>, 1, 10]             # Push integer 10 onto stack
[<OpCode.VARBIND: 28>, 1, 120]        # Bind value to variable 'x' (ASCII 120)
```

#### If Statement: `if x > 5 then ...`

```text
[<OpCode.PUSH: 2>, 1, 120]            # Push variable name 'x'
[<OpCode.PUSH: 2>, 1, 5]              # Push integer 5
[<OpCode.GT: 12>]                     # Compare: x > 5
[<OpCode.JUMP_IF_FALSE: 49>, 25]      # If false, jump 25 instructions ahead (to else branch)

# Then branch: displayl "x is greater than 5";
[<OpCode.PUSH: 2>, 19]                # Push string "x is greater than 5"
[<OpCode.DISPLAYL: 30>]               # Display with newline
[<OpCode.JUMP: 47>, 18]               # Jump past else branch (unconditional)

# Else branch: displayl "x is 5 or less";
[<OpCode.PUSH: 2>, 14]                # Push string "x is 5 or less"
[<OpCode.DISPLAYL: 30>]               # Display with newline
```

#### While Loop: `while (x > 0) { ... }`

```text
[<OpCode.PUSH: 2>, 1, 120]            # Push variable name 'x'
[<OpCode.PUSH: 2>, 1, 0]              # Push integer 0
[<OpCode.GT: 12>]                     # Compare: x > 0
[<OpCode.JUMP_IF_FALSE: 49>, 17]      # If false, jump 17 instructions ahead (exit loop)

# Loop body
[<OpCode.PUSH: 2>, 1, 120]            # Push variable name 'x'
[<OpCode.DISPLAYL: 30>]               # Display with newline
[<OpCode.PUSH: 2>, 1, 120]            # Push variable name 'x'
[<OpCode.PUSH: 2>, 1, 255]            # Push integer -1 (two's complement)
[<OpCode.ADD: 4>]                     # Add x + (-1) = x - 1
[<OpCode.ASSIGN: 31>, 1, 120]         # Assign result back to 'x'
[<OpCode.JUMP: 47>, -24]              # Jump back 24 instructions (to loop condition)

[<OpCode.HALT: 0>]                    # Terminate program
```

### Basic Bytecode Generation Function

```python
def codegen(ast, scope, not_list=False):
    """Generate bytecode for an AST"""
    generator = BytecodeGenerator()
    bytecode = generator.generate(ast, scope)
    
    if not_list:
        return bytecode
    else:
        return bytearray(bytecode)
```

The `codegen` function creates a `BytecodeGenerator` instance, calls its `generate` method with the AST and scope, and returns either a list or bytearray of bytecode instructions depending on the `not_list` parameter.

The `BytecodeGenerator` class recursively traverses the AST, handling each node type with specialized methods that emit the appropriate bytecode instructions. Control flow is managed through labels and jump instructions, with placeholder jumps that are resolved in a final pass.
