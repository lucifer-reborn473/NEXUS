from bytecode_gen_new import *
import math

class BytecodeVM:
    def __init__(self, bytecode):
        self.bytecode = bytecode
        self.ip = 0                # Instruction pointer
        self.stack = []            # Operand stack
        self.frames = [{}]         # Call frames for variable storage
        self.frame_index = 0       # Current frame index
        self.builtins = {  # Built-in functions
        # Existing built-ins
        'char': (chr, 1),
        'ascii': (ord, 1),
        'length': (len, 1),
        'string': (str, 1),
        'integer': (int, 1),
        'decimal': (float, 1),
        'boolean': (bool, 1),
        
        # Array operations - modified to return the array
        'array_insert': (lambda arr, idx, val: (arr.insert(idx, val), arr)[1], 3),
        'array_append': (lambda arr, val: (arr.append(val), arr)[1], 2),
        'array_remove': (lambda arr, idx: (arr.pop(idx), arr), 2),
        'array_popfront': (lambda arr: (arr.pop(0), arr), 1),
        'array_popback': (lambda arr: (arr.pop(), arr), 1),
        'array_clear': (lambda arr: (arr.clear(), arr), 1),
        'array_sort': (lambda arr: sorted(arr), 1),
        'array_sort_with_comparator': (lambda arr, comp: sorted(arr, key=comp), 2),
        # String operations
        'string_index': (lambda s, idx: s[idx], 2),
        'string_pushfront': (lambda s, val: val + s, 2),
        'string_pushback': (lambda s, val: s + val, 2),
        'string_popfront': (lambda s: s[1:], 1),
        'string_popback': (lambda s: s[:-1], 1),
        'string_set': (lambda s, idx, val: s[:idx] + val + s[idx + 1:], 3),
        'string_insert': (lambda s, idx, val: s[:idx] + val + s[idx:], 3),
        'string_remove_at': (lambda s, idx: s[:idx] + s[idx + 1:], 2),
        
        # Hash operations
        'hash_remove': (lambda hash_map, key: hash_map.pop(key, None), 2),
        
        # Type checking and generic operations
        'type_check': (lambda obj: type(obj) is list, 1),
        'obj_slice': (lambda obj, start, end, step: obj[start:end:step], 4),
        'typeof': (lambda val: next((t for t, ty in [
            ('integer', int), ('decimal', float), ('string', str), 
            ('array', list), ('Hash', dict), ('boolean', bool)
        ] if isinstance(val, ty)), 'unknown'), 1),

        # Format string operations
        'format_string_1': (lambda template, var1: template.replace('{1}', str(var1)), 2),
        'format_string_2': (lambda template, var1, var2: template.replace('{1}', str(var1)).replace('{2}', str(var2)), 3),
        
        # Math operations
        'math_abs': (lambda x: math.fabs(x), 1),
        'math_min': (lambda arr: min(arr), 1),
        'math_max': (lambda arr: max(arr), 1),
        'math_round': (lambda x, digits=0: round(x, digits), 2),
        'math_ceil': (lambda x: math.ceil(x), 1),
        'math_floor': (lambda x: math.floor(x), 1),
        'math_truncate': (lambda x: math.trunc(x), 1),
        'math_sqrt': (lambda x: math.sqrt(x), 1),
        'math_cbrt': (lambda x: x ** (1/3), 1),
        'math_pow': (lambda x, y: math.pow(x,y), 2),
        'math_exp': (lambda x: math.exp(x), 1),
        'math_log': (lambda x: math.log(x), 1),
        'math_log10': (lambda x: math.log10(x), 1),
        'math_log2': (lambda x: math.log2(x), 1),
        'math_sin': (lambda x: math.sin(x), 1),
        'math_cos': (lambda x: math.cos(x), 1),
        'math_tan': (lambda x: math.tan(x), 1),
        'math_asin': (lambda x: math.asin(x), 1),
        'math_acos': (lambda x: math.acos(x), 1),
        'math_atan': (lambda x: math.atan(x), 1),
        'math_atan2': (lambda y, x: math.atan2(y, x), 2),
        'math_sinh': (lambda x: math.sinh(x), 1),
        'math_cosh': (lambda x: math.cosh(x), 1),
        'math_tanh': (lambda x: math.tanh(x), 1),
        'math_asinh': (lambda x: math.asinh(x), 1),
        'math_acosh': (lambda x: math.acosh(x), 1),
        'math_atanh': (lambda x: math.atanh(x), 1),
        'math_pi': (lambda: math.pi, 0),
        'math_e': (lambda: math.e, 0),
        }
    
    def current_frame(self):
        """Get the current variable frame"""
        return self.frames[self.frame_index]
    
    def push(self, value):
        """Push value onto the stack"""
        self.stack.append(value)
    
    def pop(self):
        """Pop value from the stack"""
        if not self.stack:
            raise RuntimeError("Stack underflow")
        return self.stack.pop()
    
    def run(self):
        """Execute the bytecode"""
        while self.ip < len(self.bytecode.insns):
            instruction = self.bytecode.insns[self.ip]
            self.execute_instruction(instruction)
            # print(f"IP: {self.ip}, Stack: {self.stack}")
            
        # Return the top of the stack (if any) as the program result
        return self.stack[0] if self.stack else None
    
    def perform_typecast(self, value, dtype):
        """Cast value to the specified type"""
        try:
            match dtype:
                case "integer":
                    return int(value)
                case "decimal":
                    return float(value)
                case "uinteger":
                    val = int(value)
                    return abs(val)
                case "string":
                    return str(value)
                case "array":
                    if not isinstance(value, list):
                        raise ValueError(f"Cannot cast {value} to array")
                    return value
                case "Hash":
                    if not isinstance(value, dict):
                        raise ValueError(f"Cannot cast {value} to Hash")
                    return value
                case "boolean":
                    return bool(value)
                case None:
                    return value
                case _:
                    raise ValueError(f"Unknown data type: {dtype}")
        except (ValueError, TypeError) as err:
            raise ValueError(f"Typecasting error to type '{dtype}': {err}")
    
    def execute_instruction(self, instruction):
        """Execute a single instruction"""
        match instruction:
            case I.HALT():
                # Stop execution
                self.ip = len(self.bytecode.insns)  # Move past the last instruction
                
            case I.PUSH():
                # Push value onto stack
                self.push(instruction.value)  # Access value as an attribute
                self.ip += 1
                
            case I.POP():
                # Pop value from stack
                self.pop()
                self.ip += 1
                
            case I.DUP():
                # Duplicate top value on stack
                value = self.pop()
                self.push(value)
                self.push(value)
                self.ip += 1
                
            # Arithmetic operations
            case I.ADD():
                # print(self.stack)
                right = self.pop()
                # print(f"Right: {right}")
                left = self.pop()
                # print(f"Left: {left}")
                
                self.push(left + right)
                self.ip += 1
                
            case I.SUB():
                right = self.pop()
                left = self.pop()
                self.push(left - right)
                self.ip += 1
                
            case I.MUL():
                right = self.pop()
                left = self.pop()
                self.push(left * right)
                self.ip += 1
                
            case I.DIV():
                right = self.pop()
                left = self.pop()
                self.push(left / right)
                self.ip += 1
                
            case I.MODULO():
                right = self.pop()
                left = self.pop()
                self.push(left % right)
                self.ip += 1
                
            case I.POW():
                right = self.pop()
                left = self.pop()
                self.push(left ** right)
                self.ip += 1
                
            # Comparison operations
            case I.EQ():
                right = self.pop()
                left = self.pop()
                self.push(left == right)
                self.ip += 1
                
            case I.NE():
                right = self.pop()
                left = self.pop()
                self.push(left != right)
                self.ip += 1
                
            case I.LT():
                right = self.pop()
                left = self.pop()
                self.push(left < right)
                self.ip += 1
                
            case I.GT():
                right = self.pop()
                left = self.pop()
                self.push(left > right)
                self.ip += 1
                
            case I.LE():
                right = self.pop()
                left = self.pop()
                self.push(left <= right)
                self.ip += 1
                
            case I.GE():
                right = self.pop()
                left = self.pop()
                self.push(left >= right)
                self.ip += 1
        # Logical operations
            case I.AND():
                right = self.pop()
                left = self.pop()
                self.push(left and right)
                self.ip += 1
                
            case I.OR():
                right = self.pop()
                left = self.pop()
                self.push(left or right)
                self.ip += 1
                
            case I.NOT():
                value = self.pop()
                self.push(not value)
                self.ip += 1
                
            # Bitwise operations
            case I.BITAND():
                right = self.pop()
                left = self.pop()
                self.push(left & right)
                self.ip += 1
                
            case I.BITOR():
                right = self.pop()
                left = self.pop()
                self.push(left | right)
                self.ip += 1
                
            case I.BITXOR():
                right = self.pop()
                left = self.pop()
                self.push(left ^ right)
                self.ip += 1
                
            case I.BITNOT():
                value = self.pop()
                self.push(~value)
                self.ip += 1
                
            case I.LSHIFT():
                right = self.pop()
                left = self.pop()
                self.push(left << right)
                self.ip += 1
                
            case I.RSHIFT():
                right = self.pop()
                left = self.pop()
                self.push(left >> right)
                self.ip += 1
                
            # Control flow
            case I.JMP():
                # Jump to target
                self.ip = instruction.label.target
                # print(f'Jumped to {self.ip}')
                
            case I.JMP_IF_TRUE():
                # Jump to target if top value is true
                condition = self.pop()
                if condition:
                    self.ip = instruction.label.target
                else:
                    self.ip += 1
                    
            case I.JMP_IF_FALSE():
                # Jump to target if top value is false
                condition = self.pop()
                if not condition:
                    self.ip = instruction.label.target
                else:
                    self.ip += 1
                    
            # Variable operations
            case I.LOAD():
                # Load variable onto stack
                name = instruction.name
                if name in self.builtins:
                    self.push(self.builtins[name])
                else:
                    # Look for variable in all frames, starting from innermost
                    for i in range(self.frame_index, -1, -1):
                        if name in self.frames[i]:
                            self.push(self.frames[i][name])
                            break
                    else:
                        raise RuntimeError(f"Variable '{name}' not defined")
                self.ip += 1

                
            case I.STORE():
                # Store top value in variable
                name = instruction.name
                value = self.pop()
                self.current_frame()[name] = value
                # If the variable is already in the current scope, update it
                # if name in self.current_frame():
                #     self.current_frame()[name] = value
                # else:
                #     # Otherwise, look for it in parent scopes
                #     found = False
                #     for i in range(self.frame_index - 1, -1, -1):
                #         if name in self.frames[i]:
                #             # Update the variable in the outer scope
                #             self.frames[i][name] = value
                #             found = True
                #             break
                    
                #     # If not found in any scope, create it in the current scope
                #     if not found:
                #         self.current_frame()[name] = value
                
                self.ip += 1

                # Function operations
            case I.CALL():
                name = instruction.name
                if name in self.builtins:
                    # Handle builtin function calls
                    num_args = self.builtins[name][1]
                    
                    # Pop arguments in reverse order
                    args = []
                    for _ in range(num_args):
                        args.insert(0, self.pop())  # Reverse order
                    
                    # Call the builtin and push result
                    # print(f"Calling builtin function '{name}' with args: {args}")
                    result = self.builtins[name][0](*args)
                    # print(f"Result: {result}")
                    if result is not None:  # Don't push None results
                        if isinstance(result, tuple) and len(result) == 2:
                            self.push(result[0])
                            self.push(result[1])
                        else:
                            self.push(result)
                    self.ip += 1
                else:
                   # Look for the function in all frames, starting from the current one
                    target = None
                    for frame_idx in range(self.frame_index, -1, -1):
                        if name in self.frames[frame_idx]:
                            target = self.frames[frame_idx][name]
                            break
                            
                    if target is None:
                        raise RuntimeError(f"Function '{name}' not defined")
                    
                    # Create a new frame
                    self.frames.append({})
                    self.frame_index += 1
                    
                    # Save return address
                    self.current_frame()['__return_addr__'] = self.ip + 1
                    
                    # Jump to function
                    self.ip = target

                
            case I.RETURN():
                # Get return address
                return_addr = self.current_frame().get('__return_addr__')
                
                # Restore previous frame
                self.frames.pop()
                self.frame_index -= 1
                
                # Jump to return address
                self.ip = return_addr
                
            case I.PUSHFN():
                # Store function entry point in current frame
                name = instruction.name
                self.current_frame()[name] = instruction.label.target
                # print(f"Pushed function '{name}' at {self.ip}")
                self.ip += 1
            # Collection operations
            case I.MAKE_ARRAY():
                # Create an array from the top 'size' values on the stack
                size = instruction.size
                elements = []
                for _ in range(size):
                    elements.insert(0, self.pop())  # Insert at front to maintain order
                self.push(elements)
                self.ip += 1
                
            case I.MAKE_HASH():
                # Create a hash from the top 'size*2' values on the stack (key-value pairs)
                size = instruction.size
                keys = []
                values = []
                for _ in range(size):
                    value = self.pop()
                    key = self.pop()
                    # Insert at the beginning to restore original order
                    keys.insert(0, key)
                    values.insert(0, value)
                # Create dictionary with preserved order
                hash_map = {k: v for k, v in zip(keys, values)}
                self.push(hash_map)
                self.ip += 1

                
            case I.ARRAY_GET():
                # Get element from array
                index = self.pop()
                array = self.pop()
                self.push(array[index])
                self.ip += 1
                
            case I.ARRAY_SET():
                # Set element in array
                value = self.pop()
                index = self.pop()
                array = self.pop()
                array[index] = value
                self.push(array)  # Push the modified array back
                self.ip += 1
                
            case I.HASH_GET():
                # Get value from hash
                key = self.pop()
                hash_map = self.pop()
                self.push(hash_map[key])
                self.ip += 1
                
            case I.HASH_SET():
                # Set value in hash
                value = self.pop()
                key = self.pop()
                hash_map = self.pop()
                hash_map[key] = value
                self.push(hash_map)  # Push the modified hash back
                self.ip += 1
            # I/O operations
            case I.PRINT():
                # Print top value without newline
                value = self.pop()
                print(value, end="")
                self.push(None)
                self.ip += 1
                
            case I.PRINTLN():
                # Print top value with newline
                value = self.pop()
                print(value)
                self.push(None)
                self.ip += 1
                
            case I.INPUT():
                # Read input from user
                prompt = self.pop()
                self.push(input(prompt))
                self.ip += 1
                
            # Typecasting
            case I.TYPECAST():
                # Cast top value to specified type
                dtype = instruction.dtype
                value = self.pop()
                casted = self.perform_typecast(value, dtype)
                self.push(casted)
                self.ip += 1
            # Add to execute_instruction method in BytecodeVM
            # In the execute_instruction method of BytecodeVM
            case I.PUSH_SCOPE():
                # Create a new frame for the scope
                self.frames.append({})
                self.frame_index += 1
                self.ip += 1
            case I.POP_SCOPE():
                # Remove the scope frame and restore parent scope
                self.frames.pop()
                self.frame_index -= 1
                self.ip += 1

            case _:
                # Unknown instruction
                raise RuntimeError(f"Unknown instruction: {instruction.__class__.__name__}")


def execute_bytecode(bytecode):
    """Execute bytecode and return the final stack"""
    vm = BytecodeVM(bytecode)
    result = vm.run()
    return result

def run_program(program,display_bytecode=False):
    """Compile and execute a program."""
    bytecode, symbols = compile_program(program)
    if display_bytecode:
        bytecode.print_bytecode()
    return execute_bytecode(bytecode)

# Example usage
if __name__ == "__main__":
    from parser import parse
    
    # Sample program
    program = """
    var integer x = 5;
    var integer y = 10;
    displayl (x + y);
    """
    program ="""
    var integer sum=0;
    for (var i=1;i<10;i+=1){
        sum+=i;
    };
    displayl sum;
    display "done";
"""
    program = """ 
    fn loopFunction(n) {
        var i = 0;
        while (i < n) {
            displayl(i);
            i = i + 1;
        };
    };
    var x = 5;
    displayl("Calling loopFunction with x=5");
    loopFunction(x);
"""
    

    program="""
    var a= char (66);
    displayl a;
    var b= ascii("A");
    displayl b;
    var c= char (ascii('x') + ascii (char(1)));
    displayl c;  
"""

    program=""" 
    var str = "Code";
    str.PushBack("!");
    str.PushFront("Let's ");
    displayl str;             /> Output: "Let's Code!"
    str[6] = "c";
    displayl str;             /> Output: "Let's code!"
    var slice = str.Slice(6, 10);
    displayl slice;           /> Output: "code
"""
    # run_program("displayl((5 + 3) * 2 - 4 / 2);")
    program="""displayl "Fibonacci:";

    fn fib(a) {
        if (a==1 or a==2) then 1 else fib(a-1) + fib(a-2) end;
    };
    displayl "----";
    var x = 20;
    displayl x;
    displayl fib(x);"""

#     program="""
#     var integer sum=0;
#     for (var i=1;i<10;i+=1){
#         sum+=i;
#     };
#     displayl sum;
#     display "done";
# """

#     program="""
#     var u = 100;
#     for(var u=0; u<3; u+=1){
#         var b = 2;
#         displayl b;
#     }
#     displayl 179;
#     displayl u;
# """
    program="""var sum = 0;
    for (var i = 0; i < 3; i += 1) {
        var j = 0;
        while (j < 2) {
            repeat (2) {
                sum += i + j;
            }
            j += 1;
        }
    }
    displayl sum;"""

    program="""
    var str = \"Length Test\";
    var len = str.Length();
    display len;
    """

    # pprint(parse(program))
    # run_program(program,display_bytecode=True)

    prog = """
    fn calculate(x, y) {
        displayl (x + y) * (x - y) / (x % y + 1.0);
        displayl (x ** y) - (x * y) + (x / y);
    };
    calculate(4.4, 2.2);
"""
    pprint(parse(prog, SymbolTable()))
    run_program(prog, display_bytecode=True)