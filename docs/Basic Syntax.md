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
