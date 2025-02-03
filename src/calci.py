from dataclasses import dataclass
from collections.abc import Iterator
from more_itertools import peekable
from typing import Optional, Any
from tokens import (
    keyword_tokens,
    base_type_tokens,
    top_level_operator_tokens,
    base_operator_tokens,
)
from context import Context


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
    
    def eval(self,context):
        return context[self.name]

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


def e(tree: AST) -> int:
    context=Context()
    match tree:
        case Number(v):
            return int(v)
        case String(s):
            return s
        case BinOp("+", l, r):
            return e(l) + e(r)
        case BinOp("*", l, r):
            return e(l) * e(r)
        case BinOp("-", l, r):
            return e(l) - e(r)
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
        case BinOp("%", l , r):
            return e(l) % e(r)
        case UnaryOp("~", val):
            return ~e(val)
        case UnaryOp("!", val):
            return not e(val)
        case UnaryOp("++", val):
            return e(val) + 1
        case UnaryOp("--", val):
            return e(val) - 1
        case If(cond, sat, else_):
            return e(sat) if e(cond) else e(else_)
        case Display(val):
            return print(e(val))
        case Binding(name, dtype, value):
            context.add_variable(name,e(value),dtype)
            return context #temporary return value -> will be removed later

class Token:
    pass


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
class If(AST):
    c: AST
    t: AST
    e: AST = None


def lex(s: str) -> Iterator[Token]:
    i = 0
    prev_char = None
    prev_token= None
    while True:
        while i < len(s) and s[i].isspace():
            i = i + 1

        if i >= len(s):
            return

        if s[i].isalpha():
            t = s[i]
            i = i + 1
            while i < len(s) and s[i].isalpha():
                t = t + s[i]
                i = i + 1
            if t in keyword_tokens:
                yield KeywordToken(t)
            elif t in base_type_tokens:
                yield TypeToken(t)
            else:
                yield StringToken(t)
        elif s[i] == "'" or s[i] == '"':
            quote = s[i]
            i = i + 1
            t = ""
            while i < len(s) and s[i] != quote:
                t = t + s[i]
                i = i + 1
            if i >= len(s):
                raise SyntaxError(f"Expected {quote}")
            i = i + 1
            yield StringToken(t)

        elif s[i].isdigit():
            t = s[i]
            prev_char = s[i]
            i = i + 1
            while i < len(s) and s[i].isdigit():
                t = t + s[i]
                i = i + 1
            yield NumberToken(t)
        else:
            match t := s[i]:
                case "-":
                    if (
                        prev_char is None or prev_char in "+-*/(<>!=%"
                    ):  # check if it is a negative number
                        prev_char = s[i]
                        i = i + 1
                        yield NumberToken("-" + s[i])
                        i = i + 1
                    else:  # check if it is a token
                        prev_char = s[i]
                        i = i + 1
                        yield OperatorToken(t)
                case t if t in base_operator_tokens:
                    prev_char = s[i]
                    i = i + 1
                    if i<len(s) and (t + s[i]) in top_level_operator_tokens:
                        prev_char = s[i]
                        i = i + 1
                        yield OperatorToken(t + prev_char)
                    else:
                        yield (OperatorToken(t))


def parse(s: str) -> AST:

    t = peekable(lex(s))

    def expect(what: Token):
        if t.peek(None) == what:
            next(t)
            return
        raise SyntaxError(f"Expected {what}")

    def parse_display():
        ast=parse_var()
        while True:
            match t.peek(None):
                case KeywordToken("display"):
                    next(t)
                    ast=Display(parse_var())
                case _:
                    return ast

    def parse_var():
        ast=parse_if()
        while True:
            match t.peek(None):
                case KeywordToken("var"):
                    next(t)
                    dtype=None
                    if isinstance(t.peek(None), TypeToken):
                        dtype= t.peek(None).t
                        next(t)
                    # print(t.peek(None))
                    if isinstance(t.peek(None), StringToken):
                        name = t.peek(None).s
                        next(t)
                    # print(t.peek(None))
                    expect(OperatorToken("="))
                    # print(t.peek(None))
                    value = parse_var()
                    ast=Binding(name, dtype, value)
                case _:
                    return ast
    def parse_if():
        match t.peek(None):
            case KeywordToken("if"):
                next(t)
                cond = parse_if()
                expect(KeywordToken("then"))
                then = parse_if()
                expect(KeywordToken("else"))
                else_ = parse_if()
                expect(KeywordToken("end"))
                return If(cond, then, else_)
            case _:
                return parse_cmp()

    def parse_cmp():
        ast = parse_sub()
        while True:
            match t.peek(None):
                case OperatorToken("<"):
                    next(t)
                    ast = BinOp("<", ast, parse_sub())
                case OperatorToken(">"):
                    next(t)
                    ast = BinOp(">", ast, parse_sub())
                case OperatorToken("=="):
                    next(t)
                    ast = BinOp("==", ast, parse_sub())
                case OperatorToken("!="):
                    next(t)
                    ast = BinOp("!=", ast, parse_sub())
                case OperatorToken("<="):
                    next(t)
                    ast = BinOp("<=", ast, parse_sub())
                case OperatorToken(">="):
                    next(t)
                    ast = BinOp(">=", ast, parse_sub())
                case _:
                    return ast

    def parse_sub():
        ast = parse_add()
        while True:
            match t.peek(None):
                case OperatorToken("-"):
                    next(t)
                    ast = BinOp("-", ast, parse_add())
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
        ast = parse_modulo()
        while True:
            match t.peek(None):
                case OperatorToken("*"):
                    next(t)
                    ast = BinOp("*", ast, parse_modulo())
                case _:
                    return ast
    def parse_modulo():
        ast =parse_div()
        while True:
            match t.peek(None):
                case OperatorToken("%"):
                    next(t)
                    ast=BinOp("%",ast,parse_div())
                case _:
                    return ast

    def parse_div():
        ast = parse_brackets()
        while True:
            match t.peek(None):
                case OperatorToken("/"):
                    next(t)
                    ast = BinOp("/", ast, parse_brackets())
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
                return parse_atom()

    def parse_atom(): # while True may be included in future
        match t.peek(None):
            case NumberToken(v):
                next(t)
                return Number(v)

    return parse_display()


if __name__ == "__main__":
    # expression=" (5-4)*5+ (8-2)/3"
    # print(parse(expression))
    # print(e(parse(expression)))
    # simple_exp=" 3 *(3+1*(4-1)) /2"
    # simple_exp=" -3 + 7 + (2+8)/5 - (2*(4-3))"
    # print(parse(simple_exp))
    # print(e(parse(simple_exp)))
    # sample_exp="if 2 < 3 then 0 end"
    # print(parse("if 2 < 3 then 0+5 else 1*6 end"))
    # print(e(parse("if 2 < 3 then 0+5 else 1*6 end")))
    # expr = "display 2+1 "
    # expr = "display 0<= 1 >=2 "
    expr = " display( var integer x= (2 + 1 + 5 % 2 ))"
    compound_assignment= "display ( -3 < -2 <-1)"
    for t in lex(expr):
        print(t)
    # t = peekable(lex(expr))
    # print(t.peek(None))
    # next(t)
    # print(t.peek(None))
    print("Parsed expression:")
    print(parse(expr))
    print("Evaluated expression:")
    e(parse(expr))
    # loop <condition> then <statement> end
    # int32 x=2
