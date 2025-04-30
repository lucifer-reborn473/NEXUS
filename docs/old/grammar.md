# Grammar for the Prog Language

This document outlines the overall grammar for the Nexus language, including lexical elements and tokens used by the compiler.

## Lexical Elements

### Keywords

- `if`, `else`, `then`, `end`
- `display`, `displayl`
- `while`, `for`
- `var`, `fn`, `fnrec`
- `ascii`, `char`
- `proc`, `array`, `return`

### Base Types

- `integer`
- `decimal`
- `uinteger`

### Operators

- **Arithmetic:** `+`, `-`, `*`, `/`, `%`, `÷`
- **Logical:** `&&`, `||`, `==`, `!=`
- **Bitwise:** `&`, `|`, `^`
- **Assignment:** `=`, `+=`, `-=`, `*=`, `/=`, `%=`

### Special Tokens

- Boolean values: `True`, `False`
- Semicolons (`;`) for statement termination
- Parentheses (`(`, `)`) for grouping
- Braces (`{`, `}`) for block scope
- Square brackets (`[`, `]`) for array indexing
- String literals enclosed in single or double quotes
