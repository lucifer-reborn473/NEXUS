from parser import *
from scope import SymbolCategory, SymbolTable
import copy
import math
import re
import sys

sys.setrecursionlimit(10000)

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
                    raise ValueError(
                        f"Cannot cast {var_val} to array: value must be a list."
                    )
            case "Hash":
                if not isinstance(var_val, dict):
                    raise ValueError(
                        f"Cannot cast {var_val} to Hash: value must be a dictionary."
                    )
            case "boolean":
                var_val = bool(var_val)
            case None:
                pass  # No typecasting needed
            case _:
                raise ValueError(f"Unknown data type: {dtype}")
    except (ValueError, TypeError) as err:
        raise ValueError(
            f"Typecasting error for variable '{name}' to type '{dtype}': {err}"
        )
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
            if "." in n:  # Check if the number contains a decimal point
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
                raise ValueError(
                    "Math error: Zero cannot be raised to a negative power."
                )
            # Rule 2: Negative number to the power of a decimal
            if base < 0 and not exponent.is_integer():
                raise ValueError(
                    "Math error: Negative numbers cannot be raised to a decimal power."
                )
            return base**exponent
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
            cat = tS.lookup(v, cat=True)
            if cat == SymbolCategory.FUNCTION:
                value, lexParent = tS.lookup(v, giveParent=True)
                """
                when accessing function like a variable (as param/return)
                value format: (params:[], body: Statements(), pS)
                pS is parsedScope whose parent must be set to lexical parent
                """
                # value[2].parent = lexParent # where this variable is found
                # return (value[0], value[1], value[2])
                isolated_scope = copy.deepcopy(value[2])
                isolated_scope.parent = lexParent
                return (value[0], value[1], isolated_scope)
            else:
                return tS.lookup(v)

        case VarBind(name, dtype, value, category):
            var_val = e(value, tS)
            var_val = perform_typecast(var_val, dtype, name)
            tS.define(name, var_val, category)  # binds in current scope
            return var_val

        case UpdateVar(var_name, value):
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

        # FUNCTIONS ===========================================================================
        case FuncDef(funcDefName, funcDefParams, funcDefBody, funcDefScope):
            # tS.define(fusncName, (funcParams, funcBody, funcScope, isRec), SymbolCategory.FUNCTION)
            return (funcDefParams, funcDefBody, funcDefScope)

        case FuncCall(fn_name, fn_args):
            # Step 1: Extract function body & adjust scope
            cat = tS.lookup(fn_name, cat=True)
            if cat == SymbolCategory.VARIABLE:
                # means variable was assigned a function, and now being called
                # closure applies here, i.e, parsedScope already "carries" the correct parent
                (param_list, fn_body, parsedScope) = tS.lookup(fn_name)
                eval_scope = SymbolTable(parsedScope.parent)
            else:
                # else we "find" the parent
                ((param_list, fn_body, parsedScope), fn_parent) = tS.lookup_fun(fn_name)
                eval_scope = SymbolTable(fn_parent)

            for key, value in parsedScope.table.items():
                if value[1] == SymbolCategory.VARIABLE:
                    # for parameters and local variables (for which value[0] is None in parsedScope)
                    eval_scope.table[key] = (None, SymbolCategory.VARIABLE)
                elif value[1] == SymbolCategory.FUNCTION:
                    # for function declarations (value[0] is a tuple (params, body, tS_f))
                    # prm = copy.deepcopy(value[0][0]) # list of strings
                    # bdy = copy.deepcopy(value[0][1]) # Statements
                    prm = value[0][0]  # list of strings
                    bdy = value[0][1]  # Statements
                    eval_scope.table[key] = (
                        (prm, bdy, value[0][2]),
                        SymbolCategory.FUNCTION,
                    )

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
                raise ValueError(
                    "Repeat loop requires a non-negative integer for the number of repetitions."
                )

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

        # STRING OPERATIONS ===================================================
        case StringIdx(var_name, index):
            string_val = tS.lookup(var_name)
            if not isinstance(string_val, str):
                raise TypeError(
                    f"StringIdx operation not supported for type {type(string_val)}"
                )
            idx = e(index, tS)
            if not (0 <= idx < len(string_val)):
                raise IndexError(f"Index {idx} out of bounds for string: {var_name}")
            return string_val[idx]

        case AssignStringVal(var_name, index, value):
            string_val = tS.lookup(var_name)
            if not isinstance(string_val, str):
                raise TypeError(
                    f"AssignStringVal operation not supported for type {type(string_val)}"
                )
            idx = e(index, tS)
            if not (0 <= idx < len(string_val)):
                raise IndexError(f"Index {idx} out of bounds for string: {var_name}")
            val = e(value, tS)
            string_val = string_val[:idx] + val + string_val[idx + 1 :]
            tS.find_and_update(var_name, string_val)
            return string_val

        case Slice(var_name, start, end, step):
            arr = tS.lookup(var_name)
            if isinstance(arr, (list, str)):
                start_idx = e(start, tS) if start else None
                end_idx = e(end, tS) if end else None
                step_val = e(step, tS) if step else None
                return arr[start_idx:end_idx:step_val]
            else:
                raise TypeError(f"Slice operation not supported for type {type(arr)}")

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
            arr = tS.lookup(arr_name)
            if isinstance(arr, list):
                arr.insert(0, e(value, tS))
            elif isinstance(arr, str):
                arr = e(value, tS) + arr
            else:
                raise TypeError(
                    f"PushFront operation not supported for type {type(arr)}"
                )
            tS.find_and_update(arr_name, arr)
            return arr

        case PushBack(arr_name, value):
            arr = tS.lookup(arr_name)
            if isinstance(arr, list):
                arr.append(e(value, tS))
            elif isinstance(arr, str):
                arr += e(value, tS)
            else:
                raise TypeError(
                    f"PushBack operation not supported for type {type(arr)}"
                )
            tS.find_and_update(arr_name, arr)
            return arr

        case PopFront(arr_name):
            arr = tS.lookup(arr_name)
            if isinstance(arr, list):
                if len(arr) > 0:
                    value = arr.pop(0)
                else:
                    raise IndexError(f"Cannot PopFront from an empty array: {arr_name}")
            elif isinstance(arr, str):
                if len(arr) > 0:
                    value = arr[0]
                    arr = arr[1:]
                else:
                    raise IndexError(
                        f"Cannot PopFront from an empty string: {arr_name}"
                    )
            else:
                raise TypeError(
                    f"PopFront operation not supported for type {type(arr)}"
                )
            tS.find_and_update(arr_name, arr)
            return value

        case PopBack(arr_name):
            arr = tS.lookup(arr_name)
            if isinstance(arr, list):
                if len(arr) > 0:
                    value = arr.pop()
                else:
                    raise IndexError(f"Cannot PopBack from an empty array: {arr_name}")
            elif isinstance(arr, str):
                if len(arr) > 0:
                    value = arr[-1]
                    arr = arr[:-1]
                else:
                    raise IndexError(f"Cannot PopBack from an empty string: {arr_name}")
            else:
                raise TypeError(f"PopBack operation not supported for type {type(arr)}")
            tS.find_and_update(arr_name, arr)
            return value

        case GetLength(arr_name):
            arr = tS.lookup(arr_name)
            if isinstance(arr, (list, str)):
                return len(arr)
            else:
                raise TypeError(
                    f"GetLength operation not supported for type {type(arr)}"
                )

        case ClearArray(arr_name):
            arr = tS.lookup(arr_name)
            if isinstance(arr, list):
                arr.clear()
            elif isinstance(arr, str):
                arr = ""
            else:
                raise TypeError(f"Clear operation not supported for type {type(arr)}")
            tS.find_and_update(arr_name, arr)
            return arr

        case InsertAt(arr_name, index, value):
            arr = tS.lookup(arr_name)
            if isinstance(arr, list):
                arr.insert(e(index, tS), e(value, tS))
            elif isinstance(arr, str):
                idx = e(index, tS)
                val = e(value, tS)
                arr = arr[:idx] + val + arr[idx:]
            else:
                raise TypeError(
                    f"InsertAt operation not supported for type {type(arr)}"
                )
            tS.find_and_update(arr_name, arr)
            return arr

        case RemoveAt(arr_name, index):
            arr = tS.lookup(arr_name)
            if isinstance(arr, list):
                if 0 <= e(index, tS) < len(arr):
                    value = arr.pop(e(index, tS))
                else:
                    raise IndexError(
                        f"Index {e(index, tS)} out of bounds for array: {arr_name}"
                    )
            elif isinstance(arr, str):
                idx = e(index, tS)
                if 0 <= idx < len(arr):
                    value = arr[idx]
                    arr = arr[:idx] + arr[idx + 1 :]
                else:
                    raise IndexError(
                        f"Index {idx} out of bounds for string: {arr_name}"
                    )
            else:
                raise TypeError(
                    f"RemoveAt operation not supported for type {type(arr)}"
                )
            tS.find_and_update(arr_name, arr)
            return value

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
            return input(e(msg, tS))

        case FormatString(template, variables):
            varmods = {var: e(Variable(var), tS) for var in variables}

            # Use eval to evaluate expressions inside braces
            def evaluate_expression(match):
                expression = match.group(1)
                return str(eval(expression, {}, varmods))

            evaluated_template = re.sub(r"\{(.*?)\}", evaluate_expression, template)
            return evaluated_template

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
                    return round(
                        arg_values[0], arg_values[1] if len(arg_values) > 1 else 0
                    )
                case "ceil":
                    return math.ceil(arg_values[0])
                case "floor":
                    return math.floor(arg_values[0])
                case "truncate":
                    return math.trunc(arg_values[0])
                case "sqrt":
                    return math.sqrt(arg_values[0])
                case "cbrt":
                    return arg_values[0] ** (1 / 3)
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

    prog2 = """
    var decimal x =10.34;
    var integer y = 10; 
    displayl (string(x) + " dip " + (string(y)));
    displayl (integer(x) + y);
    """

    prog2 = """
    var array nums = [1.1, 2.2, 3.3];
    var integer sum = 0;
    for (var i=0; i<3; i+=1) {
        sum = sum + integer(nums[i]);
    };
    displayl sum;
"""

    prog2 = """
    var array h = [1, 2, 3];
    var sum=0;
    repeat (h.Length){
        sum += h.PopFront;
    }
    displayl sum;
    displayl h;
    """

    prog2 = """
    repeat (10){
        displayl 1;
    }
"""
    prog2 = """var arr = [[1, 2, 3], [4, 5, 6], [7, 8, 9]];
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

    prog2 = """
    var hash = {
        "key1": {"nestedKey1": 10, "nestedKey2": 20},
        "key2": {"nestedKey3": 30, "nestedKey4": 40}
    };
    displayl hash["key1"]["nestedKey2"];
    hash["key2"]["nestedKey3"] = 50;
    displayl hash;
"""

    prog2 = """
fn add(a, b) {
    a + b;
};
fn subtract(a, b) {
    a - b;
};
fn multiply(a, b) {
    a * b;
};
var funcs = [add, subtract, multiply];
displayl funcs[0](10, 5);
displayl funcs[1](10, 5);
displayl funcs[2](10, 5);
    """  #! error ('CallArr' object has no attribute 'var_name')

    prog2 = """
fn A(w,v){
    w()+v();
};
fn one() { 1; };
fn negone() { 0-1; };
displayl A(one, negone);
"""  # works #! but why we have to put zero here?

    prog = """
var a = [1,2,3];
fn foo(arr){
    arr[0] = 100;
};
foo(a);
displayl a;
"""

    prog2 = """
var a;
a[0] = 100;
"""  #! same error as in above

    prog2 = """
var a = fn foo(){100;};
displayl a();
"""

    # parsed, gS = parse(prog, SymbolTable())
    # print("------")
    # pprint(parsed)
    # print("------")
    # pprint(gS.table)

    print("------")
    print("Program Output: ")
    execute(prog)
