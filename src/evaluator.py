from parser import *
from context import Context

# ==========================================================================================
# ==================================== (TREE-WALK) EVALUATOR ===============================

context = Context() # context as a global variable

def e(tree: AST, tS) -> Any:
    match tree:
        case Number(n):
            return int(n)
        case String(s):
            return s
        case Variable(v):
            # if context.has_variable(v):
            #     return context.get_variable(v).value
            # else:
            #     raise NameError(f"name '{v}' defined nhi hai")

            if v in tS.table:
                return tS.table[v]
            else:
                raise NameError(f"name '{v}' defined nhi hai")
        
        case FuncDef(funcName, funcParams, funcBody, funcScope):
            tS.table[funcName] = (funcParams, funcBody, funcScope)
            # add function definition to context
            # dtype = None # kept None for now
            # context.add_variable(funcName, (funcParams, funcBody), dtype)

        case FuncCall(funcName, funcArgs):
            # evaluate the function call

            """ 
            Step 1: Extract function body
            Step 2: Put argument values into function's scope
            Step 3: Evaluate the function body
            Step 4: Pop the arg values from the function's scope (don't delete the scope table)
            """ 

            # (funcParams, funcBody) = context.get_variable(funcName).value                 # Step 1
            (funcParams, funcBody, funcScope) = tS.table[funcName]

            for i in range(len(funcParams)):                                                # Step 2
                # context.add_variable(funcParams[i].var_name, param_values[funcParams[i].var_name], dtype)
                funcScope.table[funcParams[i].var_name] = e(funcArgs[i]) 


            for stmt in funcBody.statements:                                                # Step 3
                ans = e(stmt, funcScope)

            for i in range(len(funcParams)):
                # context.remove_variable(param.var_name)                                   # Step 4
                funcScope.table[funcParams[i].var_name] = None

            return ans
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
        # Conditional
        case If(cond, sat, else_):
            return e(sat, tS) if e(cond, tS) else e(else_, tS)
        # Display
        case Display(val):
            return print(e(val, tS))
        # Variables (evaluates to value)
        case CompoundAssignment(var_name, op, value):
            var_value = tS.table[var_name]
            var_value_updated = e(BinOp(op[0], Number(var_value), value), tS)
            tS.table[var_name] = var_value_updated
            # var_value = context.get_variable(var_name).value
            # var_value_updated = e(BinOp(op[0], Number(var_value), value), tS)
            # context.update_variable(var_name, var_value_updated)
            # return context # temporary return value -> will be removed later
            return var_value_updated
        case Binding(name, dtype, value):
            var_val = e(value, tS)
            tS.table[name] = var_val
            # context.add_variable(name, value, dtype)
            return var_val
            # return context # temporary return value -> will be removed later

if __name__ == "__main__":

    # # expression=" (5-4)*5+ (8-2)/3"
    # # print(parse(expression))
    # # print(e(parse(expression)))
    # # simple_exp=" 3 *(3+1*(4-1)) /2"
    # # simple_exp=" -3 + 7 + (2+8)/5 - (2*(4-3))"
    # # print(parse(simple_exp))
    # # print(e(parse(simple_exp)))
    # # sample_exp="if 2 < 3 then 0 end"
    # # print(parse("if 2 < 3 then 0+5 else 1*6 end"))
    # # print(e(parse("if 2 < 3 then 0+5 else 1*6 end")))
    # # expr = "display 2+1 "
    # # expr = "display 0<= 1 >=2 "
    # expr = " display( var integer x= 3+ 7 -1);"
    # compound_assignment= "display (x-=2);"
    # for t in lex(expr):
    #     print(t)
    # # t = peekable(lex(expr))
    # # print(t.peek(None))
    # # next(t)
    # # print(t.peek(None))
    # print("\nParsed expression:")
    # print(parse(expr))
    # print("\nEvaluated expression:")
    # e(parse(expr),context)
    # for t in lex(compound_assignment):
    #     print(t)
    # print("\nParsed expression:")
    # print(parse(compound_assignment))
    # print("\nEvaluated expression:")
    # e(parse(compound_assignment),context)

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
        for stmt in parse(prog).statements:
            e(stmt)
    # ========================================================

#     prog = """
# var integer a = 2;
# display a+1;
# """

    prog = """
    var a = 112910;
    var isEven = if (a%2==0) then ("True") else ("False") end;
    display isEven;
""" #! Error (True considered as variable instead of Boolean)

#     prog = """
# var a = 2;
# func foo(v): {
#     v = v+2;
# };
# display foo(3);
# display a;
# """ #! infinite loop

    prog = """
fn fib(a) {
    display "---";
    display a;
    if (a==1 or a==2) then (1) else (fib((a-1)) + fib((a-2))) end;
};
display fib(15);
""" #! Error in context/scoping

    """ nth-Fibonacci
    1,2,3,4,5,6,7
    1,1,2,3,5,8,13
    """

    prog ="""
    var a= char (66);
    display a;
    var b= ascii("A");
    display b;
    var c= char (ascii('x') + ascii (char(1)));
    display c;
"""

    prog = """
var a = 20;
fn foo(x) {
    x+2;
};
display foo(a);
""" # 22


    for t in lex(prog):
        print(t)
    
    # for t in lex(prog):
    #     print(t)

    print("------")
    parsed, gS= parse(prog)
    pprint(parsed)
    pprint(gS.table)
    # pprint(parsed.statements[2].funcScope.table)
    # pprint(parse(prog)) # List[AST]

    print("------")
    print("Program Output: ")
    # execute(prog)

    print(e(parsed, gS))

