from more_itertools import peekable
from typing import Optional, Any, List,Tuple
from pprint import pprint
from lexer import *
from scope import SymbolTable, SymbolCategory

# ==========================================================================================
# ==================================== PARSER ==============================================


class AST:
    """
    Abstract Syntax Tree (AST) class.

    This class represents the abstract syntax tree used in the compiler.
    It serves as a base class for all nodes in the AST.
    """

    pass

class ABT: #unused for the time being
    """
    ABT (Abstract Binding Tree) class.

    This class represents an abstract binding tree used in the compilation process.
    It is designed to handle the structure and operations related to the binding of
    variables and expressions in a compiler.
    """
    pass

@dataclass
class VarBind(AST): # for variable binding
    var_name: str
    dtype: Optional[str]
    val: AST
    category : SymbolCategory

@dataclass
class Variable(AST):
    var_name: str

@dataclass
class BinOp(AST):
    op: str
    left: AST
    right: AST

@dataclass
class UnaryOp(AST):
    op: str
    val: AST

@dataclass
class CallArr(AST):
    xname: str
    index: AST

@dataclass
class PushFront(AST):
    xname: str
    val: AST

@dataclass
class PushBack(AST):
    xname: str
    val: AST

@dataclass
class PopFront(AST):
    xname: str

@dataclass
class PopBack(AST):
    xname: str

@dataclass
class AssigntoArr(AST):
    xname: str
    index: AST
    val: AST
@dataclass
class Array(AST):
    val : List[AST]

@dataclass
class Hash(AST):
    val: List[Tuple[AST]]

@dataclass
class CallHashVal(AST):
    name: str
    key : AST

@dataclass 
class AddHashPair(AST):
    name: str
    key: AST
    val: AST

@dataclass
class RemoveHashPair(AST):
    name: str
    key : AST

@dataclass
class AssignHashVal(AST):
    name: str
    key : AST
    new_val: AST

@dataclass
class AssignFullArray(AST):
    xname: str
    val: List[AST]

@dataclass
class InsertAt(AST):
    xname: str
    index: AST
    val: AST

@dataclass
class RemoveAt(AST):
    xname: str
    index: AST

@dataclass
class GetLength(AST):
    xname: str

@dataclass
class ClearArray(AST):
    xname: str

@dataclass
class Number(AST):
    val: str

@dataclass
class String(AST):
    val: str

@dataclass
class Boolean(AST):
    val: bool

@dataclass
class Display(AST):
    val: Any

@dataclass
class DisplayL(AST):
    val: Any

@dataclass
class Break(AST):
    pass

@dataclass
class CompoundAssignment(AST):
    var_name: str
    op: str
    val: AST

@dataclass
class WhileLoop(AST):
    condition: AST 
    body: AST
    whileScope: Any

@dataclass
class Feed(AST):
    msg: AST

@dataclass
class Repeat(AST):
    times : AST
    body: AST
    repeatScope: Any

@dataclass
class ForLoop(AST):
    initialization: AST 
    condition: AST
    increment: AST
    body: AST
    forScope: Any

@dataclass
class BreakOut(AST):
    pass

@dataclass
class MoveOn(AST):
    pass

@dataclass
class AssignToVar(AST): # through assignment operator
    var_name: str
    val: AST

@dataclass
class If(AST):
    c: AST
    t: Any
    e: Any
    condScope: Any

@dataclass
class Statements:
    statements: List[AST]

@dataclass
class FuncDef(AST):
    funcName: str
    funcParams: List[Any]  # list of variables
    funcBody: List[AST]         # assumed body is one-liner expression # will use {} for multiline
    funcScope: Any              # static scoping (scope is tied to function definition and not its call)

@dataclass 
class FuncCall(AST):
    funcName: str               # function name as a string
    funcArgs: List[AST]         # takes a list of expressions

@dataclass
class FormatString(AST):
    template: str
    variables: List[str]

@dataclass
class TypeCast(AST):
    dtype: str
    val: AST

@dataclass
class MathFunction(AST):
    funcName: str
    arg: List[AST]

@dataclass
class TypeOf(AST):
    value : AST
# ==========================================================================================

def map_type(value):
    if isinstance(value, Array):
        return SymbolCategory.ARRAY
    elif isinstance(value, Hash):
        return SymbolCategory.HASH
    elif isinstance(value, (FuncCall, FuncDef)):
        return SymbolCategory.FUNCTION
    else:
        return SymbolCategory.VARIABLE
#==========================================================================================
def parse(s: str) -> List[AST]:

    t = peekable(lex(s))

    def expect(what: Token):
        if t.peek(None) == what:
            next(t)
            return
        raise SyntaxError(f"Expected {what} got {t.peek(None)}")
    
    def expect_any(expected_tokens: list[Token]):
        next_token = t.peek(None)  
        if next_token.o in expected_tokens:
            next(t)  
            return
        raise SyntaxError(f"Expected one of {expected_tokens}, but got {next_token}")

    

    def parse_program(thisScope=None):
        if thisScope is None:
            thisScope = SymbolTable()  # forms the global scope

        statements = []
        while t.peek(None) is not None:
            if isinstance(t.peek(None), RightBraceToken):  # function body parsing done
                break
            match t.peek(None):
                case KeywordToken("while"):
                    stmt, thisScope = parse_while(thisScope)
                case KeywordToken("for"):
                    stmt, thisScope = parse_for(thisScope)
                case KeywordToken("repeat"):
                    stmt, thisScope = parse_repeat(thisScope)
                case _:
                    stmt, thisScope = parse_display(thisScope)

            statements.append(stmt)  # collection of parsed statements

        return Statements(statements), thisScope  # Return a list of parsed statements + scope


    def parse_while(tS):
        """
        Parse a while loop.
        Syntax: while (condition) { statements }
        """
        match t.peek(None):
            case KeywordToken("while"):
                next(t)
                expect(LeftParenToken()) 
                tS_while = SymbolTable(tS)
                condition = parse_var(tS_while)[0]
                expect(RightParenToken()) 
                expect(LeftBraceToken()) 
                body, tS_while = parse_program(tS_while)  
                expect(RightBraceToken()) 
                return WhileLoop(condition, body, tS_while), tS
            case _:
                raise SyntaxError("Invalid syntax for while loop")

    def parse_for(tS):
        """
        Parse a for loop.
        Syntax: for (initialization; condition; increment) { statements }
        """
        match t.peek(None):
            case KeywordToken("for"):
                next(t)
                expect(LeftParenToken())
                tS_for = SymbolTable(tS) # new scope for tS
                initialization, tS_for = parse_var(tS_for)
                expect(SemicolonToken())
                condition = parse_var(tS_for)[0]
                expect(SemicolonToken())
                increment, tS_for = parse_var(tS_for)
                expect(RightParenToken())
                expect(LeftBraceToken())
                body, tS_for = parse_program(tS_for)
                expect(RightBraceToken())
                return ForLoop(initialization, condition, increment, body, tS_for), tS # no change in tS
            case _:
                raise SyntaxError("Invalid syntax for for loop")

    def parse_repeat(tS):
        """
        Parse a repeat loop.
        Syntax: repeat (times) { statements }
        """
        match t.peek(None):
            case KeywordToken("repeat"):
                next(t)
                expect(LeftParenToken())
                tS_repeat = SymbolTable(tS)
                times = parse_var(tS_repeat)[0]  # Parse the number of repetitions
                expect(RightParenToken())
                expect(LeftBraceToken())
                body, tS_repeat = parse_program(tS_repeat)  # Parse the body of the loop
                expect(RightBraceToken())
                return Repeat(times, body, tS_repeat), tS
            case _:
                raise SyntaxError("Invalid syntax for repeat loop")

    def parse_display(tS):  # display value/output
        (ast, tS) = parse_var(tS)
        while True:
            match t.peek(None):
                case KeywordToken("display"):
                    next(t)
                    ast = Display(parse_var(tS)[0])
                case KeywordToken("displayl"):
                    next(t)
                    ast = DisplayL(parse_var(tS)[0])
                case SemicolonToken():
                    next(t)
                    return ast, tS
                case _:
                    return ast, tS
    
    def parse_var(tS):  # for `var` declaration
        def parse_dtype_and_name():
            """Parse the data type and variable name."""
            dtype = None
            if isinstance(t.peek(None), TypeToken):
                dtype = t.peek(None).type_name
                next(t)
            if isinstance(t.peek(None), VarToken):
                name = t.peek(None).var_name
                if tS.inScope(name):
                    print(f"Error! Variable `{name}` is already declared. Can't declare again.")
                    exit()
                next(t)
                return dtype, name
            else:
                print("Syntax Error! Expected a variable name.")
                exit()

        def parse_value():
            """Parse the value of the variable."""
            if isinstance(t.peek(None), SemicolonToken):
                return None
            expect(OperatorToken("="))
            if isinstance(t.peek(None), SemicolonToken):
                print(f"Syntax Error! Used `;` after `=` for identifier `{name}`")
                exit()
            return parse_var(tS)[0]

        ast = parse_update_var(tS)
        while True:
            match t.peek(None):
                case KeywordToken("var"):
                    next(t)
                    dtype, name = parse_dtype_and_name()
                    value = parse_value()
                    category=map_type(value)
                    ast = VarBind(name, dtype, value,category)
                    tS.define(name,None,category)
                case KeywordToken("fixed"):  # Add this case
                    next(t)
                    # Check if 'var' follows 'fixed'
                    if not isinstance(t.peek(None), KeywordToken) or t.peek(None).kw_name != "var":
                        print("Syntax Error! Expected 'var' after 'fixed'")
                        exit()
                    next(t)  # Consume 'var'
                    dtype, name = parse_dtype_and_name()
                    value = parse_value()
                    if value is None:
                        print(f"Error! Fixed variable `{name}` must be initialized.")
                        exit()
                    category = SymbolCategory.FIXED  # Use FIXED category
                    ast = VarBind(name, dtype, value, category)
                    tS.define(name, None, category)
                case _:
                    return ast, tS

                
    def parse_update_var(tS): # for updating var
        ast = parse_if(tS)
        while True:
            match t.peek(None):
                case OperatorToken(op):
                    var_name = ast.var_name
                    next(t)
                    value = parse_var(tS)[0]
                    ast = CompoundAssignment(var_name,op,value) if op in compound_assigners else AssignToVar(var_name, value)
                case _:
                    return ast

                # case VarToken(var_name):
                #     next(t)
                #     if isinstance(t.peek(None),OperatorToken):
                #         op = t.peek(None).o 
                #         next(t)
                #         value = parse_var(tS)[0]
                #         ast = CompoundAssignment(var_name,op,value) if op in compound_assigners else AssignToVar(var_name, value)
                #     else:
                #         return ast #! use?
                # case _ :
                #     return ast

    def parse_if(tS):
        match t.peek(None):
            case KeywordToken("if"):
                next(t)
                tS_cond = SymbolTable(tS)
                cond = parse_var(tS_cond)[0]
                expect(KeywordToken("then"))
                
                if isinstance(t.peek(None), LeftBraceToken):
                    next(t)  
                    then_body, tS_cond = parse_program(tS_cond)
                    expect(RightBraceToken()) 
                else:
                    then_body = parse_display(tS_cond)[0]

                # Optional else
                if not (isinstance(t.peek(None), KeywordToken) and t.peek(None).kw_name == "else"):
                    else_body = None
                else:
                    next(t)  
                    if isinstance(t.peek(None), LeftBraceToken):
                        next(t)  
                        else_body, tS_cond = parse_program(tS_cond)
                        expect(RightBraceToken())
                    else:
                        else_body = parse_display(tS_cond)[0]
                
                # `end` is a must
                expect(KeywordToken("end"))

                return If(cond, then_body, else_body, tS_cond)
            case _:
                return parse_logic(tS)

    def parse_logic(tS):
        ast = parse_bitwise(tS)
        while True:
            match t.peek(None):
                case KeywordToken("and"):
                    next(t)
                    ast = BinOp("and", ast, parse_bitwise(tS))
                case KeywordToken("or"):
                    next(t)
                    ast = BinOp("or", ast, parse_bitwise(tS))
                case KeywordToken("not"):
                    next(t)
                    ast = UnaryOp("not", parse_bitwise(tS))
                case _:
                    return ast

    def parse_bitwise(tS):
        ast = parse_cmp(tS)
        while True:
            match t.peek(None):
                case OperatorToken("&"):
                    next(t)
                    ast = BinOp("&", ast, parse_cmp(tS))
                case OperatorToken("|"):
                    next(t)
                    ast = BinOp("|", ast, parse_cmp(tS))
                case OperatorToken("^"):
                    next(t)
                    ast = BinOp("^", ast, parse_cmp(tS))
                case OperatorToken("~"):
                    next(t)
                    ast = UnaryOp("~", parse_cmp(tS))
                case _:
                    return ast

    def parse_cmp(tS):
        ast = parse_shift(tS)
        while True:
            match t.peek(None):
                case OperatorToken("<"):
                    next(t)
                    ast = BinOp("<", ast, parse_shift(tS))
                case OperatorToken(">"):
                    next(t)
                    ast = BinOp(">", ast, parse_shift(tS))
                case OperatorToken("=="):
                    next(t)
                    ast = BinOp("==", ast, parse_shift(tS))
                case OperatorToken("!="):
                    next(t)
                    ast = BinOp("!=", ast, parse_shift(tS))
                case OperatorToken("<="):
                    next(t)
                    ast = BinOp("<=", ast, parse_shift(tS))
                case OperatorToken(">="):
                    next(t)
                    ast = BinOp(">=", ast, parse_shift(tS))
                case _:
                    return ast
                             
    def parse_shift(tS):
        ast = parse_add(tS)
        while True:
            match t.peek(None):
                case OperatorToken("<<"):
                    next(t)
                    ast = BinOp("<<", ast, parse_add(tS))
                case OperatorToken(">>"):
                    next(t)
                    ast = BinOp(">>", ast, parse_add(tS))
                case _:
                    return ast

    def parse_add(tS):
        ast = parse_sub(tS)
        while True:
            match t.peek(None):
                case OperatorToken("+"):
                    next(t)
                    ast = BinOp("+", ast, parse_sub(tS))
                case _:
                    return ast
                
    def parse_sub(tS):
        ast = parse_mul(tS)
        while True:
            match t.peek(None):
                case OperatorToken("-"):
                    next(t)
                    ast = BinOp("-", ast, parse_mul(tS))
                case _:
                    return ast


    def parse_mul(tS):
        ast = parse_modulo(tS)
        while True:
            match t.peek(None):
                case OperatorToken("*"):
                    next(t)
                    ast = BinOp("*", ast, parse_modulo(tS))
                case _:
                    return ast
    def parse_modulo(tS):
        ast =parse_div_slash(tS)
        while True:
            match t.peek(None):
                case OperatorToken("%"):
                    next(t)
                    ast=BinOp("%",ast,parse_div_slash(tS))
                case _:
                    return ast

    def parse_div_slash(tS):
        ast = parse_div_dot(tS)
        while True:
            match t.peek(None):
                case OperatorToken("/"):
                    next(t)
                    ast = BinOp("/", ast, parse_div_dot(tS))
                case _:
                    return ast

    def parse_div_dot(tS):
        ast = parse_exp(tS)
        while True:
            match t.peek(None):
                case OperatorToken("÷"):
                    next(t)
                    ast = BinOp("÷", ast, parse_exp(tS))
                case _:
                    return ast
                
    def parse_exp(tS):
        ast = parse_ascii_char(tS)
        if isinstance(t.peek(None), OperatorToken) and t.peek(None).o == "**":
            next(t)
            right = parse_exp(tS)
            ast = BinOp("**", ast, right)
        return ast

                
    def parse_ascii_char(tS):
        ast = parse_typecast(tS)
        while True:
            match t.peek(None):
                case KeywordToken("char"):
                    next(t)
                    expect(LeftParenToken())
                    value = parse_if(tS)    
                    expect(RightParenToken())
                    ast = UnaryOp("char", value)
                case KeywordToken("ascii"):
                    next(t)
                    expect(LeftParenToken())
                    value = parse_if(tS)
                    expect(RightParenToken())
                    ast = UnaryOp("ascii", value)
                case _:
                    return ast
    def parse_typecast(tS):
        ast = parse_array_dict(tS)
        while True:
            match t.peek(None):
                case TypeToken(dtype):
                    next(t)
                    expect(LeftParenToken())
                    value = parse_var(tS)[0]
                    expect(RightParenToken())
                    ast = TypeCast(dtype, value)
                case _:
                    return ast
    def parse_array_dict(tS):
        ast=parse_math(tS)
        while True:
            match t.peek(None):
                case LeftSquareToken(): # parse list of elements
                    next(t)
                    elements = []
                    while not isinstance(t.peek(None), RightSquareToken):
                        elements.append(parse_var(tS)[0])
                        if isinstance(t.peek(None), CommaToken):
                            next(t)
                    expect(RightSquareToken())

                    ast = Array(elements)
                case LeftBraceToken(): # parse list of dictionary
                    next(t)
                    elements= []
                    while not isinstance(t.peek(None), RightBraceToken):
                        key=parse_var(tS)[0]
                        expect(ColonToken())
                        val = parse_var(tS)[0]
                        elements.append((key,val))
                        if isinstance(t.peek(None), CommaToken):
                            next(t)
                    expect(RightBraceToken())

                    ast=Hash(elements)
                case _:
                    return ast
    def parse_math(tS):
        ast = parse_input(tS)
        while True:
            match t.peek(None):
                case MathToken(m):
                    next(t)
                    if isinstance(t.peek(None), LeftParenToken):
                        next(t)
                        args = []
                        while not isinstance(t.peek(None), RightParenToken):
                            args.append(parse_var(tS)[0])
                            if isinstance(t.peek(None), CommaToken):
                                next(t)
                        expect(RightParenToken())
                    else:
                        args = []
                    ast = MathFunction(m, args)
                case _:
                    return ast
    def parse_input(tS):
        ast=parse_string(tS)
        while True:
            match t.peek(None):
                case KeywordToken("feed"):
                    next(t)
                    expect(LeftParenToken())
                    msg=parse_string(tS)
                    if (msg is None):
                        msg=String("FEED:")
                    expect(RightParenToken())
                    ast = Feed(msg)
                case KeywordToken("typeof"):
                    next(t)
                    expect(LeftParenToken())
                    value = parse_var(tS)[0]
                    expect(RightParenToken())
                    ast = TypeOf(value)
                case _:
                    return ast
                
    def parse_string(tS): # while True may be included in future
        match t.peek(None):
            case StringToken(s):
                next(t)
                return String(s)
            case FstringToken(s):
                next(t)
                variables = []
                for var in s.split("{")[1:]:
                    var_name = var.split("}")[0]
                    variables.append(var_name)
                return FormatString(s, variables)
            case _:
                return parse_boolean(tS)
                            
    def parse_boolean(tS):
        match t.peek(None):
            case BooleanToken(b):
                next(t)
                return Boolean(b=="True")
            case _:
                return parse_func(tS)
    # def loop_parse(tS):
        # ast=parse_func(tS)
        # while True:
        #     match t.peek(None):
        #         case KeywordToken("loop"):
        #             next(t) # loop keyword detected move to next token
        #             cond=None
        #             if (t.peek(None) == LeftParenToken()): # loop condition starts
        #                 next(t)
        #                 cond=parse_logic(tS)[0]
        #                 expect(RightParenToken())
        #             expect (LeftBraceToken()) # loop body starts
        #             body = parse_var(tS)[0] # temporary 
        #             ast=Loop(cond,body)
        #         case _:
        #             return ast       
    def parse_func(tS): # Function definition and Function call
        ast = parse_brackets(tS)
        while True:
            match t.peek(None):
                case KeywordToken("fn"): # function declaration
                # case KeywordToken("fn") | KeywordToken("fnrec"): # function declaration
                    # if t.peek(None).kw_name == "fnrec":
                    #     isRec = True
                    # else:
                    #     isRec = False

                    next(t)
                    
                    if isinstance(t.peek(None), VarToken):
                        funcName = t.peek(None).var_name
                        next(t)
                    else:
                        print("Function name missing\nAborting")
                        exit()

                    if tS.inScope(funcName):
                        print(f"Error! Multiple declaration of function `{funcName}()` in the same scope (not allowed)")
                        exit()

                    expect(LeftParenToken())

                    # parse parameters
                    params = []
                    while isinstance(t.peek(None), VarToken):
                        params.append(t.peek(None).var_name)
                        next(t)
                        if isinstance(t.peek(None), CommaToken):
                            next(t) 
                        else:
                            expect(RightParenToken()) # parameter list end
                            break    
                    
                    if len(params)==0:
                        expect(RightParenToken()) # no parameters in the function declaration

                    tS_f = SymbolTable(tS) # Function Scope (with tS as parent scope)

                    # add param names to function scope
                    for var_name in params:
                        tS_f.define(var_name, None, SymbolCategory.VARIABLE)
                    
                    expect(LeftBraceToken()) # {
                    # function body begins
                    
                    # body = parse_var()
                    # bodyCode = []
                    # while not isinstance(t.peek(None), RightBraceToken):
                    #     stmt = parse_display()      # Parse current statement
                    #     bodyCode.append(stmt)       # collection of parsed statements
                    # body = Statements(bodyCode)     # list of parsed statements
                    # tS.define(funcName,None,SymbolCategory.FUNCTION)
                    # (body, tS_f) = parse_program(tS_f) # get updated tS_f
                    # next(t)
                    # ast = FuncDef(funcName, params, body, tS_f, isRec)
                    # # tS.table[funcName] = (params, body, tS_f, isRec)
                    # tS.define(funcName,(params,body,tS_f,isRec),SymbolCategory.FUNCTION)

                    (body, tS_f) = parse_program(tS_f) # get updated tS_f
                    next(t)
                    ast = FuncDef(funcName, params, body, tS_f)
                    tS.define(funcName, (params, body, tS_f), SymbolCategory.FUNCTION)
                
                # Function call
                case LeftParenToken(): # denotes the identifier is not a variable but a function call
                    # extract arguments
                    funcName = ast.var_name
                    funcArgs = []
                    next(t)
                    while True: 
                        match t.peek(None):
                            case CommaToken():
                                next(t)
                            case RightParenToken():
                                # function call ends
                                ast = FuncCall(funcName, funcArgs)
                                next(t)
                                return ast
                            case _:
                                # expect expression
                                expr = parse_var(tS)[0]
                                funcArgs.append(expr)
                
                case _:
                    return ast
                # parse_func() ends here
   

    def parse_brackets(tS):
        while True:
            match t.peek(None):
                case LeftParenToken():
                    next(t)
                    (ast, tS) = parse_display(tS)
                    match t.peek(None):
                        case RightParenToken():
                            next(t)
                            return ast
                        case _:
                            raise SyntaxError(f"Expected ')' got {t.peek(None)}")
                case _:
                    return call_vartoks(tS)
    
    def call_vartoks(tS): #handles all calls related to vartokens
        ast =parse_atom(tS)
        while True:
            match t.peek(None):
                case VarToken(v):
                    next(t)
                    if isinstance(t.peek(None), LeftParenToken):
                        # means a function call
                        return ast
                    category = tS.lookup(v, cat = True)
                    match category:
                        case SymbolCategory.VARIABLE:
                            ast = Variable(v)
                        case SymbolCategory.ARRAY:
                            if isinstance(t.peek(None), LeftSquareToken):  # array access
                                indices = []
                                while isinstance(t.peek(None), LeftSquareToken):
                                    next(t)
                                    indices.append(parse_var(tS)[0])
                                    expect(RightSquareToken())
                                
                                if (isinstance(t.peek(None), OperatorToken) 
                                    and t.peek(None).o == "="):  # assigning a new value
                                    next(t)
                                    value = parse_var(tS)[0]
                                    ast = AssigntoArr(v, indices, value)
                                else:  # accessing a given index
                                    ast = CallArr(v, indices)
                            elif isinstance(t.peek(None), DotToken):

                                next(t)
                                match t.peek(None):
                                    case KeywordToken("PushFront"):
                                        next(t)
                                        expect(LeftParenToken())
                                        val = parse_var(tS)[0]
                                        expect(RightParenToken())
                                        ast = PushFront(v, val)
                                        return ast
                                    case KeywordToken("PushBack"):
                                        next(t)
                                        expect(LeftParenToken())
                                        val = parse_var(tS)[0]
                                        expect(RightParenToken())
                                        ast=PushBack(v, val)
                                        return ast
                                    case KeywordToken("PopFront"):
                                        next(t)
                                        ast=PopFront(v)
                                        return ast
                                    case KeywordToken("PopBack"):
                                        next(t)
                                        ast=PopBack(v)
                                        return ast
                                    case KeywordToken("Length"):
                                        next(t)
                                        ast=GetLength(v)
                                        return ast
                                    case KeywordToken("Clear"):
                                        next(t)
                                        ast=ClearArray(v)
                                        return ast
                                    case KeywordToken("Insert"):
                                        next(t)
                                        expect(LeftParenToken())
                                        index = parse_var(tS)[0]
                                        expect(CommaToken())
                                        val = parse_var(tS)[0]
                                        expect(RightParenToken())
                                        ast = InsertAt(v, index, val)    
                                        return ast   
                                    case KeywordToken("Remove"):
                                        next(t)
                                        expect(LeftParenToken())
                                        index = parse_var(tS)[0]
                                        expect(RightParenToken())
                                        ast = RemoveAt(v, index)
                                        return ast
                                    case _:
                                        return ast
                            else:  # calling the whole array
                                ast = Variable(v)
                        case SymbolCategory.HASH:
                            if isinstance(t.peek(None), LeftSquareToken):
                                keys = []
                                while isinstance(t.peek(None), LeftSquareToken):
                                    next(t)
                                    keys.append(parse_var(tS)[0])
                                    expect(RightSquareToken())
                                if (isinstance(t.peek(None), OperatorToken) 
                                    and t.peek(None).o == "="):  # assigning a new value
                                    next(t)
                                    value = parse_var(tS)[0]
                                    ast = AssignHashVal(v, keys, value)  # Handle nested keys
                                else:
                                    ast = CallHashVal(v, keys)  # Handle nested keys
                            elif isinstance(t.peek(None), DotToken):
                                next(t)
                                match t.peek(None):
                                    case KeywordToken("Add"):
                                        next(t)
                                        expect(LeftParenToken())
                                        key = parse_var(tS)[0]
                                        expect(CommaToken())
                                        val = parse_var(tS)[0]
                                        expect(RightParenToken())
                                        ast = AddHashPair(v, key, val)
                                        return ast
                                    case KeywordToken("Remove"):
                                        next(t)
                                        expect(LeftParenToken())
                                        key = parse_var(tS)[0]
                                        expect(RightParenToken())
                                        ast = RemoveHashPair(v, key)
                                        return ast
                                    case _:
                                        return ast
                            else:
                                ast = Variable(v)
                        case _:
                            ast = Variable(v)
                case _:
                    return ast    
    
    def parse_atom(tS): #! while True may be included in future
        match t.peek(None):
            case NumberToken(n):
                next(t)
                return Number(n)
            case BreakToken():
                next(t)
                return Break()
            case BreakOutToken():
                next(t)
                return BreakOut()
            case MoveOnToken():
                next(t)
                return MoveOn()
            case VarToken(v):
                # next(t)
                return Variable(v)

    return parse_program()


if __name__ == "__main__":
   

   prog="""
    repeat (10){
        displayl 1;
    }
"""
   prog1="""
    
    
"""
   pprint(parse(prog1))


# def array_dot_operations(v, tS, ast):
#         next(t)
#         match t.peek(None):
#             case KeywordToken("PushFront"):
#                 next(t)
#                 expect(LeftParenToken())
#                 val = parse_var(tS)[0]
#                 expect(RightParenToken())
#                 ast = PushFront(v, val)
#             case KeywordToken("PushBack"):
#                 next(t)
#                 expect(LeftParenToken())
#                 val = parse_var(tS)[0]
#                 expect(RightParenToken())
#                 ast = PushBack(v, val)
#             case KeywordToken("PopFront"):
#                 next(t)
#                 ast = PopFront(v)
#             case KeywordToken("PopBack"):
#                 next(t)
#                 ast = PopBack(v)
#             case KeywordToken("Length"):
#                 next(t)
#                 ast = GetLength(v)
#             case KeywordToken("Clear"):
#                 next(t)
#                 ast = ClearArray(v)
#             case KeywordToken("Insert"):
#                 next(t)
#                 expect(LeftParenToken())
#                 index = parse_var(tS)[0]
#                 expect(CommaToken())
#                 val = parse_var(tS)[0]
#                 expect(RightParenToken())
#                 ast = InsertAt(v, index, val)
#             case KeywordToken("Remove"):
#                 next(t)
#                 expect(LeftParenToken())
#                 index = parse_var(tS)[0]
#                 expect(RightParenToken())
#                 ast = RemoveAt(v, index)
#             case _:
#                 return ast
#         return ast