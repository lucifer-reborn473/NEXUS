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

    def define(self, iden, value):
        self.table[iden] = value

    def lookup(self, iden):
        if iden in self.table:
            return self.table[iden]
        elif self.parent:  # check in parent (enclosing scope)
            return self.parent.lookup(iden)
        else:
            raise NameError(f"Variable '{iden}' nhi mila!")
        
    def find_and_update(self, iden, val):
        if iden in self.table:
            self.table[iden] = val
        elif self.parent:
            self.parent.find_and_update(iden, val)
        else:
            raise NameError(f"Variable '{iden}' nhi mila!")
        
    def copy_scope(self):
        new_scope = SymbolTable(parent=self.parent)
        new_scope.table = self.table.copy() 
        return new_scope

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
class BindArray(AST):
    xname: str
    atype: str
    val: List[AST]
@dataclass
class Array(AST):
    xname: str
    index: int

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
class ForLoop(AST):
    initialization: AST 
    condition: AST
    increment: AST
    body: AST
    forScope: Any

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
    funcParams: List[Variable]  # list of variables
    funcBody: List[AST]         # assumed body is one-liner expression # will use {} for multiline
    funcScope: Any              # static scoping (scope is tied to function definition and not its call)
    isRec: bool                 # recursive or not

@dataclass 
class FuncCall(AST):
    funcName: str               # function name as a string
    funcArgs: List[AST]         # takes a list of expressions
    
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
            if isinstance(t.peek(None), RightBraceToken):    # function body parsing done
                break
            match t.peek(None):
                case KeywordToken("while"):
                    stmt, thisScope = parse_while(thisScope)
                case KeywordToken("for"):
                    stmt, thisScope = parse_for(thisScope)
                case _:
                    stmt, thisScope = parse_display(thisScope)

            statements.append(stmt)                         # collection of parsed statements

        return Statements(statements), thisScope          # Return a list of parsed statements + scope



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
                    if isinstance(t.peek(None), VarToken):
                        name = t.peek(None).var_name
                        next(t) 
                    if isinstance(t.peek(None), SemicolonToken):
                        value = None
                    else:
                        expect(OperatorToken("="))
                        value = parse_var(tS)[0]
                    tS.table[name] = None # add to current scope (value added at runtime (evaluation))
                    ast = VarBind(name, dtype, value)
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
        ast = parse_array(tS)
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
    def parse_array(tS):
        match t.peek(None):
            case KeywordToken("array"):
                next(t)
                elements = []
                atype=None
                if (isinstance(t.peek(None), TypeToken)):
                    atype = t.peek(None).type_name
                    next(t)
                if (isinstance(t.peek(None), VarToken)):
                    xname = t.peek(None).var_name
                    next(t)
                expect(OperatorToken("="))
                expect(LeftSquareToken())
                while not isinstance(t.peek(None), RightSquareToken):
                    elements.append(parse_string(tS))
                    if isinstance(t.peek(None), CommaToken):
                        next(t)
                expect(RightSquareToken())
                return BindArray(xname,atype,elements)
            case _:
                return parse_string(tS)
    def parse_string(tS): # while True may be included in future
        match t.peek(None):
            case StringToken(s):
                next(t)
                return String(s)
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
                case KeywordToken("fn") | KeywordToken("fnrec"): # function declaration
                    if t.peek(None).kw_name == "fnrec":
                        isRec = True
                    else:
                        isRec = False

                    next(t)
                    
                    if isinstance(t.peek(None), VarToken):
                        funcName = t.peek(None).var_name
                        next(t)
                    else:
                        print("Function name missing\nAborting")
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
                        tS_f.table[var_name] = None
                    
                    expect(LeftBraceToken()) # {
                    # function body begins
                    
                    # body = parse_var()
                    # bodyCode = []
                    # while not isinstance(t.peek(None), RightBraceToken):
                    #     stmt = parse_display()      # Parse current statement
                    #     bodyCode.append(stmt)       # collection of parsed statements
                    # body = Statements(bodyCode)     # list of parsed statements

                    (body, tS_f) = parse_program(tS_f) # get updated tS_f
                    next(t)
                    ast = FuncDef(funcName, params, body, tS_f, isRec)
                    tS.table[funcName] = (params, body, tS_f, isRec)
                
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
                    return parse_atom(tS)

    def parse_atom(tS): #! while True may be included in future
        match t.peek(None):
            case NumberToken(n):
                next(t)
                return Number(n)
            case VarToken(v): # variable identifier
                next(t)
                if (isinstance(t.peek(None), LeftSquareToken)): # probable array access
                    next(t)
                    index=parse_var(tS)[0]
                    expect(RightSquareToken())
                    return Array(v,index)
                return Variable(v)
            case BreakToken():
                next(t)
                return Break()

    return parse_program()


if __name__ == "__main__":
    pass
