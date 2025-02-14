from dataclasses import dataclass
from collections.abc import Iterator
from more_itertools import peekable
from typing import Optional, Any, List
from tokens import *
from context import Context
from pprint import pprint

# ==========================================================================================
# ==================================== LEXER ===============================================

class Token:
    pass

@dataclass
class VarToken(Token):
    var_name: str

@dataclass
class NumberToken(Token):
    v: str

@dataclass
class OperatorToken(Token):
    o: str

@dataclass
class StringToken(Token):
    s: str

@dataclass
class KeywordToken(Token):
    w: str

@dataclass
class TypeToken(Token):
    t: str

@dataclass
class SemicolonToken(Token):
    pass

@dataclass
class WhileToken(Token):
    pass

def lex(s: str) -> Iterator[Token]:
    i = 0
    prev_char = None
    prev_token = None
    while True:
        while i < len(s) and s[i].isspace():
            i += 1

        if i >= len(s):
            return
        
        if s[i] == ";":
            yield SemicolonToken()
            i += 1

        elif s[i].isalpha():
            t = s[i]
            i += 1
            while i < len(s) and s[i].isalpha():
                t += s[i]
                i += 1
            if t in keyword_tokens:
                yield KeywordToken(t)
            elif t in base_type_tokens:
                yield TypeToken(t)
            else:
                yield VarToken(t)

        elif s[i] == "'" or s[i] == '"':
            quote = s[i]
            i += 1
            t = ""
            while i < len(s) and s[i] != quote:
                t += s[i]
                i += 1
            if i >= len(s):
                raise SyntaxError(f"Expected {quote}")
            i += 1
            yield StringToken(t)

        elif s[i].isdigit():
            t = s[i]
            prev_char = s[i]
            i += 1
            while i < len(s) and s[i].isdigit():
                t += s[i]
                i += 1
            yield NumberToken(t)
        
        elif s[i:i+2] == "/~":
            i += 2
            while i < len(s) and s[i:i+2] != "~/":
                i += 1
            i += 2
            continue 

        elif s[i:i+3] == "/~{":
            i += 3
            while i < len(s) and s[i:i+3] != "}~/":
                i += 1
            i += 3
            continue 
        
        else:
            match t := s[i]:
                case "-":
                    if (s[i+1] == "="):
                        i += 2
                        yield OperatorToken("-=")
                    elif (
                        prev_char is None or prev_char in "+-*/(<>!=%"
                    ):
                        prev_char = s[i]
                        i += 1
                        if s[i].isdigit():
                            while i < len(s) and (s[i].isdigit() or s[i] == "."):
                                t += s[i]
                                i += 1
                            yield NumberToken(t)
                        elif s[i].isalpha():
                            while i < len(s) and s[i].isalpha():
                                t += s[i]
                                i += 1
                            yield NumberToken("-1")
                            yield OperatorToken("*")
                            yield VarToken(t[1:])
                    else:
                        prev_char = s[i]
                        i += 1
                        yield OperatorToken(t)
                case t if t in base_operator_tokens:
                    prev_char = s[i]
                    i += 1
                    if i < len(s) and (t + s[i]) in top_level_operator_tokens:
                        prev_char = s[i]
                        i += 1
                        yield OperatorToken(t + prev_char)
                    else:
                        yield OperatorToken(t)

# ==========================================================================================
# ================================= PARSER =================================================

class AST:
    pass

@dataclass
class While(AST):
    condition: AST
    body: AST

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
class Number(AST):
    val: str

@dataclass
class String(AST):
    val: str

@dataclass
class Display(AST):
    val: Any

@dataclass
class Statements:
    statements: List[AST]

def parse(s: str) -> List[AST]:
    t = peekable(lex(s))

    def expect(what: Token):
        if t.peek(None) == what:
            next(t)
            return
        raise SyntaxError(f"Expected {what} got {t.peek(None)}")
    
    def parse_program():
        statements = []
        while t.peek(None) is not None:
            stmt = parse_statement()
            statements.append(stmt)
        return Statements(statements)

    def parse_statement():
        match t.peek(None):
            case KeywordToken("while"):
                return parse_while()
            case KeywordToken("display"):
                return parse_display()
            case _:
                return parse_var()

    def parse_while():
        expect(KeywordToken("while"))
        condition = parse_expression()
        expect(KeywordToken("do"))
        body = parse_statement()
        expect(KeywordToken("end"))
        return While(condition, body)

    def parse_display():
        expect(KeywordToken("display"))
        value = parse_expression()
        expect(SemicolonToken())
        return Display(value)

    def parse_var():
        ast = parse_update_var()
        while True:
            match t.peek(None):
                case KeywordToken("var"):
                    next(t)
                    dtype = None
                    if isinstance(t.peek(None), TypeToken):
                        dtype = t.peek(None).t
                        next(t)
                    if isinstance(t.peek(None), VarToken):
                        name = t.peek(None).var_name
                        next(t)
                    expect(OperatorToken("="))
                    value = parse_expression()
                    ast = Binding(name, dtype, value)
                case _:
                    return ast

    def parse_expression():
        return parse_cmp()

    def parse_cmp():
        ast = parse_add()
        while True:
            match t.peek(None):
                case OperatorToken("<"):
                    next(t)
                    ast = BinOp("<", ast, parse_add())
                case OperatorToken(">"):
                    next(t)
                    ast = BinOp(">", ast, parse_add())
                case _:
                    return ast

    def parse_add():
        ast = parse_mul()
        while True:
            match t.peek(None):
                case OperatorToken("+"):
                    next(t)
                    ast = BinOp("+", ast, parse_mul())
                case _:
                    return ast

    def parse_mul():
        ast = parse_atom()
        while True:
            match t.peek(None):
                case OperatorToken("*"):
                    next(t)
                    ast = BinOp("*", ast, parse_atom())
                case _:
                    return ast

    def parse_atom():
        match t.peek(None):
            case NumberToken(n):
                next(t)
                return Number(n)
            case VarToken(v):
                next(t)
                return Variable(v)
            case StringToken(s):
                next(t)
                return String(s)

    return parse_program()

# ==========================================================================================
# ================================= EVALUATOR ==============================================

context = Context()

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
                raise NameError(f"name '{v}' is not defined")
        case While(cond, body):
            while e(cond):
                e(body)
        case Display(val):
            return print(e(val))
        case Binding(name, dtype, value):
            value = e(value)
            context.add_variable(name, value, dtype)
            return value

if __name__ == "__main__":
    # Example usage
    expr = """
    var integer x = 0;
    while x < 5 do
        display x;
        x = x + 1;
    end
    """
    print("\nParsed expression:")
    print(parse(expr))
    print("\nEvaluated expression:")
    e(parse(expr))