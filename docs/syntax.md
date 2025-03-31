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
var x : integer = 10;
display x;
```

## Statements

A statement can be one of the following:

```prog
Statement := VariableDeclaration | FunctionDefinition | FunctionCall | IfStatement | LoopStatement | DisplayStatement | Expression
```

**Example:**

```prog
var y : integer = 20;
display y + 5;
```

## Variable Declarations

Variables are declared using the `var` keyword:

```prog
VariableDeclaration := "var" Identifier ":" Type "=" Expression ";"
Type := "integer" | "decimal" | "uinteger"
```

**Example:**

```prog
var z : decimal = 3.14;
var count : uinteger = 100;
display z * count;
```

## Arrays

Arrays are declared and manipulated using square brackets:

```prog
ArrayDeclaration := "var" Identifier ":" "array" "=" "[" Elements "]"
Elements := Expression | Expression "," Elements
ArrayOperations := Identifier "[" Index "]" | Identifier "." ArrayMethod "(" Arguments ")"
ArrayMethod := "PushFront" | "PushBack" | "PopFront" | "PopBack" | "Length" | "Clear" | "Insert" | "Remove"
```

**Example:**

```prog
var arr : array = [1, 2, 3];
arr.PushBack(4);
display arr[2];
arr.Remove(1);
display arr.Length;
```

## Hashes

Hashes (dictionaries) are declared and manipulated using curly braces:

```prog
HashDeclaration := "var" Identifier ":" "hash" "=" "{" KeyValuePairs "}"
KeyValuePairs := Key ":" Value | Key ":" Value "," KeyValuePairs
HashOperations := Identifier "[" Key "]" | Identifier "." HashMethod "(" Arguments ")"
HashMethod := "Add" | "Remove"
```

**Example:**

```prog
var hash : hash = {"key1": 10, "key2": 20};
hash.Add("key3", 30);
display hash["key1"];
hash.Remove("key2");
```

## Loops

Loops are supported with `while` and `for` constructs:

```prog
WhileLoop := "while" "(" Condition ")" Block
ForLoop := "for" "(" Initialization ";" Condition ";" Increment ")" Block
```

**Example:**

```prog
var i : integer = 0;
while (i < 5) {
    display i;
    i = i + 1;
}

for (var j : integer = 0; j < 5; j = j + 1) {
    display j;
}
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

## Functions

Functions are declared with `fn` or `fnrec`:

```prog
FunctionDefinition := ("fn" | "fnrec") Identifier "(" Parameters ")" Block
Parameters := Identifier | Identifier "," Parameters
Block := "{" Statements "}"
```

**Example:**

```prog
fn add(a, b) {
    return a + b;
}
display add(5, 10);
```

## Sample Program

Here is a sample program demonstrating all the features:

```prog
var x : integer = 10;
var arr : array = [1, 2, 3];
var hash : hash = {"key1": 10, "key2": 20};

arr.PushBack(4);
hash.Add("key3", 30);

fn multiply(a, b) {
    return a * b;
}

if x > 5 then {
    display "x is greater than 5";
} else {
    display "x is 5 or less";
} end;

while (x > 0) {
    display x;
    x = x - 1;
}

for (var i : integer = 0; i < arr.Length; i = i + 1) {
    display arr[i];
}

display multiply(hash["key1"], 2);
```
