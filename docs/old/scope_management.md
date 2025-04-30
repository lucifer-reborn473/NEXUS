# Scope Management in Nexus

This document provides an overview of how scoping works in Nexus.

---

## Scoping in Nexus

Nexus is based on lexical (or static) scoping, meaning the scope of variables is determined by their position in the source code.

### **Key Features**

- Structural hierarchy of scopes is created during parsing.
- Lexical structure is captured while parsing to identify and catch duplicate declarations for variables and functions.
- Resolution of values occurs during the evaluation phase.

---

## Rules

- Conditionals and loops have their own local scopes.
- Variables declared in inner blocks cannot access variables in outer blocks unless they are in the enclosing scope.
- Shadowing occurs when a local variable has the same name as a global variable.

---

## Examples

### **Example 1: Local Scope**

```prog
fn foo(i) {
    if i == 1 then var a = 2 else 5 end;
    a = 42;
}
displayl foo(1);
```

---

### **Example 2: Shadowing**

```prog
var x = 9;

fn bar() {
    x;
}

fn foo() {
    var x = 100;
    bar();
}

displayl foo(); /~ Outputs: 9 ~/
```

---

### **Example 3: Nested Scopes**

```prog
var x = 2;

fn foo() {
    var x = 300;
    x;
}

fn bar(x) {
    x += 1000;
    x;
}

fn baz(x) {
    if x < 5 then foo() else bar(x) end;
}

displayl baz(4); /~ Outputs: 300 ~/
displayl baz(6); /~ Outputs: 1006 ~/
```

---

### **Example 4: Function Scope**

```prog
var x = 1000;

fn foo() {
    fn bar() {
        x;
    }
    var x = 117;
    bar();
}

displayl foo(); /~ Outputs: 117 ~/
```

---

### **Example 5: Recursive Scoping**

```prog
var a = "g-";

fn foo(x, i) {
    if i == 1 then var a = "1-" else "dummy" end;
    if x == 1 then "k" else a + foo(x - 1, i + 1) end;
}

displayl foo(5, 1); /~ Outputs: g-g-g-g-k ~/
```