### Functions
- Declared using the `fn` keyword.
- Redeclaration is not allowed in the same scope and is caught before evaluation.
- Calling a function with empty body returns `None`
- Examples:
    - The below example declares and calls a function `giveSum()` which takes two parameters `a` and `b` and returns their sum
        ```  
        fn giveSum(a, b){  
            a+b;  
        };  
        displayl giveSum(40, 2);  
        ```  
        Output:
        ```
        42
        ```
    - Function to calculate the nth Fibonacci number:
        ```
        fn fib(n){
            if n==1 or n==2 then 1 else fib(n-1) + fib(n-2) end;
        };
        displayl fib(10); /> outputs 55
        ```  
        Note: fib(31) takes nearly 22.8 seconds, while fib(32) takes nearly 35.4 seconds (averaged over 3 iterations)

#### Functions are first-class citizens in Nexus
- Example 1:
    ```  
    var x = 100;
    fn bar(){
        x;
    }
    fn foo(g){ 
        g() + 2; /> takes function as parameter
    }
    displayl foo(bar);  
    ```  
    Output
    ```
    102
    ```

- Example 2:
    ```
    fn foo(){
        fn bar(){
            x+2;
        }
        bar; /> returns a function
    }
    var x = 40;
    var y = foo(); /> assigns to a variable
    displayl y();
    ```  
    Output
    ```
    42
    ```

# Scoping
- Nexus is based on lexical (or, static) scoping.

- structural hierarchy of scopes made during parsing
    - lexical structure captured while parsing
    - helps identify and catch duplicate declarations for variables and functions
- resolution of values during the evaluation phase (see Example 6 below)

- Conditionals and loops have their own local scopes

- Example 1:
    ```
    fn foo(i){
        if i==1 then var a = 2 else 5 end;
        a = 42;
    };
    displayl foo(1);
    ```  
- Example 2:
    ```
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
    ```
    9
    ```


- Example 3:
    ```
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
    ```
    300
    1006
    ```

- Example 4:
    ```
    var x = 1000;
    fn foo() {
        fn bar() {
            x;
        }
        var x = 117;
        bar();
    }
    displayl foo();
    ```  
    Output
    ```
    117
    ```

- Example 5:
    ```
    var a = "g-";
    fn foo(x, i){
        if i==1 then var a = "1-" else "dummy" end;
        if x==1 then "k" else a + foo(x-1, i+1) end; 
    };
    displayl foo(5,1);
    ```  
    Output:
    ```
    g-g-g-g-k
    ```

- Example 6:
    ```
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
    ```
    10
    ```
