# Control Flow

Control flow mechanisms allow a program to make decisions, repeat actions, and execute code conditionally. In the Prog language, control flow is implemented using **conditional statements** (`if-then-else`) and **looping constructs** (`while` and `for` loops). 

---

## **1. If-Then-Else Statements**

The `if-then-else` construct is used for conditional execution. It evaluates a condition and executes the `THEN` block of code if the condition is true, otherwise the `ELSE` block (optional) if the condition is false.

### **Syntax in Prog**

#### **As Statements**

The `if-then-else` construct can be used as a statement to control the flow of execution. It does not return a value but performs actions based on the condition.

```prog
if <condition> then {
    <statements>
} else {
    <statements>
} end;
```

#### **As Expressions**

The `if-then-else` construct can also be used as an expression, allowing it to evaluate to a value. This is useful when the result of the conditional logic is directly assigned to a variable or used in another expression.

```prog
var result = if <condition> then {
    <expression>
} else {
    <expression>
} end;
```

### **Rules**

- Valid syntax:
  - `if ... then ... else ... end;`
  - `if ... then ... end;` (if the condition is false, then evaluates to `None`)
- Nesting is supported.
- Empty `then` and/or `else` expressions return `None`.

### **Examples**

#### **Using Braces (`{...}`)**

```prog
var a = if 2 == 2 then {
    displayl "inside then";
    42;
} else {
    displayl "inside else";
    7;
} end;
displayl a;
/~ Outputs:
inside then
42 ~/
```

#### **Conditionally Evaluating Expressions**

```prog
var b = if 2 != 2 then a else 5; /> `a` is not declared in this scope but the code runs without error!
displayl b;
/~ Outputs:
5 ~/
```

#### **Nesting**

```prog
var a = if 4 < 3 then if 3 == 2 then 5 else 100 end else 1000 end;
displayl a;
/~ Outputs:
1000 ~/
```

#### **If-Then-Else as a Statement**

```prog
var score  = 85;

if score >= 90 then {
    display "Grade A";
} else if score >= 80 then {
    display "Grade B";
} else {
    display "Grade C";
} end;
/~ Outputs: Grade B ~/
```

#### **If-Then-Else as an Expression**

```prog
var score = 85;

var grade : string = if score >= 90 then {
    "Grade A"
} else if score >= 80 then {
    "Grade B"
} else {
    "Grade C"
} end;

display grade;
/~ Outputs: Grade B ~/
```

---

## **2. While Loops**

The `while` loop repeats a block of code as long as a specified condition is true. It is useful for indefinite iteration where the number of iterations is not known beforehand.

### **Syntax in Prog**

```prog
while (<condition>) {
    <statements>
}
```

### **Example**

```prog
var i = 0;

while (i < 5) {
    display i;
    i += 1;
}
/~ Outputs: Numbers from 0 to 4 ~/
```

---

## **3. For Loops**

The `for` loop is used for definite iteration, where the number of iterations is known beforehand. It includes initialization, a condition, and an update expression.

### **Syntax in Prog**

```prog
for (<initialization>; <condition>; <update>) {
    <statements>
}
```

### **Example**

```prog
for (var i = 0; i < 5; i += 1) {
    display i;
}
/~ Outputs: Numbers from 0 to 4 ~/
```

---

## **4. Break and Continue**

- **Break (`breakon`)**: Exits the loop immediately.
- **Continue (`moveon`)**: Skips the current iteration and moves to the next.

### **Syntax in Prog**

```prog
while (<condition>) {
    if (<break_condition>) then breakon end;
    if (<continue_condition>) then moveon end;
    <statements>
}
```

### **Example**
```prog
var i = 0;

while (i < 5) {
    i += 1;
    if i == 2 then moveon end;
    if i == 4 then breakon end;
    display i;
}
/~ Outputs: 1, 3 ~/
```

---

## **5. Nested Loops and Scoping**

Nested loops allow one loop to be placed inside another. Each loop has its own scope, and variables declared in an inner loop do not affect the outer loop.

### **Example**

```prog
for (var i = 0; i < 3; i += 1) {
    for (var j  = 0; j < 2; j += 1) {
        display i * j;
    }
}
/~ Outputs: 0, 0, 0, 1, 0, 2 ~/
```

---
