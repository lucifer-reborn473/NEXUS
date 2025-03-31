# Recursive Functions in Nexus

This document covers how recursive functions and static scoping work in Nexus.

## Recursive Functions

Prog supports recursive functions, allowing a function to call itself either directly or indirectly.

### Direct Recursion

A function calls itself until a base case is met.

```prog
fn factorial(n) {
    if n == 1 then {
        return 1;
    } else {
        return n * factorial(n - 1);
    } end;
}
display factorial(5); /~ Outputs: 120 ~/
```

### Indirect Recursion

Two or more functions call each other in a cyclic manner.

```prog
fn A(n) {
    if n > 0 then {
        display n;
        B(n - 1);
    } end;
}

fn B(n) {
    if n > 0 then {
        display n;
        A(n / 2);
    } end;
}

A(5); /~ Demonstrates indirect recursion. ~/
```

### Tail Recursion

The recursive call is the last operation performed in the function.

```prog
fn sum(n, acc) {
    if n == 0 then {
        return acc;
    } else {
        return sum(n - 1, acc + n);
    } end;
}
display sum(5, 0); /~ Outputs: 15 ~/
```

## Static Scoping

Prog uses static (lexical) scoping, which means the scope of variables is determined by their position in the source code.

**Example:**

```prog
var globalVar : integer = 10;

fn func() {
    var localVar : integer = globalVar + 5;
    display localVar; /~ Uses globalVar from outer scope. ~/
}

func(); /~ Outputs: 15 ~/

fn anotherFunc() {
    var globalVar : integer = 20; /~ Local variable shadows the global one. ~/
    display globalVar; /~ Outputs: 20. ~/
}

anotherFunc();
display globalVar; /~ Outputs: 10 (global variable remains unchanged). ~/
```

**Key Points:**

- Variables declared in inner blocks cannot access variables in outer blocks unless they are in the enclosing scope.
- Shadowing may occur when a local variable has the same name as a global variable.
