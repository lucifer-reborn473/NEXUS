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
- Blocks of code can be enclosed in braces (`{...}`)

### Datatypes
- Numbers
- Strings (must be enclosed in double quotes)
- Booleans (`True` and `False`)

### Comments
- Full-line comments using `/>` (everything written after `/>` in the same line is ignored)
    Example:
    ```
    var a = 40+2;   /> a holds 42
    displayl a;     /> 42
    ```
-  Multi-line or in-expression comments using `/~ ... ~/`  
    Example:
    ```
    var price = 100;    /> INR per KG
    var quantity = 3;   /> KGs
    var discount = 0.3;
    var total = price * /~ discount * ~/ quantity; /> INR
    ```
    ```
    /~
    The below program
    outputs team name
    ~/
    displayl "Team Nexus";
    ```

### Variables
- Declared using the `var` keyword. Redeclaration is not allowed in the same scope and is caught at compile-time.
- Initialization defaults to `None`
- Optional datatype declarations (interger, uinteger, decimal)


### Strings
- Must be enclosed in double quotes
- String operations:
    - Concatenation using `+`
    - `char()` and `ascii()` functions
        - Description:
        ...
        - Examples:
            If `x` is a lower-case Latin letter, then `char("A" + x - "a")` evaluates to `x`'s upper-case version.


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
    - acts as control-flow constructs

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
    - `if ... then ... else end;`
    - `if ... then ... end;`
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

### Functions
- Functions in Nexus are declared using the `fn` keyword if the function is non-recursive (does not calls itself), else using `fnrec`
- Redeclaration is not allowed in the same scope and is caught at compile-time.
- Calling a function with empty body returns `None`
- Examples:
    - The below example declares and calls a function `giveSum()` which takes two parameters `a` and `b` and returns their sum
        ```
        fn giveSum(a, b){
            a+b;
        }
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
        }
        displayl fib(10); /> outputs 55
        ```
        Note: fib(31) takes nearly ___ seconds, while fib(32) takes nearly __ seconds (averaged over 5 iterations)

    

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
- Nexus is based on lexical (or, static) scoping, i.e, a function's scope is based on where it's defined and not where it's called
- Scoping in conditionals, loops and functions


# Bytecode


# Error handling

To add:
- Common error types
- How to catch and handle errors
- Best practices for error handling
- Troubleshooting: common issues users might encounter and their solutions