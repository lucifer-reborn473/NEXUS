## CS 327: Compilers (2025) Project

### Making our own Programming Language & its Compiler

# Operator Precedence Table (Highest to Lowest)

| **Precedence** | **Operator**                           | **Description**                   | **Associativity**                                          |
| -------------------- | -------------------------------------------- | --------------------------------------- | ---------------------------------------------------------------- |
| 1                    | **Numbers**                            | Numeric values (constants or variables) | N/A                                                              |
| 2                    | `()`                                       | Parentheses (for grouping expressions)  | Left-to-Right                                                    |
| 3                    | `**`                                       | Exponentiation                          | Right-to-Left                                                    |
| 4                    | `div_dot`                                  | Floor Division using dot notation       | Left-to-Right                                                    |
| 5                    | `div_slash`                                | Regular Division using slash notation   | Left-to-Right                                                    |
| 6                    | `%`                                        | Modulo (Remainder)                      | Left-to-Right                                                    |
| 7                    | `*`                                        | Multiplication                          | Left-to-Right                                                    |
| 8                    | `-`                                        | Subtraction                             | Left-to-Right                                                    |
| 9                    | `+`                                        | Addition                                | Left-to-Right                                                    |
| 10                   | `<<`, `>>`                               | Bitwise Shift (Left, Right)             | Left-to-Right                                                    |
| 11                   | `<`, `>`, `<=`, `>=`, `==`, `!=` | Comparison Operators                    | Left-to-Right                                                    |
| 12                   | `&`, `^`, `~`                        | Bitwise Operators                       | Left-to-Right                                                    |
| 13                   | `and`, `or`, `not`                     | Logical Operators                       | Left-to-Right (`and`, `or`) `<br>` Right-to-Left (`not`) |
