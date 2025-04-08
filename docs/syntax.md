# Syntax Rules and Examples

This document details the syntax rules of the Prog language, along with illustrative examples.

## Program Structure

A program is composed of a sequence of statements:

```prog
Program := Statements
Statements := Statement | Statement Statements
```

**Example:**

```prog
var integer x = 10;
display x;
```

## Statements

A statement can be one of the following:

```prog
Statement := VariableDeclaration | FunctionDefinition | FunctionCall | IfStatement | LoopStatement | DisplayStatement | Expression
```

**Example:**

```prog
var integer= 20;
display y + 5;
```

## Variable Declarations

Variables are declared using the `var` keyword followed by the type and the variable name. The type must be explicitly specified (`integer`, `decimal`, `uinteger`, `array`, or `hash`) to typecast the variable. If no type is specified, the type is inferred from the assigned value.

```prog
VariableDeclaration := "var" Type Identifier "=" Expression ";"
Type := "integer" | "decimal" | "uinteger" | "array" | "hash"
```

### Rules:

- Specifying a type will typecast the variable to the given type.
- If the type is omitted, it is inferred from the value.
- For `array` and `hash`, if the value cannot be translated into the specified type, an error is thrown.

**Examples:**

```prog
/> Basic declarations
var integer x = 10; /> Explicit type declaration
var decimal y = 3.14; /> Explicit type declaration
var uinteger count = 100;

/> Array declarations
var array arr = [1, 2, 3];
var mixedArr = [2.5, "hi"]; /> Type inferred

/> Hash declarations
var Hash hashy = {"key1": 10, "key2": 20};
var inferredHash = {"a": 1, "b": 2}; /> Type inferred

/> Invalid declarations
var array invalidArr = {"a": 1}; /> Error: Cannot typecast to array
var Hash invalidHash = [1, 2, 3]; /> Error: Cannot typecast to hash
```





## Comments

Nexus supports two types of comments:

1. **Single-line comments**: Begin with `/>` and continue until the end of the line.
   **Example:**
   ```prog
   var a = 42;   /> This is a single-line comment
   display a;    /> Outputs 42
   ```

2. **Multi-line or expression-embedded comments**: Enclosed within `/~ ... ~/`.
   **Examples:**
   - Multi-line comments:

     ```prog
     /~
     This is a multi-line comment.
     It spans multiple lines.
     ~/
     display "Hello, World!";
     ```

   - Expression-embedded comments:

     ```prog
     var total = price * /~ discount * ~/ quantity;
     ```

## Operators

Nexus supports a variety of operators:

1. **Arithmetic Operators**: `+`, `-`, `*`, `/`, `÷`, `%`, `**`
   - `÷` has higher precedence than `/`.
   - Exponentiation (`**`) follows right-associativity.

2. **Comparison Operators**: `==`, `!=`, `>`, `<`, `<=`, `>=`

3. **Logical Operators**: `and`, `or`, `not`

4. **Bitwise Operators**: `&`, `|`, `^`, `>>`, `<<`, `~`

5. **Assignment Operators**: `=`, `+=`, `-=`, `*=`, `/=`, `%=`

**Examples:**

```prog
var a = 5 + 3 * 2; /> a = 11
var b = (5 > 3) + 99; /> b = 100
```

## Arrays

Arrays are declared and manipulated using square brackets. They support various operations such as adding, removing, and accessing elements.

```prog
ArrayDeclaration := "var" "array" Identifier "=" "[" Elements "]"
Elements := Expression | Expression "," Elements
ArrayOperations := Identifier "[" Index "]" | Identifier "." ArrayMethod "(" Arguments ")"
ArrayMethod := "PushFront" | "PushBack" | "PopFront" | "PopBack" | "Length" | "Clear" | "Insert" | "Remove"
```

### Rules:

- Arrays can contain elements of mixed types.
- Operations like `PushFront`, `PushBack`, `Insert`, and `Remove` modify the array.
- Accessing an invalid index will throw an error.

**Examples:**

```prog
var array arr = [1, 2, 3];
arr.PushBack(4); /> Adds 4 to the end
display arr[2]; /> Displays 3
arr.Remove(1); /> Removes the element at index 1
display arr.Length; /> Displays the length of the array
```

## Hashes

Hashes (dictionaries) are declared and manipulated using curly braces. They allow key-value pairs and support operations like adding and removing keys.

```prog
HashDeclaration := "var" "hash" Identifier "=" "{" KeyValuePairs "}"
KeyValuePairs := Key ":" Value | Key ":" Value "," KeyValuePairs
HashOperations := Identifier "[" Key "]" | Identifier "." HashMethod "(" Arguments ")"
HashMethod := "Add" | "Remove"
```

### Rules:

- Keys must be unique.
- Accessing a non-existent key will throw an error.
- Operations like `Add` and `Remove` modify the hash.

**Examples:**

```prog
var hash h = {"key1": 10, "key2": 20};
h.Add("key3", 30); /> Adds a new key-value pair
display h["key1"]; /> Displays 10
h.Remove("key2"); /> Removes the key "key2"
```

## Conditional Statements

Conditional statements use `if`, `then`, `else`, and `end`:

```prog
IfStatement := "if" Condition "then" Block ["else" Block] "end"
```

**Example:**

```prog
if x > 10 then {
    display "x is greater than 10";
} else {
    display "x is 10 or less";
} end;
```

## Loops

Loops are supported with `while` and `for` constructs:

```prog
WhileLoop := "while" "(" Condition ")" Block
ForLoop := "for" "(" Initialization ";" Condition ";" Increment ")" Block
```

**Example:**

```prog
var integer i = 0;
while (i < 5) {
    display i;
    i = i + 1;
}

for (var integer j = 0; j < 5; j = j + 1) {
    display j;
}
```

## Display Statements

The `display` and `displayl` keywords are used for printing output.

```prog
DisplayStatement := "display" Expression ";" | "displayl" Expression ";"
```

### Rules:

- `display` prints the expression without a newline.
- `displayl` prints the expression followed by a newline.

**Examples:**

```prog
display "Hello, ";
displayl "World!";
```

## Functions

Functions are declared with `fn` or `fnrec`:

```prog
FunctionDefinition := ("fn" | "fnrec") Identifier "(" Parameters ")" Block
Parameters := Identifier | Identifier "," Parameters
Block := "{" Statements "}"
```

### Rules:

- `fn` is used for non-recursive functions.
- `fnrec` is used for recursive functions.
- Functions are first-class citizens and can be passed as arguments, returned, or assigned to variables.

**Examples:**

```prog
fn add(a, b) {
    return a + b;
}
display add(5, 10);

fnrec fib(n) {
    if n == 1 or n == 2 then 1 else fib(n - 1) + fib(n - 2) end;
}
display fib(10); /> Outputs 55
```

## Feed Function

The `feed` function is used to take input from the user. It always requires parentheses.

```prog
FeedFunction := "feed" "(" [StringLiteral] ")"
```

- If a string literal is provided, it is displayed as a prompt to the user.
- If no string literal is provided, a default prompt (`FEED`) is displayed.

**Examples:**

```prog
var integer a = feed("Give input:");
var integer b = feed();
```

## Sample Program

Here is a sample program demonstrating all the features:

```prog
var integer x = 10;
var array arr = [1, 2, 3];
var hash hash = {"key1": 10, "key2": 20};

arr.PushBack(4);
hash.Add("key3", 30);

fn multiply(a, b) {
    a * b;
}

if x > 5 then {
    displayl "x is greater than 5";
} else {
    displayl "x is 5 or less";
} end;

while (x > 0) {
    displayl x;
    x = x - 1;
}
displayl ("Array run:");
for (var integer i = 0; i < arr.Length; i = i + 1) {
    displayl arr[i];
}

display multiply(hash["key1"], 2);
```
