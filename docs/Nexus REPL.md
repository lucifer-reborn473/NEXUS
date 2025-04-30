## Nexus REPL

The Nexus REPL (Read-Evaluate-Print Loop) provides an interactive environment to write, test, and experiment with Nexus code.

### Getting Started
Launch the REPL by running the nexus_repl.py script:
```
./nexus_repl.py
```
You'll see the welcome message and the primary prompt:
```
Nexus Language REPL v0.1
Type 'help' for assistance or 'exit' to quit
nexus> 
```
Built-in Commands
- `help` - Display help information and example code
- `exit` - Exit the REPL and save command history (you can also use Ctrl+D to exit the REPL)
- `reset` - Clear all variables and functions from the environment
Autocomplete feature
- Press `tab` to autocomplete 
    - Fixed keywords like `var`, `for`, `while`, `else` and `display`
    - User-defined variables and functions

### Writing Code
Enter Nexus code directly at the prompt.  
Example:
```
nexus> var x = 10;
nexus> displayl x + 5;
15
nexus> x*20
200
nexus> x
10
```

### Multi-line Support

The REPL automatically detects incomplete input and switches to continuation mode:  
Example 1:
```
nexus> fn add(a, b) {
...     a + b;
... }
nexus> displayl add(5, 7);
12
```
Example 2:
```
nexus> var x = 100;
100
nexus> if x<50 then {
... displayl "less";
... } else {
... displayl "more";
... } end;
more
nexus>
```
The prompt changes from `nexus>` to `...` when entering multi-line code.

### Exiting the REPL
Type `exit` or press `Ctrl+D` to exit the REPL.