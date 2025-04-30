# Recursive Functions in Nexus

This document covers how recursive functions work in Nexus.

---

## Recursive Functions

Nexus supports recursive functions, allowing a function to call itself either directly or indirectly.

### **Direct Recursion**

A function calls itself until a base case is met.

```prog
fn fib(n) {
    if n == 1 or n == 2 then 1 else fib(n - 1) + fib(n - 2) end;
}
displayl fib(10); /> Outputs: 55
```

---

## Functions as First-Class Citizens

Functions in Nexus are first-class citizens, meaning they can be assigned to variables, passed as arguments, and returned from other functions.

### **Examples**

#### **Assigning a Function to a Variable**

```prog
var x = 100;

fn bar() {
    x;
}

fn foo(g) {
    g() + 2; /> Takes a function as a parameter
}

displayl foo(bar); /~ Outputs: 102 ~/
```

#### **Returning a Function**

```prog
fn foo() {
    fn bar() {
        x + 2;
    }
    bar; /> Returns a function
}

var x = 40;
var y = foo(); /> Assigns the returned function to a variable
displayl y(); /~ Outputs: 42 ~/
```