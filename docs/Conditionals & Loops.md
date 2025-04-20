### Conditionals
- Valid syntaxes:
    - `if ... then ... else ... end;`
    - `if ... then ... end;` (if condition is false, then evaluates to `None`)
- Nesting supported
- Empty `then` and/or `else` expressions return `None`
- Examples:
    - Using braces (`{...}`)
        ```prog
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
        ```prog
        inside then
        42
        ```

    - Conditionally evaluating expressions
        ```prog
        var b = if 2!=2 then a else 5; 
        // a is not declared in this scope but the code runs without error!
        displayl b;
        ```
        Output:
        ```prog
        5
        ```

    - Nesting:
        - Example 1:
            ```prog
            var a = if 4<3 then if 3==2 then 5 else 100 end else 1000 end;
            displayl a;
            ```
            Output:
            ```prog
            1000
            ```
        -  Example 2:
            ```
            var a = 100;
            var b;
            if a<5 then {
                b = "less than 5";
            } else if a<50 then {
                        b = "less than 50";
                    } else if a<60 then {
                            b = "less than 60";
                        } else {
                            b = "more than 60";
                        } end
                    end 
            end;
            displayl b;
            ```
            Output:
            ```
            more than 60
            ```

### Loops
- `for` and `while` loops supported with similar syntax as in C/C++.
- Example:

    ```prog
    for(var i=0; i<10; i+=1){
        displayl i;
    }
    ```

- `moveon` statement equivalent to `continue` statement in Python.
- `breakout` statement equivalent to `break` statement in Python.
- Example:

    ```prog
    while (i < 5) {
        i += 1;
        if i == 2 then moveon end;
        if i == 4 then breakout end;
        display i;
    }
    ```
    Output:
    ```prog
    1
    3
    ```

- Example
    ```
    var u = 100;
    for(var u=0; u<3; u+=1){
        var b = u;
        displayl b;
    };
    displayl u;
    ```
    Output:
    ```
    0
    1
    2
    100
    ```
