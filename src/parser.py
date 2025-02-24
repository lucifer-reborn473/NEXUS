from more_itertools import peekable
from typing import Optional, Any, List
from pprint import pprint
from lexer import *

# ==========================================================================================
# ==================================== PARSER ==============================================

class SymbolTable:
    def __init__(self, parent=None):
        self.table = {}
        self.parent = parent  # enclosing scope

    def define(self, name, value):
        self.table[name] = value

    def lookup(self, name):
        if name in self.table:
            return self.table[name]
        elif self.parent:  # check in parent (enclosing scope)
            return self.parent.lookup(name)
        else:
            raise NameError(f"Variable '{name}' nhi mila!")

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
    funcScope: Any

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

    def parse_program(thisScope = None):

        if thisScope is None:
            thisScope = SymbolTable() # forms the global scope

        statements = []
        while t.peek(None) is not None:
            if isinstance(t.peek(None), RightCurlyBracketToken): # function body parsing done
                break
            stmt,thisScope = parse_display(thisScope)      # Parse current statement
            statements.append(stmt)     # collection of parsed statements

        return (Statements(statements), thisScope)  # Return a list of parsed statements


    def parse_display(tS): # display value/output
        (ast, tS) = parse_var(tS)
        while True:
            match t.peek(None):
                case KeywordToken("display"):
                    next(t)
                    ast = Display(parse_var(tS)[0])
                case SemicolonToken():
                    next(t)
                    return ast, tS
                case _:
                    return ast, tS

    def parse_var(tS): # for `var` declaration
        ast = parse_update_var(tS)
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
                    value = parse_var(tS)[0]
                    tS.table[name] = None # add to current scope
                    ast = Binding(name, dtype, value)
                case _:
                    return ast, tS
                
    def parse_update_var(tS): # for updating var
        ast =parse_logic(tS)
        while True:
            match t.peek(None):
                case VarToken(var_name):
                    next(t)
                    if isinstance(t.peek(None),OperatorToken) and t.peek(None).o in compound_assigners:
                        op=t.peek(None).o
                        next(t)
                        value=parse_logic(tS)
                        ast=CompoundAssignment(var_name,op,value)
                    else:
                        return ast
                case _ :
                    return ast
                
    def parse_logic(tS):
        ast = parse_if(tS)
        while True:
            match t.peek(None):
                case KeywordToken("and"):
                    next(t)
                    ast = BinOp("and", ast, parse_if(tS))
                case KeywordToken("or"):
                    next(t)
                    ast = BinOp("or", ast, parse_if(tS))
                case _:
                    return ast

    def parse_if(tS):
        match t.peek(None):
            case KeywordToken("if"):
                next(t)
                cond = parse_logic(tS)
                expect(KeywordToken("then"))
                then = parse_logic(tS)
                expect(KeywordToken("else"))
                else_ = parse_logic(tS)
                expect(KeywordToken("end"))
                return If(cond, then, else_)
            case _:
                return parse_cmp(tS)

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
        ast = parse_ascii_char(tS)
        while True:
            match t.peek(None):
                case OperatorToken("÷"):
                    next(t)
                    ast = BinOp("÷", ast, parse_ascii_char(tS))
                case _:
                    return ast
    def parse_ascii_char(tS):
        ast = parse_brackets(tS)
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
    def parse_brackets(tS):
        while True:
            match t.peek(None):
                case OperatorToken("("):
                    next(t)
                    ast = parse_display(tS)
                    match t.peek(None):
                        case OperatorToken(")"):
                            next(t)
                            return ast
                        case _:
                            raise SyntaxError(f"Expected ')' got {t.peek(None)}")
                case _:
                    return parse_string(tS)

    def parse_string(tS): # while True may be included in future
        match t.peek(None):
            case StringToken(s):
                next(t)
                return String(s)
            case _:
                return parse_func(tS)

    def parse_func(tS): # Function definition and Function call
        ast = parse_atom()
        while True:
            match t.peek(None):
                case KeywordToken("fn"): # function declaration
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
                    
                    expect(LeftCurlyBracketToken())
                    # function body begins
                    # body = parse_var()

                    # bodyCode = []
                    # while not isinstance(t.peek(None), RightCurlyBracketToken):
                    #     stmt = parse_display()      # Parse current statement
                    #     bodyCode.append(stmt)       # collection of parsed statements
                    # body = Statements(bodyCode)     # list of parsed statements
                    

                    tS_f = SymbolTable(tS) # Function Scope (with tS as parent scope)

                    # add function params to scope (params contain variable tokens)
                    for var_token in params:
                        tS_f.table[var_token.var_name] = None

                    (body, tS_f) = parse_program(tS_f) # get updated tS_f
                    next(t)
                    ast = FuncDef(funcName, params, body, tS_f)
                
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
                                # expect expression
                                expr = parse_brackets()
                                funcArgs.append(expr)
                
                case _:
                    return ast
                # parse_func() ends here

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
