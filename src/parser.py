from more_itertools import peekable
from typing import Optional, Any, List
from context import Context
from pprint import pprint
from lexer import *

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
class Binding(AST):
    name: str
    dtype: Optional[str]
    value: AST

@dataclass
class Variable(AST):
    name: str

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
class Number(AST):
    val: str

@dataclass
class String(AST):
    val: str

@dataclass
class Display(AST):
    val: any

@dataclass
class CompoundAssignment(AST):
    var_name: str
    op: str
    value: AST

@dataclass
class If(AST):
    c: AST
    t: AST
    e: AST = None

@dataclass
class Statements:
    statements: List[AST]

@dataclass
class FuncDef(AST):
    funcName: str
    funcParams: List[Variable]  # list of variables
    funcBody: List[AST]         # assumed body is one-liner expression # will use {} for multiline

@dataclass 
class FuncCall(AST):
    funcName: str               # function name as a string
    funcArgs: List[AST]         
    
# ==========================================================================================
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

    def parse_program():
        statements = []
        while t.peek(None) is not None:
            stmt = parse_display()      # Parse current statement
            statements.append(stmt)     # collection of parsed statements

        return Statements(statements)  # Return a list of parsed statements


    def parse_display(): # display value/output
        ast=parse_var()
        while True:
            match t.peek(None):
                case KeywordToken("display"):
                    next(t)
                    ast=Display(parse_var())
                case SemicolonToken():
                    next(t)
                    return ast
                case _:
                    return ast

    def parse_var(): # for `var` declaration
        ast=parse_update_var()
        while True:
            match t.peek(None):
                case KeywordToken("var"):
                    next(t)
                    dtype=None
                    if isinstance(t.peek(None), TypeToken):
                        dtype= t.peek(None).t
                        next(t)
                    # print(t.peek(None))
                    if isinstance(t.peek(None), VarToken):
                        name = t.peek(None).var_name
                        next(t) 
                    # print(t.peek(None))
                    expect(OperatorToken("="))
                    # print(t.peek(None))
                    value = parse_var()
                    ast=Binding(name, dtype, value)
                case _:
                    return ast
    def parse_update_var(): # for updating var
        ast =parse_if()
        while True:
            match t.peek(None):
                case VarToken(var_name):
                    next(t)
                    if isinstance(t.peek(None),OperatorToken) and t.peek(None).o in compound_assigners:
                        op=t.peek(None).o
                        next(t)
                        value=parse_if()
                        ast=CompoundAssignment(var_name,op,value)
                    else:
                        return ast
                case _ :
                    return ast
    def parse_if():
        match t.peek(None):
            case KeywordToken("if"):
                next(t)
                cond = parse_logic()
                expect(KeywordToken("then"))
                then = parse_logic()
                expect(KeywordToken("else"))
                else_ = parse_logic()
                expect(KeywordToken("end"))
                return If(cond, then, else_)
            case _:
                return parse_cmp()

    def parse_logic():
        ast = parse_bitwise()
        while True:
            match t.peek(None):
                case KeywordToken("and"):
                    next(t)
                    ast = BinOp("and", ast, parse_bitwise())
                case KeywordToken("or"):
                    next(t)
                    ast = BinOp("or", ast, parse_bitwise())
                case _:
                    return ast
    def parse_bitwise():
        ast = parse_cmp()
        while True:
            match t.peek(None):
                case OperatorToken("&"):
                    next(t)
                    ast = BinOp("&", ast, parse_cmp())
                case OperatorToken("|"):
                    next(t)
                    ast = BinOp("|", ast, parse_cmp())
                case OperatorToken("^"):
                    next(t)
                    ast = BinOp("^", ast, parse_cmp())
                case _:
                    return ast
    def parse_cmp():
        ast = parse_shift()
        while True:
            match t.peek(None):
                case OperatorToken("<"):
                    next(t)
                    ast = BinOp("<", ast, parse_shift())
                case OperatorToken(">"):
                    next(t)
                    ast = BinOp(">", ast, parse_shift())
                case OperatorToken("=="):
                    next(t)
                    ast = BinOp("==", ast, parse_shift())
                case OperatorToken("!="):
                    next(t)
                    ast = BinOp("!=", ast, parse_shift())
                case OperatorToken("<="):
                    next(t)
                    ast = BinOp("<=", ast, parse_shift())
                case OperatorToken(">="):
                    next(t)
                    ast = BinOp(">=", ast, parse_shift())
                case _:
                    return ast
                             
    def parse_shift():
        ast = parse_add()
        while True:
            match t.peek(None):
                case OperatorToken("<<"):
                    next(t)
                    ast = BinOp("<<", ast, parse_add())
                case OperatorToken(">>"):
                    next(t)
                    ast = BinOp(">>", ast, parse_add())
                case _:
                    return ast

    def parse_add():
        ast = parse_sub()
        while True:
            match t.peek(None):
                case OperatorToken("+"):
                    next(t)
                    ast = BinOp("+", ast, parse_sub())
                case _:
                    return ast
                
    def parse_sub():
        ast = parse_mul()
        while True:
            match t.peek(None):
                case OperatorToken("-"):
                    next(t)
                    ast = BinOp("-", ast, parse_mul())
                case _:
                    return ast


    def parse_mul():
        ast = parse_modulo()
        while True:
            match t.peek(None):
                case OperatorToken("*"):
                    next(t)
                    ast = BinOp("*", ast, parse_modulo())
                case _:
                    return ast
    def parse_modulo():
        ast =parse_div_slash()
        while True:
            match t.peek(None):
                case OperatorToken("%"):
                    next(t)
                    ast=BinOp("%",ast,parse_div_slash())
                case _:
                    return ast

    def parse_div_slash():
        ast = parse_div_dot()
        while True:
            match t.peek(None):
                case OperatorToken("/"):
                    next(t)
                    ast = BinOp("/", ast, parse_div_dot())
                case _:
                    return ast

    def parse_div_dot():
        ast = parse_ascii_char()
        while True:
            match t.peek(None):
                case OperatorToken("÷"):
                    next(t)
                    ast = BinOp("÷", ast, parse_ascii_char())
                case _:
                    return ast
    def parse_ascii_char():
        ast = parse_brackets()
        while True:
            match t.peek(None):
                case KeywordToken("char"):
                    next(t)
                    expect(OperatorToken("("))
                    value = parse_if()
                    expect(OperatorToken(")"))
                    ast = UnaryOp("char", value)
                case KeywordToken("ascii"):
                    next(t)
                    expect(OperatorToken("("))
                    value = parse_if()
                    expect(OperatorToken(")"))
                    ast = UnaryOp("ascii", value)
                case _:
                    return ast
    def parse_brackets():
        while True:
            match t.peek(None):
                case OperatorToken("("):
                    next(t)
                    ast = parse_display()
                    match t.peek(None):
                        case OperatorToken(")"):
                            next(t)
                            return ast
                        case _:
                            raise SyntaxError(f"Expected ')' got {t.peek(None)}")
                case _:
                    return parse_string()

    def parse_string(): # while True may be included in future
        match t.peek(None):
            case StringToken(s):
                next(t)
                return String(s)
            case _:
                return parse_func()

    def parse_func(): # Function definition and Function call
        ast = parse_atom()
        while True:
            match t.peek(None):
                case KeywordToken("func"):
                    next(t)
                    
                    if isinstance(t.peek(None), VarToken):
                        funcName = t.peek(None)
                        funcName = funcName.var_name
                        next(t)
                    else:
                        print("Function name missing\nAborting")
                        exit()

                    expect(OperatorToken("("))

                    # parse parameters
                    params = []
                    while isinstance(t.peek(None), VarToken):
                        params.append(t.peek(None))
                        next(t)
                        if isinstance(t.peek(None), CommaToken):
                            next(t) 
                        else:
                            expect(OperatorToken(")")) # parameter list end
                            break    
                    
                    expect(ColonToken())
                    expect(LeftCurlyBracketToken())
                    # function body begins
                    # body = parse_var()

                    bodyCode = []
                    while not isinstance(t.peek(None), RightCurlyBracketToken):
                        stmt = parse_display()      # Parse current statement
                        bodyCode.append(stmt)       # collection of parsed statements
                    
                    next(t)
                    body = Statements(bodyCode)     # Return a list of parsed statements
                    ast = FuncDef(funcName, params, body)
                
                # Function call
                case OperatorToken("("): # denotes the identifier is not a variable but a function call
                    # extract arguments
                    funcName = ast.name
                    funcArgs = []
                    next(t)
                    while True: 
                        match t.peek(None):
                            case StringToken(this_arg):
                                funcArgs.append(String(this_arg))
                                next(t)
                            case NumberToken(this_arg):
                                funcArgs.append(Number(this_arg))
                                next(t)
                            case CommaToken():
                                next(t)
                            case VarToken(varName):
                                funcArgs.append(Variable(varName))
                                next(t)
                            case OperatorToken(")"):
                                # function call ends
                                ast = FuncCall(funcName, funcArgs)
                                next(t)
                                return ast

                case _:
                    return ast

    def parse_atom(): # while True may be included in future
        match t.peek(None):
            case NumberToken(n):
                next(t)
                return Number(n)
            case VarToken(v): # variable identifier
                next(t)
                return Variable(v)

    return parse_program()


if __name__ == "__main__":
    pass
