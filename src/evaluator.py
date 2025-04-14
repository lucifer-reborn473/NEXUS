from parser import *
from scope import SymbolCategory, SymbolTable
import copy
import math

# ==========================================================================================
# ==================================== (TREE-WALK) EVALUATOR ===============================


def perform_typecast(var_val, dtype, name=None):
    try:
        match dtype:
            case "integer":
                var_val = int(var_val)
            case "decimal":
                var_val = float(var_val)
            case "uinteger":
                var_val = int(var_val)
                if var_val < 0:
                    var_val *= -1
            case "string":
                var_val = str(var_val)
            case "array":
                if not isinstance(var_val, list):
                    raise ValueError(f"Cannot cast {var_val} to array: value must be a list.")
            case "Hash":
                if not isinstance(var_val, dict):
                    raise ValueError(f"Cannot cast {var_val} to Hash: value must be a dictionary.")
            case "boolean":
                var_val = bool(var_val)
            case None:
                pass  # No typecasting needed
            case _:
                raise ValueError(f"Unknown data type: {dtype}")
    except (ValueError, TypeError) as err:
        raise ValueError(f"Typecasting error for variable '{name}' to type '{dtype}': {err}")
    return var_val

# ================================================================================================================
"""
Cases inside e() listed in below order:
1. PRIMITIVES
2. OPERATORS
3. VARIABLE ACCESS, DECLARATION & UPDATE
4. CONDITIONALS
5. LOOPS
6. FUNCTIONS
7. ARRAY OPERATIONS
8. HASH OPERATIONS
9. FEATURES
"""


def e(tree: AST, tS) -> Any:
    match tree:
        # Primitives ========================================================
        case Number(n):
            if '.' in n:  # Check if the number contains a decimal point
                return float(n)  # Return as a float
            else:
                return int(n)
        case String(s):
            return s
        case Boolean(b):
            return b
        
        # OPERATORS =================================================================================
        case BinOp("+", l, r):
            return e(l, tS) + e(r, tS)
        case BinOp("*", l, r):
            return e(l, tS) * e(r, tS)
        case BinOp("-", l, r):
            return e(l, tS) - e(r, tS)
        case BinOp("÷", l, r):
            return e(l, tS) / e(r, tS)
        case BinOp("/", l, r):
            return e(l, tS) / e(r, tS)
        case BinOp("**", l, r):
            base = e(l, tS)
            exponent = e(r, tS)
            # Rule 1: Zero to the power of a negative number
            if base == 0 and exponent < 0:
                raise ValueError("Math error: Zero cannot be raised to a negative power.")
            # Rule 2: Negative number to the power of a decimal
            if base < 0 and not exponent.is_integer():
                raise ValueError("Math error: Negative numbers cannot be raised to a decimal power.")
            return base ** exponent
        case BinOp("<", l, r):
            return e(l, tS) < e(r, tS)
        case BinOp(">", l, r):
            return e(l, tS) > e(r, tS)
        case BinOp("==", l, r):
            return e(l, tS) == e(r, tS)
        case BinOp("!=", l, r):
            return e(l, tS) != e(r, tS)
        case BinOp("<=", l, r):
            return e(l, tS) <= e(r, tS)
        case BinOp(">=", l, r):
            return e(l, tS) >= e(r, tS)
        case BinOp("%", l, r):
            return e(l, tS) % e(r, tS)
        case BinOp("and", l, r):
            return e(l, tS) and e(r, tS)
        case BinOp("or", l, r):
            return e(l, tS) or e(r, tS)
        case BinOp("&", l, r):
            return e(l, tS) & e(r, tS)
        case BinOp("|", l, r):
            return e(l, tS) | e(r, tS)
        case BinOp("^", l, r):
            return e(l, tS) ** e(r, tS)
        case BinOp("<<", l, r):
            return e(l, tS) << e(r, tS)
        case BinOp(">>", l, r):
            return e(l, tS) >> e(r, tS)
        case BinOp("not", l, _):  # Unary logical operator
            return not e(l, tS)
        case BinOp("~", l, _):  # Unary bitwise operator
            return ~e(l, tS)
        case UnaryOp("~", val):
            return ~e(val, tS)
        case UnaryOp("not", val):
            return not e(val, tS)
        case UnaryOp("!", val):
            return not e(val, tS)
        case UnaryOp("ascii", val):
            return ord(e(val, tS))
        case UnaryOp("char", val):
            return chr(e(val, tS))
        
        # VARIABLE ACCESS, DECLARATION & UPDATE ========================================================
        case Variable(v):
            data, lexParent = tS.lookup(v, giveParent=True)
            if isinstance(data, tuple):
                """
                when accessing function like a variable (as param/return)
                value format: (params:[], body: Statements(), pS)
                pS is parsedScope whose parent must be set to lexical parent
                """
                
                def unwrap_function(fd):
                    # If it's a wrapped function with category
                    if (isinstance(fd, tuple) and len(fd) == 2 and 
                        isinstance(fd[1], SymbolCategory) and 
                        fd[1] == SymbolCategory.FUNCTION):
                        # Unwrap one level and check again
                        return unwrap_function(fd[0])
                    return fd

                value = unwrap_function(data)

                value[2].parent = lexParent # where this variable is found
                # tree.is_fun = True
                return (value[0], value[1], value[2])
            
            else:
                return data
        
        case VarBind(name, dtype, value, category):
            var_val = e(value, tS)
            var_val = perform_typecast(var_val, dtype, name)
            tS.define(name, var_val, category)  # binds in current scope
            return var_val
        
        case AssignToVar(var_name, value):
            val_to_assign = e(value, tS)
            tS.find_and_update(var_name, val_to_assign)
            return val_to_assign
        
        case CompoundAssignment(var_name, op, value):
            # Check if variable is fixed
            category = tS.lookup(var_name, cat=True)
            if category == SymbolCategory.FIXED:
                raise ValueError(f"Error: Cannot modify fixed variable '{var_name}'")
            prev_val = tS.lookup(var_name)
            new_val = e(BinOp(op[0], Number(str(prev_val)), value), tS)
            tS.find_and_update(var_name, new_val)
            return new_val
        
        # CONDITIONAL ===========================================================================
        case If(cond, then_body, else_body, tS_cond):
            eval_cond_scope = SymbolTable(parent=tS)
            # Copy static declarations from parse-time scope
            for key, value in tS_cond.table.items():
                if value[1] == SymbolCategory.VARIABLE:
                    eval_cond_scope.table[key] = (None, SymbolCategory.VARIABLE)
                elif value[1] == SymbolCategory.FUNCTION:
                    eval_cond_scope.table[key] = copy.deepcopy(value)
            ans = None
            if e(cond, eval_cond_scope):
                ans = e(then_body, eval_cond_scope)
            elif else_body is not None:
                ans = e(else_body, eval_cond_scope)
            return ans

        # LOOPS ========================================================================================
        case WhileLoop(cond, body, tS_while):

            eval_while_scope = SymbolTable(parent=tS)
            # Copy static declarations from parse-time scope
            for key, value in tS_while.table.items():
                if value[1] == SymbolCategory.VARIABLE:
                    eval_while_scope.table[key] = (None, SymbolCategory.VARIABLE)
                elif value[1] == SymbolCategory.FUNCTION:
                    eval_while_scope.table[key] = copy.deepcopy(value)

            while e(cond, eval_while_scope):
                loop_should_break = False
                for stmt in body.statements:
                    result = e(stmt, eval_while_scope)
                    if isinstance(result, BreakOut):
                        loop_should_break = True
                        break  
                    elif isinstance(result, MoveOn):
                        break
                if loop_should_break:
                    break

        case ForLoop(init, cond, incr, body, tS_for):
            eval_for_scope = SymbolTable(parent=tS)
            # Copy static declarations from parse-time scope
            for key, value in tS_for.table.items():
                if value[1] == SymbolCategory.VARIABLE:
                    eval_for_scope.table[key] = (None, SymbolCategory.VARIABLE)
                elif value[1] == SymbolCategory.FUNCTION:
                    eval_for_scope.table[key] = copy.deepcopy(value)

            e(init, eval_for_scope)
            while e(cond, eval_for_scope):
                loop_should_break = False
                for stmt in body.statements:
                    result = e(stmt, eval_for_scope)
                    if isinstance(result, BreakOut):
                        loop_should_break = True
                        break
                    elif isinstance(result, MoveOn):
                        break
                if loop_should_break:
                    break
                e(incr, eval_for_scope)

        case Repeat(times, body, repeatScope):
            repetitions = e(times, repeatScope)
            if not isinstance(repetitions, int) or repetitions < 0:
                raise ValueError("Repeat loop requires a non-negative integer for the number of repetitions.")

            for _ in range(repetitions):
                loop_should_break = False
                for stmt in body.statements:
                    result = e(stmt, repeatScope)
                    if isinstance(result, BreakOut):
                        loop_should_break = True
                        break
                    elif isinstance(result, MoveOn):
                        break
                if loop_should_break:
                    break
        
        case BreakOut():
            return BreakOut()

        case MoveOn():
            return MoveOn()

        # FUNCTIONS ===========================================================================
        case FuncDef(funcDefName, funcDefParams, funcDefBody, funcDefScope):
            # tS.define(fusncName, (funcParams, funcBody, funcScope, isRec), SymbolCategory.FUNCTION)
            # return (funcDefParams, funcDefBody, funcDefScope)
            return

        case FuncCall(fn_name, fn_args):
            # Step 1: Extract function body & adjust scope

            cat = tS.lookup(fn_name, cat=True)
            if cat==SymbolCategory.VARIABLE:
                # means variable was assigned a function, and now been called
                # closure applies here, i.e, parsedScope "carries" the correct parent
                (param_list, fn_body, parsedScope) = tS.lookup(fn_name)
                eval_scope = SymbolTable(parsedScope.parent)
            else:
                ((param_list, fn_body, parsedScope), fn_parent) = tS.lookup_fun(fn_name)
                eval_scope = SymbolTable(fn_parent)
            
            for key, value in parsedScope.table.items():
                k = copy.deepcopy(key)
                if (value[1]==SymbolCategory.VARIABLE):
                    # for parameters and local variables (for which value[0] is None in parsedScope)
                    eval_scope.table[k] = (None, SymbolCategory.VARIABLE)
                elif (value[1]==SymbolCategory.FUNCTION):
                    # for function declarations (value[0] is of type FuncDef)
                    v = copy.deepcopy(value)
                    eval_scope.table[k] = (v, SymbolCategory.FUNCTION)
            
            # Step 2: Put argument values into function's scope
            for param, arg in zip(param_list, fn_args):                        
                eval_scope.define(param, e(arg, tS), SymbolCategory.VARIABLE)

            # Step 3: Evaluate the function body
            ans = None
            for stmt in fn_body.statements:
                ans = e(stmt, eval_scope)

            # NOT DONE to support closure
            # Step 4: Pop the arg values from the function's scope (don't delete the scope table)
            # although not needed (freed implicitly when the function returns)
            # for param in param_list:
            #     eval_scope.define(param, None, SymbolCategory.VARIABLE)

            return ans

        # ARRAY OPERATIONS ========================================================================
        case Array(val):
            all_vals = list(map(lambda x: e(x, tS), val))
            return all_vals
        
        case CallArr(xname, indices):
            arr = tS.lookup(xname)
            for index in indices:
                arr = arr[e(index, tS)]
            return arr

        case AssigntoArr(xname, indices, value):
            arr = tS.lookup(xname)
            *outer_indices, last_index = [e(index, tS) for index in indices]
            for index in outer_indices:
                arr = arr[index]
            arr[last_index] = e(value, tS)
            tS.find_and_update(xname, tS.lookup(xname))
            return arr[last_index]

        case PushFront(arr_name, value):
            arr= tS.lookup(arr_name)
            arr.insert(0, e(value, tS))
            tS.find_and_update(arr_name, arr)
            return arr

        case PushBack(arr_name, value):
            arr = tS.lookup(arr_name)
            arr.append(e(value, tS))
            tS.find_and_update(arr_name, arr)
            return arr

        case PopFront(arr_name):
            arr = tS.lookup(arr_name)
            if len(arr) > 0:
                value = arr.pop(0)
                tS.find_and_update(arr_name, arr)
                return value
            else:
                raise IndexError(f"Cannot PopFront from an empty array: {arr_name}")

        case PopBack(arr_name):
            arr = tS.lookup(arr_name)
            if len(arr) > 0:
                value = arr.pop()
                tS.find_and_update(arr_name, arr)
                return value
            else:
                raise IndexError(f"Cannot PopBack from an empty array: {arr_name}")

        case GetLength(arr_name):
            return len(tS.lookup(arr_name))

        case ClearArray(arr_name):
            arr = tS.lookup(arr_name)
            arr.clear()
            tS.find_and_update(arr_name, arr)
            return arr

        case InsertAt(arr_name, index, value):
            arr = tS.lookup(arr_name)
            arr.insert(e(index, tS), e(value, tS))
            tS.find_and_update(arr_name, arr)
            return arr

        case RemoveAt(arr_name, index):
            arr = tS.lookup(arr_name)
            if 0 <= e(index, tS) < len(arr):
                value = arr.pop(e(index, tS))
                tS.find_and_update(arr_name, arr)
                return value
            else:
                raise IndexError(f"Index {e(index, tS)} out of bounds for array: {arr_name}")
        # case BindArray(xname, atype, val):
        #     all_vals = list(map(lambda x: e(x, tS), val))
        #     tS.table[xname] = all_vals
        #     tS.define(xname,all_vals,SymbolCategory.ARRAY)
        #     return all_vals


        # HASH OPERATIONS ========================================================================
        case Hash(val):
            return {e(k, tS): e(v, tS) for k, v in val}
       
        case CallHashVal(name, keys):
            hash_table = tS.lookup(name)
            for key in keys:
                hash_table = hash_table[e(key, tS)]
            return hash_table
        
        case AddHashPair(name, key, val):
            hash_table = tS.lookup(name)
            hash_table[e(key, tS)] = e(val, tS)
            tS.find_and_update(name, hash_table)
        
        case RemoveHashPair(name, key):
            hash_table = tS.lookup(name)
            if e(key, tS) in hash_table:
                del hash_table[e(key, tS)]
                tS.find_and_update(name, hash_table)
            else:
                raise KeyError(f"Key {e(key, tS)} not found in hash {name}")

        case AssignHashVal(name, keys, new_val):
            hash_table = tS.lookup(name)
            *outer_keys, last_key = [e(key, tS) for key in keys]
            for key in outer_keys:
                hash_table = hash_table[key]
            hash_table[last_key] = e(new_val, tS)
            tS.find_and_update(name, tS.lookup(name))
            return hash_table[last_key]
        
        # FEATURES =================================================================================
        case Display(val):
            return print(e(val, tS), end="")

        case DisplayL(val):
            return print(e(val, tS))
        
        case Feed(msg):
            return input(e(msg,tS))
        
        case FormatString(template, variables):
            varmods = {var: e(Variable(var), tS) for var in variables}
            return template.format(**varmods)
        
        case TypeCast(dtype, value):
            return perform_typecast(e(value, tS), dtype)
        
        case Statements(statements):
            result = None
            for stmt in statements:
                result = e(stmt, tS)
            return result
        
        case TypeOf(value):
            val = e(value, tS)
            python_type = type(val)
            type_mapping = {
                int: "integer",
                float: "decimal",
                str: "string",
                list: "array",
                dict: "Hash",
                bool: "boolean",
            }
            return type_mapping.get(python_type, "unknown")

        case MathFunction(funcName, args):
            arg_values = [e(arg, tS) for arg in args]
            match funcName:
                case "abs":
                    return math.fabs(arg_values[0])
                case "min":
                    return min(arg_values[0])
                case "max":
                    return max(arg_values[0])
                case "round":
                    return round(arg_values[0], arg_values[1] if len(arg_values) > 1 else 0)
                case "ceil":
                    return math.ceil(arg_values[0])
                case "floor":
                    return math.floor(arg_values[0])
                case "truncate":
                    return math.trunc(arg_values[0])
                case "sqrt":
                    return math.sqrt(arg_values[0])
                case "cbrt":
                    return arg_values[0] ** (1/3)
                case "pow":
                    return math.pow(arg_values[0], arg_values[1])
                case "exp":
                    return math.exp(arg_values[0])
                case "log":
                    return math.log(arg_values[0])
                case "log10":
                    return math.log10(arg_values[0])
                case "log2":
                    return math.log2(arg_values[0])
                case "sin":
                    return math.sin(arg_values[0])
                case "cos":
                    return math.cos(arg_values[0])
                case "tan":
                    return math.tan(arg_values[0])
                case "asin":
                    return math.asin(arg_values[0])
                case "acos":
                    return math.acos(arg_values[0])
                case "atan":
                    return math.atan(arg_values[0])
                case "atan2":
                    return math.atan2(arg_values[0], arg_values[1])
                case "sinh":
                    return math.sinh(arg_values[0])
                case "cosh":
                    return math.cosh(arg_values[0])
                case "tanh":
                    return math.tanh(arg_values[0])
                case "asinh":
                    return math.asinh(arg_values[0])
                case "acosh":
                    return math.acosh(arg_values[0])
                case "atanh":
                    return math.atanh(arg_values[0])
                case "PI":
                    return math.pi
                case "E":
                    return math.e
                case _:
                    raise ValueError(f"Unknown math function: {funcName}")


# ================================================================================================================

def execute(prog):
    pS = SymbolTable()
    lines, tS = parse(prog, pS)
    for line in lines.statements:
        e(line, tS)

# ==================================================================
if __name__ == "__main__":

    prog = """
    for(var i = 0; i < 5; i = i + 1) {
        if i == 2 then moveon end;
        if i == 4 then breakout end;
        displayl i;
    }
    """


    prog= """var a = 5;
var b = `This is a: {a}`;
display `This is b: {b}`;"""

    prog="""
    var decimal x =10.34;
    var integer y = 10; 
    displayl (string(x) + "dip" + (string(y)));
    displayl (integer(x) + y);
    """

    prog="""
    var array nums = [1.1, 2.2, 3.3];
    var integer sum = 0;
    for (var i=0; i<3; i+=1) {
        sum = sum + integer(nums[i]);
    };
    displayl sum;
"""

    prog="""
    var array h = [1, 2, 3];
    var sum=0;
    repeat (h.Length){
        sum+=h.PopFront;
    }
    displayl sum;
    """

    prog="""
    repeat (10){
        displayl 1;
    }
"""
    prog="""var arr = [[1, 2, 3], [4, 5, 6], [7, 8, 9]];
    var hash = {
        "key1": {"nestedKey1": 10, "nestedKey2": 20},
        "key2": {"nestedKey3": 30, "nestedKey4": 40}
    };
    
    displayl arr[1][2];  /> Accessing nested array element
    displayl hash["key1"]["nestedKey2"];  /> Accessing nested hash value
    arr[2][0] = 99;  /> Modifying nested array element
    hash["key2"]["nestedKey3"] = 50;  /> Modifying nested hash value
    displayl arr;
    displayl hash;"""

    prog="""
    var hash = {
        "key1": {"nestedKey1": 10, "nestedKey2": 20},
        "key2": {"nestedKey3": 30, "nestedKey4": 40}
    };
    displayl hash["key1"]["nestedKey2"];
    hash["key2"]["nestedKey3"] = 50;
    displayl hash;
"""

    prog = """
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
""" #works! (prints 12)

    prog = """
fn foo(g){
    g() + 2;
};
fn haha(){
    var x = 100;
    fn bar(){
        x;
    }
    foo(bar);
};
displayl haha();
""" #works! (prints 102)

    prog = """
fn counter() {
    var count = 0;
    fn increment() {
        count = count + 1;
        count;
    }
    increment;
}
var c = counter();
displayl c();
displayl c();
displayl c();
    """# works! (prints 1 2 3)

    prog = """
fn multiplier(factor) {
    fn multiply(n) {
        n * factor;
    };
    multiply;
};
var double = multiplier(2);
var triple = multiplier(3);
displayl double(5);
displayl triple(5);
    """ # works! (prints 10 15)

    prog = """
var x = 100;
fn foo(i){
    fn bar(){
        x+i;
    };
    if i==42 then bar else foo(i+1) end;
};
var y = foo(0);
displayl y();
""" # works! (prints 142)

    prog = """
fn add(a, b) {
    a + b;
}
fn subtract(a, b) {
    a - b;
}
fn multiply(a, b) {
    a * b;
}
var operations = [add, subtract, multiply];
displayl operations[0](10, 5);
displayl operations[1](10, 5);
displayl operations[2](10, 5);
    """ #! error ('CallArr' object has no attribute 'var_name')

    prog = """
var a = [1,2,3]
a[0] = 100;
displayl a;
""" #! error in 2nd line

    prog = """
var u = 100;
for(var u=0; u<3; u+=1){
    var b = 2;
    displayl b;
}
displayl 179;
displayl u;
    """ # works! (prints 2 2 2 179 100) (put in docs)


    # parsed, gS = parse(prog, SymbolTable())
    # print("------")
    # pprint(parsed)
    # print("------")
    # pprint(gS.table)

    print("------")
    print("Program Output: ")
    execute(prog)