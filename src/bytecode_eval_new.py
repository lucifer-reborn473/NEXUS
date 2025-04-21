from bytecode_gen_new import *
import math
from evaluator import execute

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
        'math_sum': (lambda arr: sum(arr), 1),
        'math_avg': (lambda arr: sum(arr) / len(arr), 1),
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
            # print(f"IP: {self.ip}, Stack: {self.stack}") # printer
            
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
                
            # Unary operations
            case I.UPLUS():
                # Unary plus - essentially does nothing
                value = self.pop()
                self.push(+value)  # Unary plus (maintains value)
                self.ip += 1
                
            case I.UMINUS():
                # Unary minus - negates the value
                value = self.pop()
                self.push(-value)  # Unary negation
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

            # case I.PROPERTY_ACCESS():
            #     obj = self.pop()
            #     operation = instruction.operation

            #     # Handle array operations
            #     if isinstance(obj, list):
            #         if operation == "Length":
            #             self.push(len(obj))
            #         elif operation == "PushBack":
            #             value = self.pop()
            #             obj.append(value)
            #             self.push(obj)  # Return modified array
            #         elif operation == "PushFront":
            #             value = self.pop()
            #             obj.insert(0, value)
            #             self.push(obj)  # Return modified array
            #         elif operation == "PopBack":
            #             if len(obj) == 0:
            #                 raise IndexError("Cannot PopBack from empty array")
            #             value = obj.pop()  # Pop last element
            #             self.push(value)   # Push the POPPED VALUE
            #         elif operation == "PopFront":
            #             if len(obj) == 0:
            #                 raise IndexError("Cannot PopFront from empty array")
            #             value = obj.pop(0)  # Pop first element
            #             self.push(value)    # Push the POPPED VALUE
            #         elif operation == "Insert":
            #             index = self.pop()
            #             value = self.pop()
            #             if index < 0:
            #                 index = 0
            #             elif index > len(obj):
            #                 index = len(obj)
            #             obj.insert(index, value)
            #             self.push(obj)  # Return modified array
            #         elif operation == "Remove":
            #             index = self.pop()
            #             if 0 <= index < len(obj):
            #                 obj.pop(index)
            #             self.push(obj)  # Return modified array
            #         elif operation == "Clear":
            #             obj.clear()
            #             self.push(obj)  # Return modified array
            #         elif operation == "Slice":
            #             end = self.pop()
            #             start = self.pop()
            #             # Handle optional step parameter if present
            #             if len(self.stack) > 0 and isinstance(self.peek(), int):
            #                 step = self.pop()
            #                 self.push(obj[start:end:step])
            #             else:
            #                 self.push(obj[start:end])
            #         else:
            #             raise ValueError(f"Unknown operation '{operation}' for arrays")
                
            #     # Handle string operations
            #     elif isinstance(obj, str):
            #         if operation == "Length":
            #             self.push(len(obj))
            #         elif operation == "PushBack":
                        # value = self.pop()
                        # self.push(obj + str(value))  # Return new string
            #         elif operation == "PushFront":
            #             value = self.pop()
            #             self.push(str(value) + obj)  # Return new string
            #         elif operation == "PopBack":
            #             if len(obj) == 0:
            #                 raise IndexError("Cannot PopBack from empty string")
            #             last_char = obj[-1]
            #             self.push(obj[:-1])  # Return new string with last char removed
            #         elif operation == "PopFront":
            #             if len(obj) == 0:
            #                 raise IndexError("Cannot PopFront from empty string")
            #             first_char = obj[0]
            #             self.push(obj[1:])  # Return new string with first char removed
            #         elif operation == "Slice":
            #             end = self.pop()
            #             start = self.pop()
            #             # Handle optional step parameter if present
            #             if len(self.stack) > 0 and isinstance(self.peek(), int):
            #                 step = self.pop()
            #                 self.push(obj[start:end:step])
            #             else:
            #                 self.push(obj[start:end])
            #         elif operation == "Clear":
            #             self.push("")  # Return empty string
            #         elif operation == "Insert":
            #             index = self.pop()
            #             value = self.pop()
            #             if index < 0:
            #                 index = 0
            #             elif index > len(obj):
            #                 index = len(obj)
            #             self.push(obj[:index] + str(value) + obj[index:])
            #         elif operation == "Remove":
            #             index = self.pop()
            #             if 0 <= index < len(obj):
            #                 self.push(obj[:index] + obj[index+1:])
            #             else:
            #                 self.push(obj)
            #         else:
            #             raise ValueError(f"Unknown operation '{operation}' for strings")
                
            #     # Handle dictionary operations
            #     elif isinstance(obj, dict):
            #         if operation == "Length":
            #             self.push(len(obj))
            #         elif operation == "Keys":
            #             self.push(list(obj.keys()))
            #         elif operation == "Values":
            #             self.push(list(obj.values()))
            #         elif operation == "Contains":
            #             key = self.pop()
            #             self.push(key in obj)
            #         elif operation == "Add":
            #             key = self.pop()
            #             value = self.pop()
            #             obj[key] = value
            #             self.push(obj)  # Return modified dict
            #         elif operation == "Remove":
            #             key = self.pop()
            #             if key in obj:
            #                 del obj[key]
            #             self.push(obj)  # Return modified dict
            #         elif operation == "Clear":
            #             obj.clear()
            #             self.push(obj)  # Return modified dict
            #         else:
            #             raise ValueError(f"Unknown operation '{operation}' for dictionaries")
                
            #     # Handle other types
            #     else:
            #         raise TypeError(f"Object of type {type(obj).__name__} does not support operation '{operation}'")
                
                # self.ip += 1

            case I.PROPERTY_ACCESS():
                operation = instruction.operation

                if operation == "Length":
                    obj=self.pop()
                    if isinstance(obj, list) or isinstance(obj, str):
                        self.push(len(obj))
                    elif isinstance(obj, dict):
                        self.push(len(obj.keys()))
                
                elif operation == "PushBack":
                    value = self.pop()
                    obj = self.pop()  # Get the array from stack
                    if isinstance(obj, list):
                        obj.append(value)
                        self.push(obj)  # Return modified array
                    elif isinstance(obj, str):
                        self.push(obj + str(value))  # Return new string
                    else:
                        raise TypeError("PushBack requires an array")
                elif operation == "PushFront":
                    value = self.pop()
                    obj = self.pop()  # Get the array from stack
                    if isinstance(obj, list):
                        obj.insert(0, value)
                        self.push(obj)  # Return modified array
                    elif isinstance(obj, str):
                        self.push(str(value) + obj)  # Return new string
                    else:
                        raise TypeError("PushFront requires an array")
                elif operation == "PopBack":
                    obj = self.pop()  # Get the array from stack
                    if isinstance(obj, list):
                        if len(obj) == 0:
                            raise IndexError("Cannot PopBack from empty array")
                        value = obj.pop()  # Pop last element
                        self.push(value)   # Push the POPPED VALUE
                        self.push(obj)  # Push the modified array back
                    elif isinstance(obj, str):
                        if len(obj) == 0:
                            raise IndexError("Cannot PopBack from empty string")
                        last_char = obj[-1]
                        self.push(last_char)
                        self.push(obj[:-1])
                    else:
                        raise TypeError("PopBack requires an array")
                elif operation == "PopFront":
                    obj = self.pop()  # Get the array from stack
                    if isinstance(obj, list):
                        if len(obj) == 0:
                            raise IndexError("Cannot PopFront from empty array")
                        value = obj.pop(0)  # Pop first element
                        self.push(value)    # Push the POPPED VALUE
                        self.push(obj)  # Push the modified array back
                    elif isinstance(obj, str):
                        if len(obj) == 0:
                            raise IndexError("Cannot PopBack from empty string")
                        first_char = obj[0]
                        self.push(first_char)
                        self.push(obj[1:])
                    else:
                        raise TypeError("PopFront requires an array")
                elif operation == "Insert":
                    index = self.pop()
                    value = self.pop()
                    obj = self.pop()  # Get the array from stack
                    if isinstance(obj, list):
                        if index < 0:
                            index = 0
                        elif index > len(obj):
                            index = len(obj)
                        obj.insert(index, value)
                        self.push(obj)  # Return modified array
                    elif isinstance(obj, str):
                        if index < 0:
                            index = 0
                        elif index > len(obj):
                            index = len(obj)
                        self.push(obj[:index] + str(value) + obj[index:])
                    else:
                        raise TypeError("Insert requires an array")
                elif operation == "Remove":
                    index = self.pop()
                    obj = self.pop()  # Get the array from stack
                    if isinstance(obj, list):
                        if 0 <= index < len(obj):
                            obj.pop(index)
                        self.push(obj)  # Return modified array
                    elif isinstance(obj, str):
                        if 0 <= index < len(obj):
                            self.push(obj[:index] + obj[index+1:])
                        else:
                            self.push(obj)
                    else:
                        raise TypeError("Remove requires an array")
                elif operation == "Clear":
                    obj = self.pop()  # Get the array from stack
                    if isinstance(obj, list):
                        obj.clear()
                        self.push(obj)  # Return modified array
                    elif isinstance(obj, str):
                        self.push("")
                    else:
                        raise TypeError("Clear requires an array")
                elif operation == "Slice":
                    # assumed atleast three items on stack
                    start = self.pop()
                    end = self.pop()
                    n3 = self.pop()

                    if type(n3)==int:
                        step = n3
                        obj = self.pop()
                    else:
                        step = None
                        obj = n3
                    if isinstance(obj, list) or isinstance(obj, str):
                        # Handle optional step parameter if present
                        if step:
                            self.push(obj[start:end:step])
                        else:
                            self.push(obj[start:end])
                    else:
                        raise TypeError("Slice requires an array or string")

                # Dictionary Operations
                elif operation == "Keys":
                    obj = self.pop()  # Get the dictionary from stack
                    if isinstance(obj, dict):
                        self.push(list(obj.keys()))
                    else:
                        raise TypeError("Keys requires a dictionary")
                elif operation == "Values":
                    obj = self.pop()  # Get the dictionary from stack
                    if isinstance(obj, dict):
                        self.push(list(obj.values()))
                    else:
                        raise TypeError("Values requires a dictionary")
                elif operation == "Contains":
                    key = self.pop()
                    obj = self.pop()  # Get the dictionary from stack
                    if isinstance(obj, dict):
                        self.push(key in obj)
                    else:
                        raise TypeError("Contains requires a dictionary")
                elif operation == "Add":
                    value = self.pop()
                    key = self.pop()
                    obj = self.pop()  # Get the dictionary from stack
                    if isinstance(obj, dict):
                        obj[key] = value
                        self.push(obj)  # Return modified dict
                    else:
                        raise TypeError("Add requires a dictionary")
                elif operation == "Remove":
                    key = self.pop()
                    obj = self.pop()  # Get the dictionary from stack
                    if isinstance(obj, dict):
                        if key in obj:
                            del obj[key]
                        self.push(obj)  # Return modified dict
                    else:
                        raise TypeError("Remove requires a dictionary")

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
                if type(array)==str:
                    array = array[:index] + value + array[index + 1 :]
                else:
                    array[index] = value
                    self.ip+=1
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

    program = """
fn compute() {
    /> Implementation of Project Euler Problem 14 - Longest Collatz sequence
    
    fn collatz_chain_length(x) {
        /> Create a cache to store already computed lengths
        var hash cache = {};
        
        fn collatz_with_cache(n) {
            /> Base case: if n is 1, the chain length is 1
            if n == 1 then {
                return 1;
            } end;
            
            /> Check if we've already computed this value
            if cache[n] then {
                return cache[n];
            } end;
            
            /> Calculate the next number in the sequence
            var next = 0;
            if n % 2 == 0 then {
                next = n / 2;
            } else {
                next = n * 3 + 1;
            } end;
            
            /> Calculate the chain length and store in cache
            var lengthy = collatz_with_cache(next) + 1;
            cache[n] = lengthy;
            
            return lengthy;
        };
        
        return collatz_with_cache(x);
    };
    
    var max_length = 0;
    var max_number = 0;
    
    /> Loop through all numbers from 1 to 999,999
    for (var i = 1; i < 1000000; i += 1) {
        var lengthy = collatz_chain_length(i);
        /> displayl max_length;
        if lengthy > max_length then {
            max_length = lengthy;
            max_number = i;
        } end;
    };
    
    string(max_number);
};

displayl(compute());

"""
    program ="""
    fn compute() {
    var array triangle = [  /> Mutable
        [75],
        [95,64],
        [17,47,82],
        [18,35,87,10],
        [20, 4,82,47,65],
        [19, 1,23,75, 3,34],
        [88, 2,77,73, 7,63,67],
        [99,65, 4,28, 6,16,70,92],
        [41,41,26,56,83,40,80,70,33],
        [41,48,72,33,47,32,37,16,94,29],
        [53,71,44,65,25,43,91,52,97,51,14],
        [70,11,33,28,77,73,17,78,39,68,17,57],
        [91,71,52,38,17,14,91,43,58,50,27,29,48],
        [63,66, 4,68,89,53,67,30,73,16,69,87,40,31],
        [ 4,62,98,27,23, 9,70,98,73,93,38,53,60, 4,23]
    ];
    
    var integer height = triangle.Length;

    /> Process the triangle from bottom to top
    for (var i = height - 2; i >= 0; i -= 1) {
        var array idx = triangle[i];
        var width = idx.Length ;  /> Get the width of the current row    
           
        for (var j = 0; j < width; j += 1) {
            /> For each position, add the maximum of the two possible paths below
            var integer path1 = triangle[i + 1][j];
            var integer path2 = triangle[i + 1][j + 1];
            
            if (path1 > path2) then {
                triangle[i][j] = triangle[i][j] + path1;
            } else {
                triangle[i][j] = triangle[i][j] + path2;
            } end;
        };
        
    };
    /> The top element now contains the maximum path sum
    return string(triangle[0][0]);
};

displayl(compute());

"""

    program = """
fn foo(){-1;};
displayl foo();
"""

    program = """
fn foo(){
    -1;
};
displayl foo();
"""

    program = """
fn compute() {
    fn edit(a, b) {
        var string adash = a;
        var string bdash = b;
        var integer out = 0;
        for (var integer i = 0; i < adash.Length; i += 1) {
            if (adash[i] != bdash[i]) then {
                out += 1;
            } end;
        };
        return out;
    };
    
    var array strings = ["cat", "cot", "pot", "pat"];
    var integer maxi = 0;
    
    for (var integer i = 0; i < strings.Length; i += 1) {
        for (var integer j = i; j < strings.Length; j += 1) {
            var integer distance = edit(strings[i], strings[j]);
            if (distance > maxi) then {
                maxi = distance;
            } end;
        };
    };
    
    return string(maxi);
};

displayl(compute());
"""

    program = """
    var a = [1,2,3,4,5];
    a.PushFront(0);
    displayl a;
    a.PushBack(6);
    displayl a;
    displayl a.PopFront;
    displayl a[a.Length-1];
    displayl a;
    displayl a.PopBack;
    displayl a;
    displayl a.Length;
    a.Insert(3, 10);
    displayl a;
    a.Remove(1);
    displayl a; 
    a.Clear;
    displayl a;
    displayl a.Length;
"""

    program = """
    var str = \"Code\";
    str.PushBack(\"!\");
    str.PushFront(\"Let's \");
    displayl str;             /> Output: \"Let's Code!\"
    str[6] = \"c\";
    displayl str;             /> Output: \"Let's code!\"
    var slice = str.Slice(6, 10);
    displayl slice;           /> Output: \"code\
"""

    program = """
var a = "ab";
a.PushBack("x");
"""
    program ="""
var a = "ab";
a[0] = "x";
"""

    program = """
    var str = \"Hello, World!\";
    displayl str[0];          /> Access the first character
    str[7] = "w";            /> Modify the 7th index
    displayl str;             /> Display the updated string
"""

    program = """
    var str = \"Code\";
    str.PushBack(\"!\");
    str.PushFront(\"Let's \");
    displayl str;             /> Output: \"Let's Code!\"
    str[6] = \"c\";
    displayl str;             /> Output: \"Let's code!\"
    var slice = str.Slice(6, 10);
    displayl slice;           /> Output: \"code\
"""

    program = """
    var arr = [[1, 2, 3], [4, 5, 6], [7, 8, 9]];
    displayl arr[1][2];
    arr[2][0] = 99;
    displayl arr;
"""

    pprint(list(lex(program)))
    pprint(parse(program, SymbolTable()))
    run_program(program,display_bytecode=True)
    # execute(program)