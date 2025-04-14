from parser import *
from scope import SymbolCategory, SymbolTable
import copy

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
def e(tree: AST, tS) -> Any:
    match tree:
        case Number(n):
            if '.' in n:  # Check if the number contains a decimal point
                return float(n)  # Return as a float
            else:
                return int(n)
        case String(s):
            return s
        case Boolean(b):
            return b
        case Variable(v):
            return tS.lookup(v)
        case FormatString(template, variables):
            varmods = {var: e(Variable(var), tS) for var in variables}
            return template.format(**varmods)
        case Array(val):
            all_vals = list(map(lambda x: e(x, tS), val))
            return all_vals
        case Hash(val):
            return {e(k, tS): e(v, tS) for k, v in val}
        # Operators
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
        case Feed(msg):
            return input(e(msg,tS))
        case TypeCast(dtype, value):
            return perform_typecast(e(value, tS), dtype)
        case FuncDef(_funcName, _funcParams, _funcBody, _funcScope):
            # tS.define(funcName, (funcParams, funcBody, funcScope, isRec), SymbolCategory.FUNCTION)
            return

        case FuncCall(fn_name, fn_args):
            # Step 1: Extract function body & adjust scope
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

            # Step 4: Pop the arg values from the function's scope (don't delete the scope table)
            # although not needed (freed implicitly when the function returns)
            for param in param_list:
                eval_scope.define(param, 100, SymbolCategory.VARIABLE)

            return ans

        case Statements(statements):
            result = None
            for stmt in statements:
                result = e(stmt, tS)
            return result

        # Conditional
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

        # Display
        case Display(val):
            return print(e(val, tS), end="")

        case DisplayL(val):
            return print(e(val, tS))

        case CompoundAssignment(var_name, op, value):
            # Check if variable is fixed
            category = tS.lookup(var_name, cat=True)
            if category == SymbolCategory.FIXED:
                raise ValueError(f"Error: Cannot modify fixed variable '{var_name}'")
            prev_val = tS.lookup(var_name)
            new_val = e(BinOp(op[0], Number(str(prev_val)), value), tS)
            tS.find_and_update(var_name, new_val)
            return new_val

        case VarBind(name, dtype, value, category):
            var_val = e(value, tS)
            var_val = perform_typecast(var_val, dtype, name)
            tS.define(name, var_val, category)  # binds in current scope
            return var_val
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
        case AssignToVar(var_name, value):
            val_to_assign = e(value, tS)
            tS.find_and_update(var_name, val_to_assign)
            return val_to_assign

        case CallArr(xname, index):
            return tS.lookup(xname)[e(index, tS)]
        
        case AssigntoArr(xname, index, value):
            val_to_assign = e(value, tS)
            tS.find_and_update_arr(xname, e(index, tS), val_to_assign)
            return val_to_assign
        #hash funcs
        case CallHashVal(name,key):
           return tS.lookup(name)[e(key, tS)]
        
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

        case AssignHashVal(name, key, new_val):
            hash_table = tS.lookup(name)
            hash_table[e(key, tS)] = e(new_val, tS)
            tS.find_and_update(name, hash_table)
            return hash_table[e(key, tS)]
            
        # Loops
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

def execute(prog):
    lines, tS = parse(prog)
    for line in lines.statements:
        e(line, tS)

if __name__ == "__main__":

    # # expr = "display 0<= 1 >=2 "
    # expr = " display( var integer x= 3+ 7 -1);"
    # compound_assignment= "display (x-=2);"
    # # loop <condition> then <statement> end
    # # int32 x=2

    # ========================================================
    # Loading the Program
    fileName = "sample-code.txt"
    try:
        with open(fileName, "r") as file:
            prog_fin = file.read()
    except FileNotFoundError:
        print(f"The file {fileName} was not found.")
    except IOError:
        print("An error occurred while reading the file.")

    def execute(prog):
        lines, tS = parse(prog)
        for line in lines.statements:
            e(line, tS)

    # ========================================================


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
    prog = """
    var a =[1,2,3,4];
    var b =20;
    a[1]=b;
    displayl a;
    displayl a[2];
    var c=[10,11,12,13];
    c[1]=a[2]+b;
    displayl c;
"""
    prog = """
fn foo(){
    fn bar(){
        x+2;
    }
    bar; /> returns a function
}
var x = 40;
var y = foo(); /> assigns to a variable
displayl y();
"""
    prog = """
    var arr = [1, 2, 3];
    var hash = {"key1": 10, "key2": 20};

    arr.PushBack(4);
    hash.Add("key3", 30);

    displayl ("array display:");
    for (var integer i = 0; i < arr.Length; i = i + 1) {
        displayl arr[i];
    }
    fn multiply(a, b) {
        a * b;
    }
    displayl multiply(hash["key1"], 2);
    """


    parsed, gS = parse(prog)
    print("------")
    pprint(parsed)
    print("------")
    pprint(gS.table)

    print("------")
    print("Program Output: ")
    execute(prog)
