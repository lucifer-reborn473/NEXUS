from parser import *

# ==========================================================================================
# ==================================== (TREE-WALK) EVALUATOR ===============================

context = Context() # context as a global variable

def e(tree: AST) -> Any:
    match tree:
        case Number(n):
            return int(n)
        case String(s):
            return s
        case Variable(v):
            if context.has_variable(v):
                return context.get_variable(v).value
            else:
                raise NameError(f"name '{v}' defined nhi hai")
        
        case FuncDef(funcName, funcParams, funcBody):
            # add function definition to context
            dtype = None # kept None for now
            context.add_variable(funcName, (funcParams, funcBody), dtype)

        case FuncCall(funcName, funcArgs):
            # evaluate the function call

            """ 
            Step 1: Extract function body
            Step 2: Put argument values into context
            Step 3: Evaluate the function body
            Step 4: Pop the arg values from context
            """ # Reference: Compiler Github page (Prof Balagopal Komarath)

            (funcParams, funcBody) = context.get_variable(funcName).value               # Step 1
            dtype = None
            for i in range(len(funcParams)):
                context.add_variable(funcParams[i].var_name, e(funcArgs[i]), dtype)     # Step 2
            
            for stmt in funcBody.statements:                                            # Step 3
                ans = e(stmt)

            for i in range(len(funcParams)):
                context.remove_variable(funcParams[i].var_name)                         # Step 4

            return ans
    
        # Operators
        case BinOp("+", l, r):
            return e(l) + e(r)
        case BinOp("*", l, r):
            return e(l) * e(r)
        case BinOp("-", l, r):
            return e(l) - e(r)
        case BinOp("÷", l, r):
            return e(l) / e(r)
        case BinOp("/", l, r):
            return e(l) / e(r)
        case BinOp("<", l, r):
            return e(l) < e(r)
        case BinOp(">", l, r):
            return e(l) > e(r)
        case BinOp("==", l, r):
            return e(l) == e(r)
        case BinOp("!=", l, r):
            return e(l) != e(r)
        case BinOp("<=", l, r):
            return e(l) <= e(r)
        case BinOp(">=", l, r):
            return e(l) >= e(r)
        case BinOp("%", l, r):
            return e(l) % e(r)
        
        case UnaryOp("~", val):
            return ~e(val)
        case UnaryOp("!", val):
            return not e(val)
        
        # Conditional
        case If(cond, sat, else_):
            return e(sat) if e(cond) else e(else_)
        
        # Display
        case Display(val):
            return print(e(val))
        
        # Variables (evaluates to value)
        case CompoundAssignment(var_name, op, value):
            var_value = context.get_variable(var_name).value
            var_value_updated = e(BinOp(op[0], Number(var_value), value))
            context.update_variable(var_name, var_value_updated)
            # return context  # temporary return value -> will be removed later
            return var_value_updated
        
        case Binding(name, dtype, value):
            value = e(value)
            context.add_variable(name, value, dtype)
            return value
            # return context  # temporary return value -> will be removed later

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
func fib(a): {
    if (a==1 or a==2) then (1) else (fib(a-1) + fib(a-2)) end;
};
display fib(6);
""" # Error

    prog = """
    var a = 19;
    var isEven = if (a%2==0 or b==2) then (True) else (False) end;
""" # Error


    # for t in lex(prog):
    #     print(t)

    # print("------")
    pprint(parse(prog)) # List[AST]

    # print("------")
    # print("Program Output: ")
    # execute(prog)
