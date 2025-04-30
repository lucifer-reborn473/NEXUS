### Functions
- Functions are declared using the `fn` keyword
     - Example: The below example declares and calls a function `giveSum` which takes two parameters `a` and `b` and returns their sum
        ```prog
        fn giveSum(a, b){
            a+b;
        };
        displayl giveSum(40, 2);
        ```
        Output:
        ```prog
        42
        ```

- Nexus supports some useful in-built functions:
    - `sort(A)` takes an array argument `A` and returns the sorted version
        - Takes an optional second argument of boolean type (`False` means sort in non-decreasing order, `True` means sort in non-increasing order)
    - `so(x)` returns the boolean value for `x` where `x` is of any type
    - `typeof(x)` returns the type of `x`
        - Possible values: integer, decimal, string, array, Hash, boolean, None
        - Return type of this function is `string`
    - `lower(s)` returns the lower-cased version of string `s`
    - `upper(s)` returns the upper-cased version of string `s`
    - `reverse(A)` returns the reversed-version of the array argument `A`
    - `unique(A)` returns the array `A` afrer removing all duplicates from it
    - `num(s)` returns the number form of string `s` (e.g. num("2.3") returns 2.3)
        - for a number type argument `n`, `num(n)` returns the argument as is (e.g. num(30) returns 30)
    

- Redeclaration is not allowed in the same scope and is caught before evaluation.
- Arrays and hashes are passed-by-value in functions
- Calling a function with empty body returns `None`
- `return` keyword is supported in the bytecode VM, and not in the tree-walk interpreter (a work under progress). Below examples demonstrate the several ways you can use functions in Nexus without needing the `return` keyword.
- Note: In this language, function declarations must appear at the top level or within other function bodies. You cannot assign a function declaration to a variable using `var`. Use the name of function declaration instead. 
    - Example: `var a = fn foo() {...};` is not allowed; you should instead do `fn foo(){...}; var a = foo;`
- <a id="changes-outer-var"> </a> Assigning to a non-local variable inside a function finds and modifies the outer-scope variable (if it exists), else throws error that the variable was not found (in any of its parent scope).
- Examples:
    - Function to calculate the nth Fibonacci number:
        ```prog
        fn fib(n){
            if n==1 or n==2 then 1 else fib(n-1) + fib(n-2) end;
        };
        displayl fib(10); /> outputs 55
        ```

    - Another example
        ```
        var x="hi";
        fn foo(x){
            x = x-1;
            x;
        };
        displayl foo(10);
        displayl x;
        ```
        Output:
        ```
        9
        hi
        ```
    - Example:
        ```
        fn foo(x){
            fn bar(){
                x = x - 1;
                x;
            };
            bar() + x; /> evaluates to 9 + 9 = 18
        };
        displayl foo(10);
        ```
        Output:
        ```
        18
        ```

#### Functions are first-class citizens in Nexus
- Example 1:
    ```prog
    var x = 100;
    fn bar(){
        x;
    };
    fn foo(g){ 
        g() + 2; /> function can be passed as parameter
    };
    displayl foo(bar);
    ```
    Output
    ```prog
    102
    ```

- Example 2:
    ```prog
    fn foo(){
        fn bar(){
            x+2;
        };
        bar; /> functions can be returned
    };
    var x = 40;
    var y = foo(); /> assigned to a variable
    displayl y();
    ```
    Output
    ```prog
    42
    ```

- Example 3:
    ```
    fn add(a, b) {
        a + b;
    };
    fn subtract(a, b) {
        a - b;
    };
    fn multiply(a, b) {
        a * b;
    };
    var funcs = [add, subtract, multiply]; /> functions as elements in an array

    displayl [funcs[0](10,5), funcs[1](10,5), funcs[2](10,5)];
    ```
    Output:
    ```
    [15, 5, 50]
    ```

# Scoping
- Nexus is based on lexical (or, static) scoping.
- Conditionals and loops have their own local scopes.

- Example 1 (produces an error, as no declaration for `a` found corresponding to `a = 42`):
    ```prog
    fn foo(i){
        if i==1 then var a = 2 else 5 end;
        a = 42;
    };
    displayl foo(1);
    ```

- Example 2:
    ```prog
    var x = 9;
    fn bar() {
        x;
    };
    fn foo() {
        var x = 100;
        bar();
    };
    displayl foo();
    ```
    Output
    ```prog
    9
    ```

- Exampl 3:
    ```prog
    var x = 2;
    fn foo(){
        var x = 300;
        x;
    };
    fn bar(x){
        x += 1000;
        x;
    };
    fn baz(x){
        if x<5 then foo() else bar(x) end;
    };
    displayl baz(4);
    displayl baz(6);
    ```
    Output:
    ```prog
    300
    1006
    ```

- Example 4:
    ```
    fn foo() {
        fn bar() {
            x;
        };
        var x = 117;
        bar();
    };
    displayl foo();
    ```
    Output
    ```prog
    117
    ```

- Example 5:
    ```prog
    fn foo(i){
        fn bar(){
            i;
        };
        fn baz(){
            bar();
        };
        if i==10 then baz() else foo(i+1) end;
    };
    displayl foo(0);
    ```
    Output:
    ```prog
    10
    ```

## Closures
- Nexus also supports closures (passes the Knuth's Man or Boy test)

- Knuth's Man or Boy test as tested in Nexus (the below code outputs for different `k` values (k=0 to k=10)):
    ```
    fn A(k, x, y, z, w, v) {
        fn B() {
            k = k - 1;
            A(k, B, x, y, z, w);
        };
        
        if k <= 0 then w() + v() else B() end;
    };

    fn one() { 1; };
    fn negone() { 0-1; };
    fn zero() { 0; };

    for(var k = 0; k<=10; k+=1){
        displayl A(k, one, negone, negone, one, zero);
    };
    ```
    Output:
    ```
    1
    0
    -2
    0
    1
    0
    1
    -1
    -10
    -30
    -67
    ```

- The below simpler examples describe more on closure's functioning in Nexus:

    - Example 1: 
        ```prog
        var x = 5;
        fn foo(){
            var x = 12;
            fn bar(){
                x;
            }
            bar; /> returns a function
        };
        var y = foo();
        displayl y();
        ```
        Output:
        ```
        12
        ```
    
    - Example 2: 
        ```prog
        fn foo(g){
            g() + 2;
        };
        fn baz(){
            var x = 100;
            fn bar(){
                x;
            }
            foo(bar);
        };
        displayl baz();
        ```
        Output
        ```
        102
        ```
    - Example 3: 
        ```
        var x = 100;
        fn foo(i){
            fn bar(){
                x+i;
            };
            if i==42 then bar else foo(i+1) end;
        };
        var y = foo(0);
        displayl y();
        ```
        Output:
        ```
        142
        ```
    - Example 4: A counter
        ```prog
        fn counter() {
            var count = 0;
            fn increment() {
                count = count + 1;
            }
            increment;
        }
        var c = counter();
        displayl c();
        displayl c();
        displayl c();
        ```
        Output:
        ```
        1
        2
        3
        ```

    - Example 5:
        ```
        fn multiplier(factor) {
            fn multiply(n) {
                n * factor;
            };
            multiply;
        };
        var twox        = multiplier(2);
        var hundredx    = multiplier(100);

        displayl twox(5);
        displayl hundredx(5);
        ```
        Output:
        ```
        10
        500
        ```

    - Example 6:
        ```
        var k = 1000;
        fn foo(k){
            fn bar(){
                k = k-1;
                displayl k;
            };
            bar;
        };

        var y = foo(10);
        y();
        var r = y;
        r();
        ```
        Output:
        ```
        9
        8
        ```
    
    - Example 7:
        ```
        fn A(k, g){
            fn B(){
                k = k+5;
            };
            if k==0 then g() else A(k-1, B) + g() end;
        };
        fn five(){
            5;
        };
        displayl A(2, five);
        ```
        Output:
        ```
        18
        ```
    
    - Example 8:
        ```
        fn foo(){
            var k = "cosmos";
            fn bar(){
                k;
            };
            var A = [bar];
            A[0];
        };
        var y = foo();
        displayl y();
        ```
        Output:
        ```
        cosmos
        ```