# Getting Started

Nexus is a powerful high-level, dynamically-typed, lexically-scoped, expression-oriented, imperative programming language.

### Installation

Follow these steps to install Nexus:

1. Download the latest release from [GitHub Releases](https://github.com/lucifer-reborn473/Our_Compiler).
2. Run the installer for your operating system.
3. Verify the installation by running `nexus --version`.

### Hello, World!
The below steps describes how to write a simple progam in Nexus that outputs "Hello, World!" onto the screen.
1. Open a directory in your favorite code editor.
2. Create a file `helloworld.nex`
3. Enter the below code:
    ```
    displayl "Hello, World!";
    ```
4. Save the file.
5. Open terminal and write `nexus helloworld.nex` and press enter!  

Woohoo! You just wrote your first "Hello, World!" program in Nexus.

# Enter Nexus!
- Every statement must end with a semicolon
- Every statement is an expression (returns a value)
- Printing outputs
    - The `display` keyword prints the expression following it. It returns `None`.
    - The `displayl` keyword prints the expression following it with the newline character. It returns `None`.
    - Each of the below statements prints the newline character:
        ```
        displayl ""; 
        display "\n";
        ```
- Taking inputs
    - `feed` keyword, followed by an optional expression to print, takes in input in string format and returns it.

- Valid identifier: Made of English letters only

### Datatypes
#### Primitives:
- Numbers
- Strings (must be enclosed in double quotes)
- Booleans (`True` and `False`)
- `None`  
#### Compound Datatypes:
- Array
- Hash
- Schema

### Comments
- Single-line comments begin with /> and continue until the end of the line
    Example:
    ```
    var a = 40+2;   /> a holds 42
    displayl a;     /> 42
    ```
-  Multi-line or expression-embedded comments using `/~ ... ~/`  
    Examples:
    - Expression-embedded comments:
        ```
        var price = 100;    /> INR per KG
        var quantity = 3;   /> KGs
        var discount = 0.3;
        var total = price * /~ discount * ~/ quantity; /> INR
        ```
    - Multiline comments:
        ```
        /~
        The below program
        outputs team name
        ~/
        displayl "Team Nexus";
        ```

### Variables
- Declared using the `var` keyword. Redeclaration is not allowed in the same scope and is caught before evaluation.
- Initialization defaults to `None`

### Strings
- Can be enclosed in either single or double quotes
- String operations:
    - Concatenation using `+`
    - `char()` and `ascii()` functions (respectively equivalen to `chr()` and `ord()` in Python)


### Operators
Basic operators include:
- Arithmetic
    - operators include `+`, `-`, `*`, `%`, `/`, `÷` and `**` 
    - follows left-associativity (except the exponentiation `^` operator which follows right-associativity)
    - Note: `÷` has a higher precedence compared to `/`

- Assignment
    - Values assigned to variables using the assignment (`=`) operator
        - A statement like `var a = ;` raises a syntax error
    - Compound Assignment operators include `+=`, `-=`, `*=`, `/=`, `%=`

- Comparison
    - operators include `==`, `!=`, `>`, `<`, `<=`, `>=`

- Logical
    - operators include `and`, `or` and `not`

- Bitwise
    - operators include `&`, `|`, `^`, `>>`, `<<`, `~`

- Precedence

- Examples:
    - `5>3` evaluates to True but as 1 when used in an expression as:
        ```
        var a = (5>3) + 99;
        displayl a;
        ```
        Output:
        ```
        100
        ```

More operators discussed in their respective sections

### Conditionals
- Valid syntaxes:
    - `if ... then ... else ... end;`
    - `if ... then ... end;` (if condition is false, then evaluates to `None`)
- Nesting supported
- Empty `then` and/or `else` expressions returns `None`
- Examples:
    - Using braces (`{...}`)
        ```
        var a = if 2==2 then {
            displayl "inside then";
            42;
        } else {
            displayl "inside else";
            7;
        } end;
        displayl a;
        ```  
        Output:
        ```
        inside then
        42
        ```

    - Conditionally evaluating expressions
        ```
        var b = if 2!=2 then a else 5; /> a is not declared in this scope but the code runs without error!
        displayl b;
        ```  
        Output:
        ```
        5
        ```

    - Nesting:
        ```
        var a = if 4<3 then if 3==2 then 5 else 100 end else 1000 end;
        displayl a;
        ```
        Output:
        ```
        1000
        ```

### Loops
- `for` and `while` loops supported with similar syntax as in C/C++.
- Example:
    ```
    for(var i=0; i<10; i+=1){
        displayl i;
    }
    ```
- `moveon` statement equaivalent to `continue` statement in Python.
- `breakout` statement equaivalent to `break` statement in Python.
- Example
    ```
    while (i < 5) {
        i += 1;
        if i == 2 then moveon end;
        if i == 4 then breakon end;
        display i;
    }
    ```
    Output
    ```
    1
    3
    ```


### Functions
- There are two types of keyword for declaring functions in Nexus:
    - `fn` for non-recursive functions (does not calls itself)
    - `fnrec` for recursive functions
- Redeclaration is not allowed in the same scope and is caught before evaluation.
- Calling a function with empty body returns `None`
- Examples:
    - The below example declares and calls a function `giveSum()` which takes two parameters `a` and `b` and returns their sum
        ```
        fn giveSum(a, b){
            a+b;
        };
        displayl giveSum(40, 2);
        ```
        Output:
        ```
        42
        ```
    - Function to calculate the nth Fibonacci number:
        ```
        fn fib(n){
            if n==1 or n==2 then 1 else fib(n-1) + fib(n-2) end;
        };
        displayl fib(10); /> outputs 55
        ```
        Note: fib(31) takes nearly 22.8 seconds, while fib(32) takes nearly 35.4 seconds (averaged over 3 iterations)

#### Functions are first-class citizens in Nexus
- Example 1:
    ```
    var x = 100;
    fn bar(){
        x;
    }
    fn foo(g){ 
        g() + 2; /> takes function as parameter
    }
    displayl foo(bar);
    ```
    Output
    ```
    102
    ```

- Example 2:
    ```
    fn foo(){
        fn bar(){
            x+2;
        }
        bar; /> returns a function
    }
    var x = 40;
    var y = foo(); /> assigns to a variable
    displayl y();
    ```
    Output
    ```
    42
    ```


### Arrays
- Declared using the `array` keyword
- Initialised with elements enclosed in square-brackets
- Elements can be of any type
- Element access through indexing (index enclosed in square-brackets)
- Mutability?
- Different methods are supported for arrays which are accessed using the `.` opeator.
    - Supported methods:

    - Examples:

### Hash Tables
Hey BG, please add:
- Declaration syntax
- Access methods
- Common operations (adding/removing keys, checking existence)
- Iteration techniques

# Scoping
- Nexus is based on lexical (or, static) scoping.

- structural hierarchy of scopes made during parsing
    - lexical structure captured while parsing
    - helps identify and catch duplicate declarations for variables and functions
- resolution of values during the evaluation phase (see Example 6 below)

- Conditionals and loops have their own local scopes

- Example 1:
    ```
    fn foo(i){
        if i==1 then var a = 2 else 5 end;
        a = 42;
    };
    displayl foo(1);
    ```
- Example 2:
    ```
    var x = 9;
    fn bar() {
        x;
    };
    fn foo() {
        var x = 100;
        bar();
    };
    displayl foo();
    ```
    Output
    ```
    9
    ```


- Exampl 3:
    ```
    var x = 2;
    fn foo(){
        var x = 300;
        x;
    };
    fn bar(x){
        x += 1000;
        x;
    };
    fn baz(x){
        if x<5 then foo() else bar(x) end;
    };
    displayl baz(4);
    displayl baz(6);
    ```
    Output:
    ```
    300
    1006
    ```

- Example 4:
    ```
    var x = 1000;
    fn foo() {
        fn bar() {
            x;
        }
        var x = 117;
        bar();
    }
    displayl foo();
    ```
    Output
    ```
    117
    ```

- Example 5:
    ```
    var a = "g-";
    fn foo(x, i){
        if i==1 then var a = "1-" else "dummy" end;
        if x==1 then "k" else a + foo(x-1, i+1) end;
    };
    displayl foo(5,1);
    ```
    Output:
    ```
    g-g-g-g-k
    ```

- Example 6:
    ```
    fn foo(i){
        fn bar(){
            i;
        };
        fn baz(){
            bar();
        };
        if i==10 then baz() else foo(i+1) end;
    };
    displayl foo(0);
    ```
    Output:
    ```
    10
    ```


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



## Tasks ahead
- String slicing and operations
- Complete error handling (with line number)
- Bytecode handling for conditions and functions
- Plots and large data handling features
- Support threading
- Types resolves
