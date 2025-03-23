from parser import *
from context import Context
import copy

# ==========================================================================================
# ==================================== (TREE-WALK) EVALUATOR ===============================

context = Context() # context as a global variable

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
        case BinOp("not", l, _): # Unary logical operator
            return not e(l, tS)
        case BinOp("~", l, _): # Unary bitwise operator
            return ~e(l, tS)
        case UnaryOp("~", val):
            return ~e(val, tS)
        case UnaryOp("!", val):
            return not e(val, tS)
        case UnaryOp("ascii", val):
            return ord(e(val, tS))
        case UnaryOp("char", val):
            return chr(e(val, tS))
        
        case FuncDef(funcName, funcParams, funcBody, funcScope):
            # tS.table[funcName] = (funcParams, funcBody, funcScope)
            return 

        case FuncCall(funcName, funcArgs):
            # evaluate the function call
            """ 
            Step 1: Extract function body
            Step 2: Put argument values into function's scope
            Step 3: Evaluate the function body
            Step 4: Pop the arg values from the function's scope (don't delete the scope table)
            """ 
            (funcParams, funcBody, funcScopeMain, isRec) = tS.lookup(funcName)              # Step 1
            funcScope = funcScopeMain.copy_scope() if isRec else funcScopeMain


            for i in range(len(funcParams)):                                                # Step 2
                funcScope.table[funcParams[i]] = e(funcArgs[i], tS) 


            for stmt in funcBody.statements:                                                # Step 3
                ans = e(stmt, funcScope) #! every line in body is evaluated (always returns something)
            
            for i in range(len(funcParams)):
                funcScope.table[funcParams[i]] = None                                     # Step 4

            return ans # after returning ans 
       
        # Conditional
        case If(cond, sat, else_):
            return e(sat, tS) if e(cond, tS) else e(else_, tS)

        # Display
        case Display(val):
            return print(e(val, tS), end = "")
       
        case DisplayL(val):
            return print(e(val, tS))

        case CompoundAssignment(var_name, op, value):
            prev_val = tS.lookup(var_name)
            new_val = e(BinOp(op[0], Number(prev_val), value), tS)
            tS.find_and_update(var_name, new_val)
            return new_val
        
        case VarBind(name, dtype, value):
            var_val = e(value, tS)
            tS.table[name] = var_val # binds in current scope
            return var_val

        case AssignToVar(var_name, value):
            val_to_assign = e(value, tS)
            tS.find_and_update(var_name, val_to_assign)
            return val_to_assign

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
        with open(fileName, 'r') as file:
            prog = file.read()
    except FileNotFoundError:
        print(f"The file {fileName} was not found.")
    except IOError:
        print("An error occurred while reading the file.")
    
    def execute(prog):
        lines, tS = parse(prog)
        for line in lines.statements:
            e(line, tS)
    # ========================================================

    parsed, gS = parse(prog)
    
    print("------")
    print("PARSED:")
    pprint(parsed)

    print("------")
    print("TABLE:")
    pprint(gS.table)
    
    print("------")
    print("Program Output: ")
    execute(prog)