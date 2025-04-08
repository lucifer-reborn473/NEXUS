from parser import *
from scope import SymbolCategory, SymbolTable
import copy

# ==========================================================================================
# ==================================== (TREE-WALK) EVALUATOR ===============================

def e(tree: AST, tS) -> Any:
    match tree:
        case Number(n):
            return int(n)
        case String(s):
            return s
        case Boolean(b):
            return b
        case Variable(v):
            return tS.lookup(v)
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
        case BinOp("^", l, r):
            return e(l, tS) ** e(r, tS)
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

        case FuncDef(_funcName, _funcParams, _funcBody, _funcScope):
            # just return
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
            # not needed (freed implicitly when the function returns)
            # for param in param_list:
            #     eval_scope.define(param, None, SymbolCategory.VARIABLE)

            return ans

        case Statements(statements):
            result = None
            for stmt in statements:
                result = e(stmt, tS)
            return result

        # Conditional
        case If(cond, then_body, else_body, tS_cond):
            ans = None
            tS_cond.parent = tS
            if e(cond, tS_cond):
                ans = e(then_body, tS_cond)
            elif else_body is not None:
                ans = e(else_body, tS_cond)
            return ans

        # Display
        case Display(val):
            return print(e(val, tS), end="")

        case DisplayL(val):
            return print(e(val, tS))

        case CompoundAssignment(var_name, op, value):
            prev_val = tS.lookup(var_name)
            new_val = e(BinOp(op[0], Number(prev_val), value), tS)
            tS.find_and_update(var_name, new_val)
            return new_val

        case VarBind(name, dtype, value, category):
            var_val = e(value, tS)
            tS.define(name, var_val, category)# binds in current scope
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
            tS_while.parent = tS
            while e(cond, tS_while):
                for stmt in body.statements:
                    e(stmt, tS_while)

        case ForLoop(init, cond, incr, body, tS_for):
            tS_for.parent = tS
            e(init, tS_for)
            while e(cond, tS_for):
                loop_should_break = False
                for stmt in body.statements:
                    e(stmt, tS_for)
                e(incr, tS_for)

        case BreakOn():
            return BreakOn()

        case MoveOn():
            return MoveOn()

def execute(prog):
    lines, tS = parse(prog)
    for line in lines.statements:
        e(line, tS)

# =========================================================================================================
if __name__ == "__main__":

    prog = """

""" 

# =====================================================================

    parsed, gS = parse(prog)
    print("------")
    pprint(parsed)
    print("------")
    pprint(gS.table)

    print("------")
    print("Program Output: ")
    execute(prog)
