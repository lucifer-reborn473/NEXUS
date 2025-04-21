from parser import *
from dataclasses import dataclass

class Label:
    def __init__(self, target=-1):
        self.target = target

# Define instruction classes in a nested structure
class I:
    # Stack operations
    class PUSH:
        def __init__(self, value):
            self.value = value
    
    class POP:
        pass
    
    class DUP:
        pass
    
    # Arithmetic operations
    class ADD:
        pass
    
    class SUB:
        pass
    
    class MUL:
        pass
    
    class DIV:
        pass
    
    class MODULO:
        pass
    
    class POW:
        pass
        
    class UPLUS:
        pass

    class UMINUS:
        pass

    # Comparison operations
    class EQ:
        pass
    
    class NE:
        pass
    
    class LT:
        pass
    
    class GT:
        pass
    
    class LE:
        pass
    
    class GE:
        pass
    
    # Logical operations
    class AND:
        pass
    
    class OR:
        pass
    
    class NOT:
        pass
    
    # Bitwise operations
    class BITAND:
        pass
    
    class BITOR:
        pass
    
    class BITXOR:
        pass
    
    class BITNOT:
        pass
    
    class LSHIFT:
        pass
    
    class RSHIFT:
        pass
    
    # Control flow
    class JMP:
        def __init__(self, label):
            self.label = label
    
    class JMP_IF_TRUE:
        def __init__(self, label):
            self.label = label
    
    class JMP_IF_FALSE:
        def __init__(self, label):
            self.label = label

    class PUSH_SCOPE:
        pass
    
    class POP_SCOPE:
        pass
    # Variable operations
    class LOAD:
        def __init__(self, name):
            self.name = name
    
    class STORE:
        def __init__(self, name):
            self.name = name
    
    # Function operations
    class CALL:
        def __init__(self, name):
            self.name = name
    
    class RETURN:
        pass
    
    class PUSHFN:
        def __init__(self, label, name):
            self.label = label
            self.name = name
    
    # String
    class STRING_INDEX_ASSIGN:
        pass

    # Array/collection operations
    class MAKE_ARRAY:
        def __init__(self, size):
            self.size = size
    
    class MAKE_HASH:
        def __init__(self, size):
            self.size = size
    
    class ARRAY_GET:
        pass
    
    class ARRAY_SET:
        pass
    
    class HASH_GET:
        pass
    
    class HASH_SET:
        pass
    
    class PROPERTY_ACCESS:
        def __init__(self, operation):
            self.operation = operation

    # I/O operations
    class PRINT:
        pass
    
    class PRINTLN:
        pass
    
    class INPUT:
        pass
    
    # Other operations
    class TYPECAST:
        def __init__(self, dtype):
            self.dtype = dtype
    
    class HALT:
        pass

class ByteCode:
    def __init__(self):
        self.insns = []
    
    def label(self):
        return Label()
    
    def emit(self, instruction):
        self.insns.append(instruction)
        return instruction
    
    def emit_label(self, label):
        label.target = len(self.insns)
    
    def print_bytecode(self):
        # pprint(self.insns)
        for i, insn in enumerate(self.insns):
            match insn:
                case I.JMP():
                    print(f"{i:=4} {'JMP':<15} target = {insn.label.target}")
                case I.JMP_IF_TRUE():
                    print(f"{i:=4} {'JMP_IF_TRUE':<15} target = {insn.label.target}")
                case I.JMP_IF_FALSE():
                    print(f"{i:=4} {'JMP_IF_FALSE':<15} target = {insn.label.target}")
                case I.LOAD():
                    print(f"{i:=4} {'LOAD':<15} name = {insn.name}")
                case I.STORE():
                    print(f"{i:=4} {'STORE':<15} name = {insn.name}")
                case I.CALL():
                    print(f"{i:=4} {'CALL':<15} name = {insn.name}")
                case I.PUSH():
                    print(f"{i:=4} {'PUSH':<15} value = {insn.value}")
                case I.PUSHFN():
                    print(f"{i:=4} {'PUSHFN':<15} target = {insn.label.target}, name = {insn.name}")
                case I.PROPERTY_ACCESS():
                    print(f"{i:=4} {'PROPERTY_ACCESS':<15} operation = {insn.operation}")
                case I.MAKE_ARRAY():
                    print(f"{i:=4} {'MAKE_ARRAY':<15} size = {insn.size}")
                case I.MAKE_HASH():
                    print(f"{i:=4} {'MAKE_HASH':<15} size = {insn.size}")
                case I.TYPECAST():
                    print(f"{i:=4} {'TYPECAST':<15} type = {insn.dtype}")
                case _:
                    print(f"{i:=4} {insn.__class__.__name__:<15}")

def codegen(ast_node):
    code = ByteCode()
    generate_bytecode(ast_node, code)
    code.emit(I.HALT())
    return code

def generate_bytecode(node, code):
    match node:
        # Basic values
        case Number(n):
            if '.' in n:
                code.emit(I.PUSH(float(n)))
            else:
                code.emit(I.PUSH(int(n)))

        case String(s):
            code.emit(I.PUSH(s))
        
        case Boolean(b):
            code.emit(I.PUSH(b))
        
        case Variable(var_name):
            code.emit(I.LOAD(var_name))
        
        # Binary operations
        case BinOp(op, left, right):
            generate_bytecode(left, code)
            generate_bytecode(right, code)
            
            match op:
                case "+": code.emit(I.ADD())
                case "-": code.emit(I.SUB())
                case "*": code.emit(I.MUL())
                case "/" | "÷": code.emit(I.DIV())
                case "**": code.emit(I.POW())
                case "%": code.emit(I.MODULO())
                case "<": code.emit(I.LT())
                case ">": code.emit(I.GT())
                case "==": code.emit(I.EQ())
                case "!=": code.emit(I.NE())
                case "<=": code.emit(I.LE())
                case ">=": code.emit(I.GE())
                case "and": code.emit(I.AND())
                case "or": code.emit(I.OR())
                case "&": code.emit(I.BITAND())
                case "|": code.emit(I.BITOR())
                case "^": code.emit(I.BITXOR())
                case "<<": code.emit(I.LSHIFT())
                case ">>": code.emit(I.RSHIFT())
        
        # Unary operations
        case UnaryOp(op, val):
            generate_bytecode(val, code)
            match op:
                case "+": code.emit(I.UPLUS())
                case "-": code.emit(I.UMINUS())
                case "~": code.emit(I.BITNOT())
                case "not" | "!": code.emit(I.NOT())
                case "ascii":
                    code.emit(I.CALL("ascii"))
                case "char":
                    code.emit(I.CALL("char"))
        
        # Variable binding and assignment
        case VarBind(name, dtype, value, _):
            generate_bytecode(value, code)
            if dtype:
                code.emit(I.TYPECAST(dtype))
            code.emit(I.STORE(name))
        
        case UpdateVar(var_name, value):
            generate_bytecode(value, code)
            code.emit(I.STORE(var_name))
        
        case AssignStringVal(var_name, index, value):
            code.emit(I.LOAD(var_name))
            generate_bytecode(index, code)
            generate_bytecode(value, code)
            code.emit(I.CALL("string_set"))
            code.emit(I.STORE(var_name))

        case CompoundAssignment(var_name, op, value):
            code.emit(I.LOAD(var_name))
            generate_bytecode(value, code)
            
            match op[0]:
                case "+": code.emit(I.ADD())
                case "-": code.emit(I.SUB())
                case "*": code.emit(I.MUL())
                case "/": code.emit(I.DIV())
                case "%": code.emit(I.MODULO())
                
            code.emit(I.STORE(var_name))
        
# PROPERTY_ACCESS handling in bytecode_gen_new.py

        case PropertyAccess(var_name, operation, args):
            # Load the variable
            code.emit(I.LOAD(var_name))
            
            # Generate code for arguments in reverse order (stack order)
            for arg in reversed(args):
                generate_bytecode(arg, code)
            
            # Emit property access instruction with operation name
            code.emit(I.PROPERTY_ACCESS(operation))
            
            # Store back only for operations that modify the original object in-place
            # Arrays: PushBack, PushFront, Clear, Insert, Remove
            # Strings: NEVER store back (strings are immutable in Python)
            # Hashes: Add, Remove, Clear
            
            if operation in ["PopFront","PopBack","PushBack", "PushFront", "Clear", "Insert", "Remove", "Add"] and var_name != "":
                # For string operations, we never store back - they return new strings
                # Check we're not dealing with a temporary result with no name
                code.emit(I.STORE(var_name))

        # Array operations
        case Array(elements):
            for element in elements:
                generate_bytecode(element, code)
            code.emit(I.MAKE_ARRAY(len(elements)))
        
        case CallArr(array_name, indices):
            code.emit(I.LOAD(array_name))
            for index in indices:
                generate_bytecode(index, code)
                code.emit(I.ARRAY_GET())
        
        case AssigntoArr(array_name, indices, value):
            code.emit(I.LOAD(array_name))
            for i, index in enumerate(indices[:-1]):
                generate_bytecode(index, code)
                code.emit(I.ARRAY_GET())
            generate_bytecode(indices[-1], code)
            generate_bytecode(value, code)
            code.emit(I.ARRAY_SET())
            code.emit(I.STORE(array_name))
        
        # Hash operations
        case Hash(pairs):
            for key, value in pairs:
                generate_bytecode(key, code)
                generate_bytecode(value, code)
            code.emit(I.MAKE_HASH(len(pairs)))
        
        case CallHashVal(hash_name, keys):
            code.emit(I.LOAD(hash_name))
            for key in keys:
                generate_bytecode(key, code)
                code.emit(I.HASH_GET())
        
        case AssignHashVal(hash_name, keys, new_val):
            code.emit(I.LOAD(hash_name))
            for key in keys[:-1]:
                generate_bytecode(key, code)
                code.emit(I.HASH_GET())
            generate_bytecode(keys[-1], code)
            generate_bytecode(new_val, code)
            code.emit(I.HASH_SET())
        case AddHashPair(hash_name, key, val):
            code.emit(I.LOAD(hash_name))
            generate_bytecode(key, code)
            generate_bytecode(val, code)
            code.emit(I.HASH_SET())
            code.emit(I.STORE(hash_name))
        case RemoveHashPair(hash_name, key):
            code.emit(I.LOAD(hash_name))
            generate_bytecode(key, code)
            code.emit(I.CALL("hash_remove"))
            code.emit(I.STORE(hash_name))
        case InsertAt(arr_name, index, value):
            code.emit(I.LOAD(arr_name))
            code.emit(I.DUP())  # Duplicate for type check
            code.emit(I.CALL("type_check"))
            code.emit(I.JMP_IF_TRUE(skip_label := code.label()))
            
            # String handling (if not array)
            generate_bytecode(index, code)
            generate_bytecode(value, code)
            code.emit(I.CALL("string_insert"))
            code.emit(I.STORE(arr_name))
            code.emit(I.JMP(end_label := code.label()))
            
            # Array handling
            code.emit_label(skip_label)
            generate_bytecode(index, code)
            generate_bytecode(value, code)
            code.emit(I.CALL("array_insert"))
            code.emit(I.STORE(arr_name))
            
            code.emit_label(end_label)

        case RemoveAt(arr_name, index):
            code.emit(I.LOAD(arr_name))
            code.emit(I.DUP())  # Duplicate for type check
            code.emit(I.CALL("type_check"))
            code.emit(I.JMP_IF_TRUE(skip_label := code.label()))
            
            # String handling (if not array)
            generate_bytecode(index, code)
            code.emit(I.CALL("string_remove_at"))
            code.emit(I.STORE(arr_name))
            code.emit(I.JMP(end_label := code.label()))
            
            # Array handling
            code.emit_label(skip_label)
            generate_bytecode(index, code)
            code.emit(I.CALL("array_remove"))
            code.emit(I.STORE(arr_name))
            
            code.emit_label(end_label)

        case ClearArray(arr_name):
            code.emit(I.LOAD(arr_name))
            code.emit(I.DUP())  # Duplicate for type check
            code.emit(I.CALL("type_check"))
            code.emit(I.JMP_IF_TRUE(skip_label := code.label()))
            
            # String handling (clear to empty string)
            code.emit(I.PUSH(""))
            code.emit(I.STORE(arr_name))
            code.emit(I.JMP(end_label := code.label()))
            
            # Array handling (clear to empty array)
            code.emit_label(skip_label)
            code.emit(I.CALL("array_clear"))
            code.emit(I.STORE(arr_name))
            
            code.emit_label(end_label)

        case Sort(arr_name, greater):
            code.emit(I.LOAD(arr_name))
            if greater:
                generate_bytecode(greater, code)
                code.emit(I.CALL("array_sort_with_comparator"))
            else:
                code.emit(I.CALL("array_sort"))
            code.emit(I.STORE(arr_name))

        case BreakOut():
            # Find the nearest loop end label and jump to it
            if hasattr(code, 'loop_end_labels') and code.loop_end_labels:
                code.emit(I.JMP(code.loop_end_labels[-1]))
            else:
                raise ValueError("BreakOut statement outside of loop")

        case MoveOn():
            # Find the nearest loop start label and jump to it
            if hasattr(code, 'loop_start_labels') and code.loop_start_labels:
                code.emit(I.JMP(code.loop_start_labels[-1]))
            else:
                raise ValueError("MoveOn statement outside of loop")

        case Return(value):
            # Generate code for the return value
            generate_bytecode(value, code)
            # Emit return instruction
            code.emit(I.RETURN())

        # Control structures
        case If(cond, then_body, else_body, _):
            end_label = code.label()
            else_label = code.label()
            
            generate_bytecode(cond, code)
            code.emit(I.JMP_IF_FALSE(else_label))
            
            # Check if then_body is a Statements object containing a Return
            if isinstance(then_body, Statements):
                for stmt in then_body.statements:
                    generate_bytecode(stmt, code)
                    # If this statement is a Return, don't emit a JMP
                    if isinstance(stmt, Return):
                        break
            else:
                generate_bytecode(then_body, code)
            
            # Only emit JMP if the then_body doesn't end with a Return
            if not (isinstance(then_body, Statements) and 
                    then_body.statements and 
                    isinstance(then_body.statements[-1], Return)):
                code.emit(I.JMP(end_label))
            
            code.emit_label(else_label)
            if else_body:
                generate_bytecode(else_body, code)
            
            code.emit_label(end_label)

        case Repeat(times, body, _):
            # Prepare loop labels
            if not hasattr(code, 'loop_start_labels'):
                code.loop_start_labels = []
            if not hasattr(code, 'loop_end_labels'):
                code.loop_end_labels = []
            
            # Setup counter and limits
            counter_var = f"__repeat_counter_{len(code.insns)}"
            code.emit(I.PUSH(0))
            code.emit(I.STORE(counter_var))
            
            # Evaluate the number of repetitions
            generate_bytecode(times, code)
            code.emit(I.STORE("__repeat_limit"))
            
            # Loop start
            start_label = code.label()
            end_label = code.label()
            
            # Remember these labels for break/continue
            code.loop_start_labels.append(start_label)
            code.loop_end_labels.append(end_label)
            
            code.emit_label(start_label)
            
            # Check if counter < limit
            code.emit(I.LOAD(counter_var))
            code.emit(I.LOAD("__repeat_limit"))
            code.emit(I.LT())
            code.emit(I.JMP_IF_FALSE(end_label))
            
            # Execute body
            generate_bytecode(body, code)
            
            # Increment counter
            code.emit(I.LOAD(counter_var))
            code.emit(I.PUSH(1))
            code.emit(I.ADD())
            code.emit(I.STORE(counter_var))
            
            # Loop back
            code.emit(I.JMP(start_label))
            
            # Loop end
            code.emit_label(end_label)
            
            # Remove these labels from the tracking stacks
            code.loop_start_labels.pop()
            code.loop_end_labels.pop()

        case WhileLoop(cond, body, _):
            if not hasattr(code, 'loop_start_labels'):
                code.loop_start_labels = []
            if not hasattr(code, 'loop_end_labels'):
                code.loop_end_labels = []
            
            start_label = code.label()
            end_label = code.label()
            
            # Track labels for break/continue
            code.loop_start_labels.append(start_label)
            code.loop_end_labels.append(end_label)
            
            code.emit_label(start_label)
            generate_bytecode(cond, code)
            code.emit(I.JMP_IF_FALSE(end_label))
            
            generate_bytecode(body, code)
            code.emit(I.JMP(start_label))
            
            code.emit_label(end_label)
            
            # Remove these labels from the tracking stacks
            code.loop_start_labels.pop()
            code.loop_end_labels.pop()

        case ForLoop(init, cond, incr, body, loop_scope):
            if not hasattr(code, 'loop_start_labels'):
                code.loop_start_labels = []
            if not hasattr(code, 'loop_end_labels'):
                code.loop_end_labels = []
            
            start_label = code.label()
            end_label = code.label()
            incr_label = code.label()
            
            # Track labels for break/continue
            code.loop_start_labels.append(incr_label) # Continue jumps to increment
            code.loop_end_labels.append(end_label) # Break jumps to end
            
            # Create a new scope for the loop
            # code.emit(I.PUSH_SCOPE())
            
            generate_bytecode(init, code)
            code.emit_label(start_label)
            generate_bytecode(cond, code)
            code.emit(I.JMP_IF_FALSE(end_label))
            generate_bytecode(body, code)
            code.emit_label(incr_label)
            generate_bytecode(incr, code)
            code.emit(I.JMP(start_label))
            code.emit_label(end_label)
            
            # Pop the loop's scope when done
            # code.emit(I.POP_SCOPE())
            
            # Remove these labels from the tracking stacks
            code.loop_start_labels.pop()
            code.loop_end_labels.pop()


        case Feed(msg):
            generate_bytecode(msg, code)
            code.emit(I.INPUT())

        case FormatString(template, variables):
            # Push template string
            code.emit(I.PUSH(template))
            
            # Push each variable needed for interpolation
            for var in variables:
                code.emit(I.LOAD(var))
            
            # Call the format function with number of variables
            code.emit(I.CALL(f"format_string_{len(variables)}"))
        
        case TypeCast(dtype, value):
            generate_bytecode(value, code)
            code.emit(I.TYPECAST(dtype))

        case TypeOf(value):
            generate_bytecode(value, code)
            code.emit(I.CALL("typeof"))

        case MathFunction(funcName, args):
            # Push all arguments in order
            for arg in args:
                generate_bytecode(arg, code)
            
            # Call the appropriate math function
            code.emit(I.CALL(f"math_{funcName.lower()}"))

        case Break():
            # This might be a simple break statement, not tied to loops
            code.emit(I.RETURN())


        # Function operations
        case FuncDef(func_name, params, body, _):
            func_end_label = code.label()
            func_start_label = code.label()
            
            code.emit(I.JMP(func_end_label))
            code.emit_label(func_start_label)
            
            # Store parameters in reverse order
            for param in reversed(params):
                code.emit(I.STORE(param[0]))
                
            generate_bytecode(body, code)
            code.emit(I.RETURN())
            
            code.emit_label(func_end_label)
            code.emit(I.PUSHFN(func_start_label, func_name))
            # code.emit(I.STORE(func_name))
        
        case FuncCall(func_name, args):
            for arg in args:
                generate_bytecode(arg, code)
            code.emit(I.CALL(func_name))
        
        # I/O operations
        case Display(val):
            generate_bytecode(val, code)
            code.emit(I.PRINT())
        
        case DisplayL(val):
            generate_bytecode(val, code)
            code.emit(I.PRINTLN())
        
        # Collection of statements
        case Statements(statements):
            for stmt in statements:
                generate_bytecode(stmt, code)

        # Array/String special operations - modify these cases in generate_bytecode()
        case PushFront(arr_name, value):
            code.emit(I.LOAD(arr_name))
            # Load the object to determine its type at runtime
            code.emit(I.DUP())  # Duplicate for type check
            code.emit(I.CALL("type_check"))  # Custom built-in to check type
            code.emit(I.JMP_IF_TRUE(skip_label := code.label()))  # Skip to array handling if True
            
            # String handling (if not array)
            generate_bytecode(value, code)
            code.emit(I.CALL("string_pushfront"))
            code.emit(I.STORE(arr_name))
            code.emit(I.JMP(end_label := code.label()))
            
            # Array handling
            code.emit_label(skip_label)
            generate_bytecode(value, code)
            code.emit(I.PUSH(0))  # Index 0
            code.emit(I.CALL("array_insert"))
            code.emit(I.STORE(arr_name))
            
            code.emit_label(end_label)

        case PushBack(arr_name, value):
            code.emit(I.LOAD(arr_name))
            # Load the object to determine its type at runtime
            code.emit(I.DUP())  # Duplicate for type check
            code.emit(I.CALL("type_check"))  # Custom built-in to check type
            code.emit(I.JMP_IF_TRUE(skip_label := code.label()))  # Skip to array handling if True
            
            # String handling (if not array)
            generate_bytecode(value, code)
            code.emit(I.CALL("string_pushback"))
            code.emit(I.STORE(arr_name))
            code.emit(I.JMP(end_label := code.label()))
            
            # Array handling
            code.emit_label(skip_label)
            generate_bytecode(value, code)
            code.emit(I.CALL("array_append"))
            code.emit(I.STORE(arr_name))
            
            code.emit_label(end_label)

        case PopFront(arr_name):
            code.emit(I.LOAD(arr_name))
            code.emit(I.DUP())  # Duplicate for type check
            code.emit(I.CALL("type_check"))
            code.emit(I.JMP_IF_TRUE(skip_label := code.label()))
            
            # String handling
            code.emit(I.CALL("string_popfront"))
            code.emit(I.STORE(arr_name))
            code.emit(I.JMP(end_label := code.label()))
            
            # Array handling
            code.emit_label(skip_label)
            code.emit(I.CALL("array_popfront"))
            code.emit(I.STORE(arr_name))
            
            code.emit_label(end_label)

        case PopBack(arr_name):
            code.emit(I.LOAD(arr_name))
            code.emit(I.DUP())  # Duplicate for type check
            code.emit(I.CALL("type_check"))
            code.emit(I.JMP_IF_TRUE(skip_label := code.label()))
            
            # String handling
            code.emit(I.CALL("string_popback"))
            code.emit(I.STORE(arr_name))
            code.emit(I.JMP(end_label := code.label()))
            
            # Array handling
            code.emit_label(skip_label)
            code.emit(I.CALL("array_popback"))
            code.emit(I.STORE(arr_name))
            
            code.emit_label(end_label)

        case GetLength(arr_name):
            code.emit(I.LOAD(arr_name))
            code.emit(I.CALL("length"))

        
        # String operations
        case StringIdx(var_name, index):
            code.emit(I.LOAD(var_name))
            generate_bytecode(index, code)
            code.emit(I.CALL("string_index"))
        
        case Slice(var_name, start, end, step):
            code.emit(I.LOAD(var_name))
            
            # Handle optional parameters
            if start:
                generate_bytecode(start, code)
            else:
                code.emit(I.PUSH(None))
            
            if end:
                generate_bytecode(end, code)
            else:
                code.emit(I.PUSH(None))
            
            if step:
                generate_bytecode(step, code)
            else:
                code.emit(I.PUSH(None))
            
            code.emit(I.CALL("obj_slice"))  # Generic slice operation for both strings and arrays

def compile_program(source_code):
    # Parse the program
    ast, symbol_table = parse(source_code, SymbolTable())
    
    # Generate bytecode
    bytecode = codegen(ast)
    
    return bytecode, symbol_table

# Example usage
if __name__ == "__main__":
    programs = [
        """
        var integer x = 5;
        var integer y = 10;
        displayl (x + y);
        """,
        """
        var integer sum=0;
        for (var i=1;i<10;i+=1){
            sum+=i;
        };
        displayl sum;
        display "done";
        """,
        """
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
        """,
        """
        var a= char (66);
        displayl a;
        var b= ascii("A");
        displayl b;
        var c= char (ascii('x') + ascii (char(1)));
        displayl c;    
        """
    ]

    for i, program in enumerate(programs):
        print(f"Program {i+1}:\n{program}\n")
        bytecode, symbols = compile_program(program)
        print("Bytecode:")
        bytecode.print_bytecode()
        print("\n" + "="*40 + "\n")
    # pprint(bytecode.insns)