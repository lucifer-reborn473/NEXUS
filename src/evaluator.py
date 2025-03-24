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
            # if context.has_variable(v):
            #     return context.get_variable(v).value
            # else:
            #     raise NameError(f"name '{v}' defined nhi hai")
        
        case FuncDef(funcName, funcParams, funcBody, funcScope):
            # tS.table[funcName] = (funcParams, funcBody, funcScope)
            return 
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
            (funcParams, funcBody, funcScopeMain) = tS.lookup(funcName)
            funcScope = funcScopeMain.copy_scope()


            for i in range(len(funcParams)):                                                # Step 2
                # context.add_variable(funcParams[i].var_name, param_values[funcParams[i].var_name], dtype)
                funcScope.table[funcParams[i]] = e(funcArgs[i], tS) 


            for stmt in funcBody.statements:                                                # Step 3
                ans = e(stmt, funcScope) #! every line in body is evaluated (always returns something)

            for i in range(len(funcParams)):
                # context.remove_variable(param.var_name)                                   # Step 4
                funcScope.table[funcParams[i]] = None

            return ans # after returning ans 
        

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
            return print(e(val, tS), end = "")
       
        case DisplayL(val):
            return print(e(val, tS))

        case CompoundAssignment(var_name, op, value):
            prev_val = tS.lookup(var_name)
            new_val = e(BinOp(op[0], Number(prev_val), value), tS)
            tS.find_and_update(var_name, new_val)
            return new_val
            # var_value = context.get_variable(var_name).value
            # var_value_updated = e(BinOp(op[0], Number(var_value), value), tS)
            # context.update_variable(var_name, var_value_updated)
            # return context # temporary return value -> will be removed later
            # # else raise error
        
        case VarBind(name, dtype, value):
            var_val = e(value, tS)
            tS.table[name] = var_val # binds in current scope
            return var_val
            # context.add_variable(name, value, dtype)
            # return context # temporary return value -> will be removed later

        case BindArray(xname,atype,val):
            all_vals= list(map(lambda x: e(x,tS),val))
            tS.table[xname]=all_vals
            return all_vals
        case Array(xname,index):
            return tS.table[xname][e(index,tS)]
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
        lines, tS = parse(prog)
        for line in lines.statements:
            e(line, tS)
    # ========================================================


    prog ="""
var a= char (66);
displayl a;
var b= ascii("A");
displayl b;
var c= char (ascii('x') + ascii (char(1)));
displayl c;
""" # testing for char(), ascii()

    prog_y = """
var a = 112911;
var isEven = if a%2==0 then True else False end;
displayl isEven;
""" #! Error (True being considered as variable instead of Boolean)

    prog = """
fn fib(a) {
    if (a==1 or a==2) then 1 else fib(a-1) + fib(a-2) end;
};
displayl "----";
var x = 20;
displayl x;
displayl fib(x); 
""" # works!

    # Fibonacci calculator: https://www.calculatorsoup.com/calculators/discretemathematics/fibonacci-calculator.php

    prog = """
var x = 2;
fn foo(){
    var x = 300;
    x;
}
fn bar(x){
    x += 1000;
    x;
}
fn baz(x){
    if x<5 then foo() else bar(x) end;
}

displayl baz(4); /~ 300 ~/
displayl baz(6); /~ 1006 ~/
""" 

    prog2 = """
var x = 1000;
fn bar() {
    x;
}
fn foo() {
    var x = 100;
    bar();
}
displayl foo();
""" #! prints None (should be 1000)

    prog3 = """
var x = 1000;
fn foo() {
    var x = 100;
    fn bar() {
        x;
    }
    bar();
}
displayl foo();
""" #! prints None (should be 100)


    # for t in lex(prog):
    #     print(t)


    prog = """
    for (var i = 0; i < 10; i = i + 1) {
        display(i);
    }
    """

    prog = """
    var x = 0;
    while (x < 15) {
        displayl(x);
        x = x + 1;
    }
    """

#     print("Running prog")
#     execute(prog)
#     parsed, gS = parse(prog)
#     print("------")
#     print("PARSED:")
#     pprint(parsed)

#     print("------")
#     print("TABLE:")
#     pprint(gS.table)

#     print("------")
#     print("Program Output: ")
#     execute(prog)



    prog4 = """
    array integer a = [1, 2, 3, 4, 5];
    array b= [2,4,6,8,10];
    displayl a[2]; 
    var c= a[2]+b[2];
    displayl c;
    c=3;
    displayl c;
    displayl a;
"""
    for t in lex(prog):
        print(t)

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


