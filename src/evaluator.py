from parser import *
from scope import SymbolCategory, SymbolTable
import copy
import math
import re
import sys

sys.setrecursionlimit(10000)
enable_cat_fn = False

# ==========================================================================================
# ==================================== (TREE-WALK) EVALUATOR ===============================

def determine_runtime_category(value):
    """Determine the SymbolCategory of a runtime value."""
    if isinstance(value, list):
        return SymbolCategory.ARRAY
    elif isinstance(value, dict):
        return SymbolCategory.HASH
    elif isinstance(value, str):
        return SymbolCategory.STRING
    # elif isinstance(value, tuple) and len(value) >= 2 and isinstance(value[1], Statements):
    #     return SymbolCategory.FUNCTION
    else:
        return SymbolCategory.VARIABLE

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
            return e(l, tS) ^ e(r, tS)
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
        case UnaryOp("+", val):
            return +e(val, tS)
        case UnaryOp("-", val):
            return -e(val, tS)        

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
            category = determine_runtime_category(var_val)
            tS.define(name, var_val, category)  # binds in current scope
            return var_val

        case UpdateVar(var_name, value):
            val_to_assign = e(value, tS)
            category = determine_runtime_category(val_to_assign)
            tS.find_and_update(var_name, val_to_assign, category)
            return val_to_assign

        case CompoundAssignment(var_name, op, value):
            # Check if variable is fixed
            category = tS.lookup(var_name, cat=True)
            if category == SymbolCategory.FIXED:
                raise ValueError(f"Error: Cannot modify fixed variable '{var_name}'")
            prev_val = tS.lookup(var_name)
            new_val = e(BinOp(op[0], Number(str(prev_val)), value), tS)
            new_category = determine_runtime_category(new_val)
            tS.find_and_update(var_name, new_val, new_category)
            return new_val

        # FUNCTIONS ===========================================================================
        case FuncDef(funcDefName, funcDefParams, funcDefBody, funcDefScope):
            # tS.define(fusncName, (funcParams, funcBody, funcScope, isRec), SymbolCategory.FUNCTION)
            return (funcDefParams, funcDefBody, funcDefScope)

        case FuncCall(fn_name, fn_args):

            # SOME IN-BUILT FUNCTION CALLS ********
            if type(fn_name)==str and fn_name=="sort":
                if len(fn_args)<1:
                    raise ValueError("sort function requires at least one argument")

                arr = e(fn_args[0], tS)
                if not isinstance(arr, list):
                    raise TypeError(f"sort function expects an array, got {type(arr)}")
            
                # Check for optional second argument (reverse flag)
                reverse = False
                if len(fn_args) > 1:
                    reverse = e(fn_args[1], tS)
                    if not isinstance(reverse, bool):
                        raise TypeError(f"sort function's second argument must be a boolean, got {type(reverse)}")
                # Return sorted array
                try:
                    return sorted(arr, reverse=reverse)
                except TypeError:
                    # Handle mixed type arrays by converting to strings for comparison
                    return sorted(arr, key=str, reverse=reverse)

            if type(fn_name) == str and fn_name == "lower":
                if len(fn_args) != 1:
                    raise ValueError("lower() function requires exactly one argument")
                string_val = e(fn_args[0], tS)
                if not isinstance(string_val, str):
                    raise TypeError(f"lower() function expects a string, got {type(string_val)}")
                return string_val.lower()
            
            if type(fn_name) == str and fn_name == "upper":
                if len(fn_args) != 1:
                    raise ValueError("upper() function requires exactly one argument")
                string_val = e(fn_args[0], tS)
                if not isinstance(string_val, str):
                    raise TypeError(f"upper() function expects a string, got {type(string_val)}")
                return string_val.upper()
            
            if type(fn_name) == str and fn_name == "reverse":
                if len(fn_args) != 1:
                    raise ValueError("reverse() function requires exactly one argument")
                arr = e(fn_args[0], tS)
                if not isinstance(arr, list):
                    raise TypeError(f"reverse() function expects an array, got {type(arr)}")
                return list(reversed(arr))

            if type(fn_name) == str and fn_name == "unique":
                if len(fn_args) != 1:
                    raise ValueError("unique() function requires exactly one argument")
                arr = e(fn_args[0], tS)
                if not isinstance(arr, list):
                    raise TypeError(f"unique() function expects an array, got {type(arr)}")
                unique_arr = []
                seen = set()
                for item in arr:
                    if item not in seen:
                        seen.add(item)
                        unique_arr.append(item)
                return unique_arr

            if type(fn_name) == str and fn_name == "so":
                if len(fn_args) != 1:
                    raise ValueError("so() function expects exactly one argument")
                return bool(e(fn_args[0], tS))

            if type(fn_name) == str and fn_name == "num":
                if len(fn_args) != 1:
                    raise ValueError("num() function requires exactly one argument")
                val = e(fn_args[0], tS)
                if isinstance(val, (int, float)):
                    return val
                if isinstance(val, str):
                    try:
                        # Try converting to integer first
                        return int(val)
                    except ValueError:
                        try:
                            # Fallback to float conversion if integer conversion fails
                            return float(val)
                        except ValueError:
                            raise ValueError(f"Cannot convert {val} to a number")
                else:
                    raise TypeError("num() function expects a string or a number")

            if enable_cat_fn and type(fn_name) == str and fn_name == "cat":
                if len(fn_args) != 1:
                    raise ValueError("cat() requires exactly one argument")
                arg = fn_args[0]
                if not isinstance(arg, Variable):
                    raise TypeError("cat() argument must be a variable")
                return tS.lookup(arg.var_name, cat=True)

            # GENERAL FUNCTION CALLS ********
            # Step 1: Extract function body & adjust scope
            if (isinstance(fn_name, CallArr)):
                arr = tS.lookup(fn_name.xname)
                for i_expr in fn_name.index:
                    arr = arr[e(i_expr, tS)]
            
                (param_list, fn_body, parsedScope) = arr
                eval_scope = SymbolTable(parsedScope.parent)

            else:    
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
                """
                if variable/fn, pass by value
                if array, pass by reference
                """
                if param[1]==SymbolCategory.VARIABLE:
                    eval_scope.define(param[0], e(arg, tS), SymbolCategory.VARIABLE)
                elif param[1]==SymbolCategory.ARRAY:
                    eval_scope.define(param[0], e(arg, tS), SymbolCategory.ARRAY)
                elif param[1]==SymbolCategory.HASH:
                    eval_scope.define(param[0], e(arg, tS), SymbolCategory.HASH)

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

        # PROPERTY ACCESS AT RUNTIME===================
        case PropertyAccess(var_name, operation, args):
            # Get the actual value and determine its runtime type
            try:
                var_value = tS.lookup(var_name) # var_name: (value, category)
                # var_category = determine_runtime_category(var_value)

                # Handle operations for each runtime type
                if type(var_value)==list:
                    match operation:
                        case "Length":
                            return len(var_value)
                        case "PushFront":
                            if len(args) < 1:
                                raise ValueError(f"PushFront requires a value argument")
                            arg_value = e(args[0], tS)
                            var_value.insert(0, arg_value)
                            tS.find_and_update(var_name, var_value)
                            return var_value
                        case "PushBack":
                            if len(args) < 1:
                                raise ValueError(f"PushBack requires a value argument")
                            arg_value = e(args[0], tS)
                            var_value.append(arg_value)
                            tS.find_and_update(var_name, var_value)
                            return var_value
                        case "PopFront":
                            if len(var_value) == 0:
                                raise IndexError(f"Cannot PopFront from empty array")
                            value = var_value.pop(0)
                            tS.find_and_update(var_name, var_value)
                            return value
                        case "PopBack":
                            if len(var_value) == 0:
                                raise IndexError(f"Cannot PopBack from empty array")
                            value = var_value.pop()
                            tS.find_and_update(var_name, var_value)
                            return value
                        case "Clear":
                            var_value.clear()
                            tS.find_and_update(var_name, var_value)
                            return var_value
                        case "Insert":
                            if len(args) < 2:
                                raise ValueError("Insert requires index and value arguments")
                            idx = e(args[0], tS)
                            if not isinstance(idx, int):
                                raise TypeError("Index must be an integer for Insert operation")
                            val = e(args[1], tS)
                            var_value.insert(idx, val)
                            tS.find_and_update(var_name, var_value)
                            return var_value
  
                        case "Remove":
                            if len(args) < 1:
                                raise ValueError("Remove requires a value argument")
                            idx_to_remove = e(args[0], tS)
                            try:
                                var_value.pop(idx_to_remove)
                            except ValueError:
                                raise ValueError("Value not found in array")
                            tS.find_and_update(var_name, var_value)
                            return var_value

                        case "Slice":
                            # Supports 1 to 3 arguments: start, end, step
                            arg_len = len(args)
                            start = e(args[0], tS) if arg_len >= 1 and args[0] is not None else None
                            end   = e(args[1], tS) if arg_len >= 2 and args[1] is not None else None
                            step  = e(args[2], tS) if arg_len >= 3 and args[2] is not None else None
                            return var_value[start:end:step]

                        case _:
                            raise ValueError(f"Unknown operation '{operation}' for arrays")
                            
                # elif var_category == SymbolCategory.STRING:
                elif type(var_value)==str:
                    match operation:
                        case "Length":
                            return len(var_value)
                        case "PushFront":
                            if len(args) < 1:
                                raise ValueError("PushFront requires a value argument")
                            arg_value = str(e(args[0], tS))
                            var_value = arg_value + var_value
                            tS.find_and_update(var_name, var_value)
                            return var_value
                        case "PushBack":
                            if len(args) < 1:
                                raise ValueError("PushBack requires a value argument")
                            arg_value = str(e(args[0], tS))
                            var_value = var_value + arg_value
                            tS.find_and_update(var_name, var_value)
                            return var_value
                        case "PopFront":
                            if len(var_value) == 0:
                                raise IndexError("Cannot PopFront from an empty string")
                            char = var_value[0]
                            var_value = var_value[1:]
                            tS.find_and_update(var_name, var_value)
                            return char
                        case "PopBack":
                            if len(var_value) == 0:
                                raise IndexError("Cannot PopBack from an empty string")
                            char = var_value[-1]
                            var_value = var_value[:-1]
                            tS.find_and_update(var_name, var_value)
                            return char
                        case "Clear":
                            var_value = ""
                            tS.find_and_update(var_name, var_value)
                            return var_value
                        case "Insert":
                            if len(args) < 2:
                                raise ValueError("Insert requires index and value arguments")
                            idx = e(args[0], tS)
                            if not isinstance(idx, int):
                                raise TypeError("Index must be an integer for Insert operation")
                            insert_val = str(e(args[1], tS))
                            var_value = var_value[:idx] + insert_val + var_value[idx:]
                            tS.find_and_update(var_name, var_value)
                            return var_value
                        case "Remove":
                            if len(args) < 1:
                                raise ValueError("Remove requires a value argument")
                            substr = str(e(args[0], tS))
                            idx = var_value.find(substr)
                            if idx == -1:
                                raise ValueError("Value not found in string")
                            var_value = var_value[:idx] + var_value[idx+len(substr):]
                            tS.find_and_update(var_name, var_value)
                            return var_value
                        case "Slice":
                            arg_len = len(args)
                            start = e(args[0], tS) if arg_len >= 1 and args[0] is not None else None
                            end   = e(args[1], tS) if arg_len >= 2 and args[1] is not None else None
                            step  = e(args[2], tS) if arg_len >= 3 and args[2] is not None else None
                            return var_value[start:end:step]
                        
                        case _:
                            raise ValueError(f"Unknown operation '{operation}' for strings")
                            
                # elif var_category == SymbolCategory.HASH:
                elif type(var_value)==dict:
                    match operation:
                        case "Length":
                            return len(var_value)
                        case "Clear":
                            var_value.clear()
                            tS.find_and_update(var_name, var_value)
                            return var_value
                        case "Keys":
                            return list(var_value.keys())
                        case "Values":
                            return list(var_value.values())
                        case "Contains":
                            if len(args) < 1:
                                raise ValueError("Contains requires a key argument")
                            key = e(args[0], tS)
                            return key in var_value
                        case "Add":
                            if len(args) < 2:
                                raise ValueError(f"Add requires key and value arguments")
                            key = e(args[0], tS)
                            value = e(args[1], tS)
                            var_value[key] = value
                            tS.find_and_update(var_name, var_value)
                            return var_value
                        case "Remove":
                            if len(args) < 1:
                                raise ValueError(f"Remove requires a key argument")
                            key = e(args[0], tS)
                            if key in var_value:
                                del var_value[key]
                            tS.find_and_update(var_name, var_value)
                            return var_value
                        # Add other hash operations as needed
                        case _:
                            raise ValueError(f"Unknown operation '{operation}' for hashes")
                            
                else:
                    raise TypeError(f"Operation '{operation}' not supported for type {type(var_value)}")
            except NameError:
                raise NameError(f"Variable '{var_name}' not found")

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
            lookedup = tS.lookup(xname)
            if type(lookedup)==str:
                index = indices[0]
                string_val = lookedup
                if not isinstance(string_val, str):
                    raise TypeError(f"AssignStringVal operation not supported for type {type(string_val)}")
                idx = e(index, tS)
                if not (0 <= idx < len(string_val)):
                    raise IndexError(f"Index {idx} out of bounds for string: {xname}")
                val = e(value, tS)
                string_val = string_val[:idx] + val + string_val[idx + 1 :]
                tS.find_and_update(xname, string_val)
                return string_val
            else:
                arr = lookedup
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

            evaluated_template = re.sub(r'\{(.*?)\}', evaluate_expression, template)
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
                type(None): "None",
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

    prog = """

"""

    parsed, gS = parse(prog, SymbolTable())
    print("------")
    pprint(parsed)
    print("------")
    pprint(gS.table)

    print("------")
    print("Program Output: ")
    execute(prog)
