### Conditionals
- Valid syntaxes:
    - `if ... then ... else ... end;`
    - `if ... then ... end;` (if condition is false, then evaluates to `None`)
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
- Example
    ``` 
    while (i < 5) {
        i += 1;
        if i == 2 then moveon end;
        if i == 4 then breakout end;
        display i;
    }
    ```
    Output
    ```
    1
    3
    ```

