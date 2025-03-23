from parser import *
from context import Context
import copy

# ==========================================================================================
# ==================================== (TREE-WALK) EVALUATOR ===============================

context = Context()  # context as a global variable


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
        case BinOp("not", l, _):  # Unary logical operator
            return not e(l, tS)
        case BinOp("~", l, _):  # Unary bitwise operator
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
            (funcParams, funcBody, funcScopeMain, isRec) = tS.lookup(funcName)  # Step 1
            funcScope = funcScopeMain.copy_scope() if isRec else funcScopeMain

            for i in range(len(funcParams)):  # Step 2
                funcScope.table[funcParams[i]] = e(funcArgs[i], tS)

            for stmt in funcBody.statements:  # Step 3
                ans = e(
                    stmt, funcScope
                )  #! every line in body is evaluated (always returns something)

            for i in range(len(funcParams)):
                funcScope.table[funcParams[i]] = None  # Step 4

            return ans  # after returning ans

        # Conditional
        # case If(cond, sat, else_):
        #     return e(sat, tS) if e(cond, tS) else e(else_, tS)
        
        case Statements(statements):
            result = None
            for stmt in statements:
                result = e(stmt, tS)
            return result

        case If(cond, then_expr, else_expr):
            if e(cond, tS):
                return e(then_expr, tS)
            else:
                return e(else_expr, tS) if else_expr is not None else None

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

        case VarBind(name, dtype, value):
            var_val = e(value, tS)
            tS.table[name] = var_val  # binds in current scope
            return var_val

        case BindArray(xname, atype, val):
            all_vals = list(map(lambda x: e(x, tS), val))
            tS.table[xname] = all_vals
            return all_vals
        case Array(xname, index):
            return tS.table[xname][e(index, tS)]
        case AssignToVar(var_name, value):
            val_to_assign = e(value, tS)
            tS.find_and_update(var_name, val_to_assign)
            return val_to_assign

        # Loops
        case WhileLoop(cond, body):
            while e(cond, tS):  # Evaluate the condition
                for stmt in body.statements:  # Execute the body
                    e(stmt, tS)

        case ForLoop(init, cond, incr, body):
            e(init, tS)  # Initialize the loop variable
            while e(cond, tS):  # Evaluate the condition
                for stmt in body.statements:  # Execute the body
                    e(stmt, tS)
                e(incr, tS)  # Increment the loop variable


if __name__ == "__main__":

    # # expr = "display 0<= 1 >=2 "
    # expr = " display( var integer x= 3+ 7 -1);"
    # compound_assignment= "display (x-=2);"
    # # loop <condition> then <statement> end
    # # int32 x=2

    # ========================================================
    # Loading the Program
    fileName = "src/sample-code.txt"
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

    prog2 = """
var a = "g-";
fnrec foo(x, i){
    if i==1 then var a = "l-" else "dummy" end;
    display x; display ", ";
    displayl i;
    if x==1 then "k" else a + foo(x-1, i+1) end;
}
displayl foo(5,1);
"""

    prog = """
fn foo(i){
    if i==1 then var a = 2 else 5 end;
}
displayl foo(2);
"""  #! why does funcScope contain `a`?

    prog2 = """
fn foo(i){
    if i==1 then a = 2 else 5 end;
}
displayl foo(2);
"""  #! here funcScope does not contain `a`

    prog = """
var a = 2;
var a = 100;
displayl a;
"""  #! should throw error

    #! check for redeclaration of function

    #! are arrays mutable?

    #! how arrays passed/returned from functions

    prog = """
displayl 2
displayl 3
"""  #! why only 3 printed (should be syntax error due to missing semicolons)

    #! add nil datatype (uninitialised variables, function return)

    prog = """
var a = 2++3;
displayl a;
"""  #! error handling missing (should be handled by TOPL & its grammar, instead of Python)

    #     prog = """
    # var a = 2^3
    # """ #! infinite loop

    #! array features in Project doc

    #! Visual separator for numbers (example: int x = 1_000_000 or 1`000`000)

    #! runs a program from .topl file extension (in terminal, we write `topl myprog.topl`)

    # parsed, gS = parse(prog)

    # print("------")
    # print("PARSED:")
    # pprint(parsed)

    # print("------")
    # print("TABLE:")
    # pprint(gS.table)

    # print("------")
    # print("Program Output: ")
    execute(prog)
