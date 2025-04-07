from parser import *
from bytecode_gen import *
from typing import Dict, List, Any, Tuple, Optional



class BreakSignal:
    """Signal to break out of a loop."""
    pass


class MoveOnSignal:
    """Signal to continue to the next iteration of a loop."""
    pass


class BytecodeEvaluator:
    def __init__(self):
        self.stack: List[Any] = []
        self.variables: Dict[str, Any] = {}
        self.functions: Dict[str, dict] = {}
        self.instruction_pointer: int = 0
        self.bytecode: List[Any] = []
        self.call_frames: List[dict] = []
        self.loop_depth: int = 0
    
    def load_bytecode(self, bytecode: List[Any]) -> None:
        """Load bytecode to be executed."""
        self.bytecode = bytecode
    
    def execute(self) -> None:
        """Execute the loaded bytecode."""
        self.instruction_pointer = 0
        while self.instruction_pointer < len(self.bytecode):
            opcode = self.bytecode[self.instruction_pointer]
            self.instruction_pointer += 1
            
            if opcode == OpCode.HALT:
                break
            
            try:
                self.handle_opcode(opcode)
            except BreakSignal:
                # Handle break signal by unwinding to the nearest loop
                if self.loop_depth > 0:
                    # The actual unwinding happens in the specific loop handlers
                    # This is just for standalone break statements
                    pass
                else:
                    raise ValueError("Break outside of loop")
            except MoveOnSignal:
                # Handle moveon signal by unwinding to the nearest loop
                if self.loop_depth > 0:
                    # The actual unwinding happens in the specific loop handlers
                    # This is just for standalone moveon statements
                    pass
                else:
                    raise ValueError("MoveOn outside of loop")
    
    def handle_opcode(self, opcode: OpCode) -> None:
        """Dispatch to the appropriate handler based on opcode."""
        if opcode == OpCode.PUSH:
            self.handle_push()
        elif opcode == OpCode.POP:
            self.stack.pop()
        elif opcode == OpCode.ADD:
            right = self.stack.pop()
            left = self.stack.pop()
            self.stack.append(left + right)
        elif opcode == OpCode.SUB:
            right = self.stack.pop()
            left = self.stack.pop()
            self.stack.append(left - right)
        elif opcode == OpCode.MUL:
            right = self.stack.pop()
            left = self.stack.pop()
            self.stack.append(left * right)
        elif opcode == OpCode.DIV:
            right = self.stack.pop()
            left = self.stack.pop()
            self.stack.append(left / right)
        elif opcode == OpCode.MOD:
            right = self.stack.pop()
            left = self.stack.pop()
            self.stack.append(left % right)
        elif opcode == OpCode.POW:
            right = self.stack.pop()
            left = self.stack.pop()
            self.stack.append(left ** right)
        elif opcode == OpCode.LT:
            right = self.stack.pop()
            left = self.stack.pop()
            self.stack.append(left < right)
        elif opcode == OpCode.GT:
            right = self.stack.pop()
            left = self.stack.pop()
            self.stack.append(left > right)
        elif opcode == OpCode.EQ:
            right = self.stack.pop()
            left = self.stack.pop()
            self.stack.append(left == right)
        elif opcode == OpCode.NEQ:
            right = self.stack.pop()
            left = self.stack.pop()
            self.stack.append(left != right)
        elif opcode == OpCode.LE:
            right = self.stack.pop()
            left = self.stack.pop()
            self.stack.append(left <= right)
        elif opcode == OpCode.GE:
            right = self.stack.pop()
            left = self.stack.pop()
            self.stack.append(left >= right)
        elif opcode == OpCode.AND:
            right = self.stack.pop()
            left = self.stack.pop()
            self.stack.append(left and right)
        elif opcode == OpCode.OR:
            right = self.stack.pop()
            left = self.stack.pop()
            self.stack.append(left or right)
        elif opcode == OpCode.BAND:
            right = self.stack.pop()
            left = self.stack.pop()
            self.stack.append(left & right)
        elif opcode == OpCode.BOR:
            right = self.stack.pop()
            left = self.stack.pop()
            self.stack.append(left | right)
        elif opcode == OpCode.BXOR:
            right = self.stack.pop()
            left = self.stack.pop()
            self.stack.append(left ^ right)
        elif opcode == OpCode.SHL:
            right = self.stack.pop()
            left = self.stack.pop()
            self.stack.append(left << right)
        elif opcode == OpCode.SHR:
            right = self.stack.pop()
            left = self.stack.pop()
            self.stack.append(left >> right)
        elif opcode == OpCode.NOT:
            value = self.stack.pop()
            self.stack.append(not value)
        elif opcode == OpCode.BNOT:
            value = self.stack.pop()
            self.stack.append(~value)
        elif opcode == OpCode.ASCII:
            value = self.stack.pop()
            self.stack.append(ord(value))
        elif opcode == OpCode.CHAR:
            value = self.stack.pop()
            self.stack.append(chr(value))
        elif opcode == OpCode.VARBIND:
            self.handle_varbind()
        elif opcode == OpCode.DISPLAY:
            value = self.stack.pop()
            print(value, end="")
        elif opcode == OpCode.DISPLAYL:
            value = self.stack.pop()
            print(value)
        elif opcode == OpCode.ASSIGN:
            self.handle_assign()
        elif opcode == OpCode.CALLARRAY:
            self.handle_callarray()
        elif opcode == OpCode.PUSHFRONT:
            self.handle_pushfront()
        elif opcode == OpCode.PUSHBACK:
            self.handle_pushback()
        elif opcode == OpCode.POPFRONT:
            self.handle_popfront()
        elif opcode == OpCode.POPBACK:
            self.handle_popback()
        elif opcode == OpCode.ASSIGNTOARRAY:
            self.handle_assigntoarray()
        elif opcode == OpCode.CALLHASHVAL:
            self.handle_callhashval()
        elif opcode == OpCode.ADDHASHPAIR:
            self.handle_addhashpair()
        elif opcode == OpCode.REMOVEHASHPAIR:
            self.handle_removehashpair()
        elif opcode == OpCode.ASSIGNHASHVAL:
            self.handle_assignhashval()
        elif opcode == OpCode.ASSIGNFULLARRAY:
            self.handle_assignfullarray()
        elif opcode == OpCode.INSERTAT:
            self.handle_insertat()
        elif opcode == OpCode.REMOVEAT:
            self.handle_removeat()
        elif opcode == OpCode.GETLENGTH:
            self.handle_getlength()
        elif opcode == OpCode.CLEARARRAY:
            self.handle_cleararray()
        elif opcode == OpCode.JUMP:
            self.handle_jump()
        elif opcode == OpCode.JUMP_IF_TRUE:
            self.handle_jump_if_true()
        elif opcode == OpCode.JUMP_IF_FALSE:
            self.handle_jump_if_false()
        elif opcode == OpCode.FEED:
            self.handle_feed()
        elif opcode == OpCode.FUNC_DEF:
            self.handle_func_def()
        elif opcode == OpCode.FUNC_CALL:
            self.handle_func_call()
        elif opcode == OpCode.RETURN:
            self.handle_return()
        elif opcode == OpCode.BREAK:
            self.handle_break()
        elif opcode == OpCode.MOVEON:
            self.handle_moveon()
        elif opcode == OpCode.COMPOUND_ASSIGN:
            self.handle_compound_assign()
        else:
            raise ValueError(f"Unknown opcode: {opcode}")
    
    def read_string(self) -> str:
        """Read a string from bytecode at current instruction pointer."""
        length = self.bytecode[self.instruction_pointer]
        self.instruction_pointer += 1
        
        bytes_data = self.bytecode[self.instruction_pointer:self.instruction_pointer + length]
        self.instruction_pointer += length
        
        return ''.join(chr(b) for b in bytes_data)
    
    # Opcode handlers
    def handle_push(self) -> None:
        """Handle PUSH opcode - push a value onto the stack."""
        length = self.bytecode[self.instruction_pointer]
        self.instruction_pointer += 1
        
        if length == 1:
            # Single integer value
            value = self.bytecode[self.instruction_pointer]
            self.instruction_pointer += 1
            # Handle negative numbers by using signed bytes
            if value > 127:  # Assuming it's signed
                value = value - 256
            self.stack.append(value)
        else:
            # String or complex value
            bytes_data = self.bytecode[self.instruction_pointer:self.instruction_pointer + length]
            self.instruction_pointer += length
            
            try:
                # Try to convert to a string
                string_value = ''.join(chr(b) for b in bytes_data)
                self.stack.append(string_value)
            except:
                # If not a valid string, use raw bytes
                self.stack.append(bytes_data)
    
    def handle_varbind(self) -> None:
        """Handle VARBIND opcode - bind value to variable name."""
        var_name = self.read_string()
        value = self.stack.pop()
        self.variables[var_name] = value
    
    def handle_assign(self) -> None:
        """Handle ASSIGN opcode - assign value to existing variable."""
        var_name = self.read_string()
        value = self.stack.pop()
        
        if var_name not in self.variables:
            raise ValueError(f"Variable '{var_name}' not defined")
        
        self.variables[var_name] = value
    
    def handle_compound_assign(self) -> None:
        """Handle COMPOUND_ASSIGN opcode - compound assignment (+=, -=, etc)."""
        var_name = self.read_string()
        op = self.read_string()
        value = self.stack.pop()
        
        if var_name not in self.variables:
            raise ValueError(f"Variable '{var_name}' not defined")
        
        current_value = self.variables[var_name]
        
        if op == "+":
            self.variables[var_name] = current_value + value
        elif op == "-":
            self.variables[var_name] = current_value - value
        elif op == "*":
            self.variables[var_name] = current_value * value
        elif op == "/":
            self.variables[var_name] = current_value / value
        elif op == "%":
            self.variables[var_name] = current_value % value
        elif op == "^":
            self.variables[var_name] = current_value ** value
        elif op == "&":
            self.variables[var_name] = current_value & value
        elif op == "|":
            self.variables[var_name] = current_value | value
        elif op == "<<":
            self.variables[var_name] = current_value << value
        elif op == ">>":
            self.variables[var_name] = current_value >> value
        else:
            raise ValueError(f"Unknown compound assignment operator: {op}")
    
    def handle_callarray(self) -> None:
        """Handle CALLARRAY opcode - get array element."""
        index = self.stack.pop()
        array_name = self.stack.pop()
        
        if array_name not in self.variables:
            raise ValueError(f"Array '{array_name}' not defined")
        
        array = self.variables[array_name]
        if not isinstance(array, list):
            raise TypeError(f"'{array_name}' is not an array")
            
        if 0 <= index < len(array):
            self.stack.append(array[index])
        else:
            raise IndexError(f"Index {index} out of bounds for array '{array_name}'")
    
    def handle_pushfront(self) -> None:
        """Handle PUSHFRONT opcode - insert element at front of array."""
        value = self.stack.pop()
        array_name = self.stack.pop()
        
        if array_name not in self.variables:
            raise ValueError(f"Array '{array_name}' not defined")
        
        array = self.variables[array_name]
        if not isinstance(array, list):
            raise TypeError(f"'{array_name}' is not an array")
            
        array.insert(0, value)
    
    def handle_pushback(self) -> None:
        """Handle PUSHBACK opcode - add element to end of array."""
        value = self.stack.pop()
        array_name = self.stack.pop()
        
        if array_name not in self.variables:
            raise ValueError(f"Array '{array_name}' not defined")
        
        array = self.variables[array_name]
        if not isinstance(array, list):
            raise TypeError(f"'{array_name}' is not an array")
            
        array.append(value)
    
    def handle_popfront(self) -> None:
        """Handle POPFRONT opcode - remove element from front of array."""
        array_name = self.stack.pop()
        
        if array_name not in self.variables:
            raise ValueError(f"Array '{array_name}' not defined")
        
        array = self.variables[array_name]
        if not isinstance(array, list):
            raise TypeError(f"'{array_name}' is not an array")
        
        if not array:
            raise ValueError(f"Cannot pop from empty array '{array_name}'")
        
        value = array.pop(0)
        self.stack.append(value)
    
    def handle_popback(self) -> None:
        """Handle POPBACK opcode - remove element from end of array."""
        array_name = self.stack.pop()
        
        if array_name not in self.variables:
            raise ValueError(f"Array '{array_name}' not defined")
        
        array = self.variables[array_name]
        if not isinstance(array, list):
            raise TypeError(f"'{array_name}' is not an array")
        
        if not array:
            raise ValueError(f"Cannot pop from empty array '{array_name}'")
        
        value = array.pop()
        self.stack.append(value)
    
    def handle_assigntoarray(self) -> None:
        """Handle ASSIGNTOARRAY opcode - assign value to array element."""
        value = self.stack.pop()
        index = self.stack.pop()
        array_name = self.stack.pop()
        
        if array_name not in self.variables:
            raise ValueError(f"Array '{array_name}' not defined")
        
        array = self.variables[array_name]
        if not isinstance(array, list):
            raise TypeError(f"'{array_name}' is not an array")
        
        if 0 <= index < len(array):
            array[index] = value
        else:
            raise IndexError(f"Index {index} out of bounds for array '{array_name}'")
    
    def handle_callhashval(self) -> None:
        """Handle CALLHASHVAL opcode - get value from hash by key."""
        key = self.stack.pop()
        hash_name = self.stack.pop()
        
        if hash_name not in self.variables:
            raise ValueError(f"Hash '{hash_name}' not defined")
        
        hash_map = self.variables[hash_name]
        if not isinstance(hash_map, dict):
            raise TypeError(f"'{hash_name}' is not a hash map")
        
        if key not in hash_map:
            raise KeyError(f"Key '{key}' not found in hash '{hash_name}'")
            
        self.stack.append(hash_map[key])
    
    def handle_addhashpair(self) -> None:
        """Handle ADDHASHPAIR opcode - add key-value pair to hash."""
        value = self.stack.pop()
        key = self.stack.pop()
        hash_name = self.stack.pop()
        
        if hash_name not in self.variables:
            raise ValueError(f"Hash '{hash_name}' not defined")
        
        hash_map = self.variables[hash_name]
        if not isinstance(hash_map, dict):
            raise TypeError(f"'{hash_name}' is not a hash map")
            
        hash_map[key] = value
    
    def handle_removehashpair(self) -> None:
        """Handle REMOVEHASHPAIR opcode - remove key from hash."""
        key = self.stack.pop()
        hash_name = self.stack.pop()
        
        if hash_name not in self.variables:
            raise ValueError(f"Hash '{hash_name}' not defined")
        
        hash_map = self.variables[hash_name]
        if not isinstance(hash_map, dict):
            raise TypeError(f"'{hash_name}' is not a hash map")
        
        if key not in hash_map:
            raise KeyError(f"Key '{key}' not found in hash '{hash_name}'")
            
        del hash_map[key]
    
    def handle_assignhashval(self) -> None:
        """Handle ASSIGNHASHVAL opcode - update value in hash by key."""
        value = self.stack.pop()
        key = self.stack.pop()
        hash_name = self.stack.pop()
        
        if hash_name not in self.variables:
            raise ValueError(f"Hash '{hash_name}' not defined")
        
        hash_map = self.variables[hash_name]
        if not isinstance(hash_map, dict):
            raise TypeError(f"'{hash_name}' is not a hash map")
            
        hash_map[key] = value
    
    def handle_assignfullarray(self) -> None:
        """Handle ASSIGNFULLARRAY opcode - assign entire array."""
        length = self.stack.pop()
        array = []
        
        for _ in range(length):
            array.insert(0, self.stack.pop())
        
        array_name = self.stack.pop()
        self.variables[array_name] = array
    
    def handle_insertat(self) -> None:
        """Handle INSERTAT opcode - insert element at specific array index."""
        value = self.stack.pop()
        index = self.stack.pop()
        array_name = self.stack.pop()
        
        if array_name not in self.variables:
            raise ValueError(f"Array '{array_name}' not defined")
        
        array = self.variables[array_name]
        if not isinstance(array, list):
            raise TypeError(f"'{array_name}' is not an array")
            
        if 0 <= index <= len(array):
            array.insert(index, value)
        else:
            raise IndexError(f"Index {index} out of bounds for array '{array_name}'")
    
    def handle_removeat(self) -> None:
        """Handle REMOVEAT opcode - remove element at specific array index."""
        index = self.stack.pop()
        array_name = self.stack.pop()
        
        if array_name not in self.variables:
            raise ValueError(f"Array '{array_name}' not defined")
        
        array = self.variables[array_name]
        if not isinstance(array, list):
            raise TypeError(f"'{array_name}' is not an array")
        
        if 0 <= index < len(array):
            value = array.pop(index)
            self.stack.append(value)
        else:
            raise IndexError(f"Index {index} out of bounds for array '{array_name}'")
    
    def handle_getlength(self) -> None:
        """Handle GETLENGTH opcode - get length of array or hash."""
        container_name = self.stack.pop()
        
        if container_name not in self.variables:
            raise ValueError(f"Container '{container_name}' not defined")
        
        container = self.variables[container_name]
        if not isinstance(container, (list, dict, str)):
            raise TypeError(f"Cannot get length of '{container_name}': not a container type")
            
        self.stack.append(len(container))
    
    def handle_cleararray(self) -> None:
        """Handle CLEARARRAY opcode - empty an array."""
        array_name = self.stack.pop()
        
        if array_name not in self.variables:
            raise ValueError(f"Array '{array_name}' not defined")
        
        array = self.variables[array_name]
        if not isinstance(array, list):
            raise TypeError(f"'{array_name}' is not an array")
            
        array.clear()
    
    def handle_jump(self) -> None:
        """Handle JUMP opcode - unconditional jump."""
        offset = self.bytecode[self.instruction_pointer]
        self.instruction_pointer += 1
        self.instruction_pointer += offset
    
    def handle_jump_if_true(self) -> None:
        """Handle JUMP_IF_TRUE opcode - conditional jump if true."""
        offset = self.bytecode[self.instruction_pointer]
        self.instruction_pointer += 1
        
        condition = self.stack.pop()
        
        if condition:
            self.instruction_pointer += offset
    
    def handle_jump_if_false(self) -> None:
        """Handle JUMP_IF_FALSE opcode - conditional jump if false."""
        offset = self.bytecode[self.instruction_pointer]
        self.instruction_pointer += 1
        
        condition = self.stack.pop()
        
        if not condition:
            self.instruction_pointer += offset
    
    def handle_feed(self) -> None:
        """Handle FEED opcode - get user input."""
        prompt = self.stack.pop()
        user_input = input(prompt)
        self.stack.append(user_input)
    
    def handle_func_def(self) -> None:
        """Handle FUNC_DEF opcode - define a function."""
        func_name = self.read_string()
        
        func_address = self.bytecode[self.instruction_pointer]
        self.instruction_pointer += 1
        
        num_params = self.bytecode[self.instruction_pointer]
        self.instruction_pointer += 1
        
        is_recursive = bool(self.bytecode[self.instruction_pointer])
        self.instruction_pointer += 1
        
        self.functions[func_name] = {
            'address': func_address,
            'num_params': num_params,
            'is_recursive': is_recursive
        }
    
    def handle_func_call(self) -> None:
        """Handle FUNC_CALL opcode - call a function."""
        func_name = self.read_string()
        num_args = self.bytecode[self.instruction_pointer]
        self.instruction_pointer += 1
        
        if func_name not in self.functions:
            raise ValueError(f"Function '{func_name}' not defined")
        
        func_info = self.functions[func_name]
        
        if num_args != func_info['num_params']:
            raise ValueError(f"Function '{func_name}' expects {func_info['num_params']} arguments, got {num_args}")
        
        # Get arguments in reverse order (since they were pushed in reverse)
        args = []
        for _ in range(num_args):
            args.insert(0, self.stack.pop())
        
        # Save current state
        self.call_frames.append({
            'return_addr': self.instruction_pointer,
            'local_vars': {},
            'prev_vars': dict(self.variables)  # Save a copy of current variables
        })
        
        # Set up function parameters
        param_names = ["a", "b", "c", "d", "e", "f", "g", "h"][:func_info['num_params']]
        
        # Store local variables
        local_vars = {}
        for i, arg in enumerate(args):
            if i < len(param_names):
                param_name = param_names[i]
                local_vars[param_name] = arg
                self.variables[param_name] = arg
        
        self.call_frames[-1]['local_vars'] = local_vars
        
        # Jump to function body
        self.instruction_pointer = func_info['address']
    
    def handle_return(self) -> None:
        """Handle RETURN opcode - return from function."""
        if not self.call_frames:
            raise ValueError("Return without function call")
        
        # Get return value if any (it should be on top of the stack)
        return_value = None
        if self.stack:
            return_value = self.stack[-1]  # Don't pop yet, it's the return value
        
        # Restore state
        call_frame = self.call_frames.pop()
        
        # Restore variables but keep the return value
        self.variables = call_frame['prev_vars']
        
        # Restore instruction pointer
        self.instruction_pointer = call_frame['return_addr']
    
    def handle_break(self) -> None:
        """Handle BREAK opcode - break from loop."""
        raise BreakSignal()
    
    def handle_moveon(self) -> None:
        """Handle MOVEON opcode - continue to next loop iteration."""
        raise MoveOnSignal()


def execute_bytecode(bytecode):
    """Execute bytecode with the evaluator."""
    evaluator = BytecodeEvaluator()
    evaluator.load_bytecode(bytecode)
    evaluator.execute()
    return evaluator
