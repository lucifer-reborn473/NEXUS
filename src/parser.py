from more_itertools import peekable
from typing import Optional, Any, List,Tuple
from pprint import pprint
from lexer import *
from scope import SymbolTable, SymbolCategory

# ==========================================================================================
# ==================================== PARSER ==============================================

class SemanticError(Exception):
    pass

class RedeclarationError(SemanticError):
    pass

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
class Slice(AST):
    var_name: str
    start : Optional[AST]
    end : Optional[AST]
    step : Optional[AST]

@dataclass
class StringIdx(AST):
    var_name: str
    index: AST
 
@dataclass 
class AssignStringVal(AST):
    var_name: str
    index: AST
    value : AST

@dataclass 
class Sort(AST):
    var_name: str
    greater: Optional[AST]

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
class UpdateVar(AST): # through assignment operator
    var_name: str
    val: AST

@dataclass
class If(AST):
    c: AST
    t: Any
    e: Any
    condScope: Any

@dataclass
class Statements(AST):
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
    # elif isinstance(value, (FuncCall, FuncDef)):
    #     return SymbolCategory.FUNCTION
    elif isinstance(value,(String,FormatString)):
        return SymbolCategory.STRING
    else:
        return SymbolCategory.VARIABLE
#==========================================================================================
def parse(s: str, defS) -> List[AST]:

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

    

    # def parse_program(thisScope=None):
        # if thisScope is None:
        #     thisScope = SymbolTable()  # forms the global scope
    def parse_program(thisScope):

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
                    raise RedeclarationError(f"Multiple declaration of variable `{name}` in the same scope is not allowed")
                next(t)
                return dtype, name
            else:
                raise SyntaxError("Expected a variable name.")
                # print("Syntax Error! Expected a variable name.")
                # exit()

        def parse_value():
            """Parse the value of the variable."""
            if isinstance(t.peek(None), SemicolonToken):
                return None
            expect(OperatorToken("="))
            if isinstance(t.peek(None), SemicolonToken):
                raise SyntaxError(f"Used `;` after `=` for identifier `{name}`")
                # print(f"Syntax Error! Used `;` after `=` for identifier `{name}`")
                # exit()
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
                        raise SyntaxError("Expected 'var' after 'fixed'")
                        # print("Syntax Error! Expected 'var' after 'fixed'")
                        # exit()
                    next(t)  # Consume 'var'
                    dtype, name = parse_dtype_and_name()
                    value = parse_value()
                    if value is None:
                        raise SyntaxError(f"Fixed variable `{name}` must be initialized.")
                        # print(f"Error! Fixed variable `{name}` must be initialized.")
                        # exit()
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
                    ast = CompoundAssignment(var_name,op,value) if op in compound_assigners else UpdateVar(var_name, value)
                case _:
                    return ast

                # case VarToken(var_name):
                #     next(t)
                #     if isinstance(t.peek(None),OperatorToken):
                #         op = t.peek(None).o 
                #         next(t)
                #         value = parse_var(tS)[0]
                #         ast = CompoundAssignment(var_name,op,value) if op in compound_assigners else UpdateVar(var_name, value)
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
        #     
    def parse_func(tS): # Function definition and Function call
        ast = parse_brackets(tS)
        while True:
            match t.peek(None):
                case KeywordToken("fn"): # function declaration
                    next(t)    
                    if isinstance(t.peek(None), VarToken):
                        funcName = t.peek(None).var_name
                        next(t)
                    else:
                        raise SyntaxError("Function name missing.")

                    if tS.inScope(funcName):
                        raise RedeclarationError(f"Multiple declaration of function `{funcName}()` in the same scope is not allowed.")
                    
                    tS.define(funcName, None, SymbolCategory.FUNCTION) # add to scope
                    tS_f = SymbolTable(tS) # Function Scope (with tS as parent scope)

                    # parse parameters
                    expect(LeftParenToken())
                    params = []

                    while isinstance(t.peek(None), VarToken):
                        param_name = t.peek(None).var_name
                        next(t)
                        if isinstance(t.peek(None), LeftBraceToken):
                            next(t)
                            expect(RightBraceToken())
                            tS_f.define(param_name, None, SymbolCategory.HASH)
                            params.append((param_name, SymbolCategory.ARRAY))
                        elif isinstance(t.peek(None), LeftSquareToken):
                            next(t)
                            expect(RightSquareToken())
                            tS_f.define(param_name, None, SymbolCategory.ARRAY)
                            params.append((param_name, SymbolCategory.ARRAY))
                        else:
                            tS_f.define(param_name, None, SymbolCategory.VARIABLE)
                            params.append((param_name, SymbolCategory.VARIABLE))

                        if isinstance(t.peek(None), CommaToken):
                            next(t)
                            if not isinstance(t.peek(None), VarToken):
                                expect(RightParenToken())
                                break
                        elif isinstance(t.peek(None), RightParenToken):
                            # param list end
                            next(t)
                            break
                        else:
                            raise SyntaxError(f"Invalid synyax for formal parameter list in `{funcName}`.")

                    if len(params)==0:
                        expect(RightParenToken()) # no parameters in the function declaration
                    
                    expect(LeftBraceToken()) # {
                    # function body begins
                    (body, tS_f) = parse_program(tS_f) # get updated tS_f
                    next(t)
                    ast = FuncDef(funcName, params, body, tS_f)
                    tS.define(funcName, (params, body, tS_f), SymbolCategory.FUNCTION)
                
                # Function call
                case LeftParenToken(): # denotes the identifier is not a variable but a function call
                    # extract arguments
                    if isinstance(ast, Variable):
                        funcName = ast.var_name
                    elif isinstance(ast, CallArr):
                        funcName = ast
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
        ast = parse_atom(tS)
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
                                operation = t.peek(None).kw_name
                                next(t)
                                args = []
                                if isinstance(t.peek(None), LeftParenToken):
                                    next(t)
                                    while not isinstance(t.peek(None), RightParenToken):
                                        args.append(parse_var(tS)[0])
                                        if isinstance(t.peek(None), CommaToken):
                                            next(t)
                                    expect(RightParenToken())
                                ast = handle_operations(v, tS, operation, *args)
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

                        case SymbolCategory.STRING:
                            if isinstance(t.peek(None), LeftSquareToken):
                                next(t)
                                index= parse_var(tS)[0]
                                expect(RightSquareToken())
                                if (isinstance(t.peek(None), OperatorToken) 
                                    and t.peek(None).o == "="): #assign new value to index
                                    next(t)
                                    value = parse_var(tS)[0]
                                    ast = AssignStringVal(v, index, value)
                                else:
                                    ast = StringIdx(v, index)
                            elif isinstance(t.peek(None), DotToken):
                                while isinstance(t.peek(None), DotToken):
                                    next(t)
                                    operation = t.peek(None).kw_name
                                    next(t)
                                    args = []
                                    if isinstance(t.peek(None), LeftParenToken):
                                        next(t)
                                        while not isinstance(t.peek(None), RightParenToken):
                                            args.append(parse_var(tS)[0])
                                            if isinstance(t.peek(None), CommaToken):
                                                next(t)
                                        expect(RightParenToken())
                                    ast = handle_operations(v, tS, operation, *args)
                            else:
                                ast=Variable(v)
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
    
    return parse_program(defS)
    
    # try:
    #     ast, scope = parse_program(defS)
    #     return ast, scope, "complete"
    # except IncompleteParseError as e:
    #     return None, defS, "incomplete"

def handle_operations(var_name, tS, operation, *args):
    """
    Handles operations like push, pop, front, back, length, clear, and insert for strings and arrays.
    Args:
        var_name (str): The name of the variable.
        tS (SymbolTable): The current scope.
        operation (str): The operation to perform (e.g., 'PushFront', 'PushBack', 'PopFront', etc.).
        *args: Additional arguments required for the operation.
    Returns:
        AST: The corresponding AST node for the operation.
    """

    category = tS.lookup(var_name, cat=True)
    if category not in [SymbolCategory.ARRAY, SymbolCategory.STRING]:
        raise TypeError(f"Operation '{operation}' is not valid for type '{category}'.")
    
    match operation:
        case "PushFront":
            return PushFront(var_name, args[0])
        case "PushBack":
            return PushBack(var_name, args[0])
        case "PopFront":
            return PopFront(var_name)
        case "PopBack":
            return PopBack(var_name)
        case "Length":
            return GetLength(var_name)
        case "Clear":
            return ClearArray(var_name)
        case "Insert":
            return InsertAt(var_name, args[0], args[1])
        case "Remove":
            return RemoveAt(var_name, args[0])
        case "Slice":
            return Slice(var_name, args[0] if len(args) > 0 else None, 
                         args[1] if len(args) > 1 else None, 
                         args[2] if len(args) > 2 else None)
        case _:
            raise ValueError(f"Unknown operation '{operation}'.")


if __name__ == "__main__":
    pass