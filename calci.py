from dataclasses import dataclass
from collections.abc import Iterator    
from more_itertools import peekable
from tokens import keyword_tokens
# from typing import Optional

class AST:
    pass

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

def e(tree: AST) -> int:
    match tree:
        case Number(v): return int(v)
        case String(s): return s
        case BinOp("+", l, r): return e(l) + e(r)
        case BinOp("*", l, r): return e(l) * e(r)
        case BinOp("-", l, r): return e(l) - e(r)
        case BinOp("/", l, r): return e(l) / e(r)
        case BinOp("<", l, r): return e(l) < e(r)
        case BinOp(">", l, r): return e(l) > e(r)
        case BinOp("==", l, r): return e(l) == e(r)
        case BinOp("!=", l, r): return e(l) != e(r)
        case BinOp ("<=", l, r): return e(l) <= e(r)
        case BinOp (">=", l, r): return e(l) >= e(r)
        case If(cond, sat, else_): return e(sat) if e(cond) else e(else_)
        case Display(val): return print(e(val))
        

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
class Display(AST):
    val: any

@dataclass
class If(AST):
    c: AST
    t: AST
    e: AST = None

def lex(s: str) -> Iterator[Token]:
    i = 0
    prev= None
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
            prev = s[i]
            i = i + 1
            while i < len(s) and s[i].isdigit():
                t = t + s[i]
                i = i + 1
            yield NumberToken(t)
        else:
            match t := s[i]:
                case '-':
                    if prev is None or prev in '+-*/(':
                        prev = s[i]
                        i = i + 1
                        yield NumberToken('-' + s[i])
                        i = i + 1
                    else:
                        prev = s[i]
                        i = i + 1
                        yield OperatorToken(t)
                case '+' | '*' | '/' | '(' | ')' | '<' | '>' | '==' | '!=' | '<=' | '>=':
                    prev = s[i]
                    i = i + 1
                    yield OperatorToken(t)

def parse(s: str) -> AST:
    from more_itertools import peekable
    t = peekable(lex(s))
    def expect(what: Token):
        if t.peek(None) == what:
            next(t)
            return
        raise  SyntaxError(f"Expected {what}") 
    def parse_display():
        match t.peek(None):
            case KeywordToken("display"):
                next(t)
                return Display(parse_if())
            case _:
                return parse_if()
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
        l = parse_sub()
        match t.peek(None):
            case OperatorToken('<'):
                next(t)
                r = parse_sub()
                return BinOp('<', l, r)
            case OperatorToken('>'):
                next(t)
                r = parse_sub()
                return BinOp('>', l, r)
            case OperatorToken('=='):
                next(t)
                r = parse_sub()
                return BinOp('==', l, r)
            case OperatorToken('!='):
                next(t)
                r = parse_sub()
                return BinOp('!=', l, r)
            case OperatorToken('<='):
                next(t)
                r = parse_sub()
                return BinOp('<=', l, r)
            case OperatorToken('>='):
                next(t)
                r = parse_sub()
                return BinOp('>=', l, r)
            case _:
                return l
    def parse_sub():
        ast = parse_add()
        while True:
            match t.peek(None):
                case OperatorToken('-'):
                    next(t)
                    ast = BinOp('-', ast, parse_add())
                case _:
                    return ast
        
    def parse_add():
        ast = parse_mul()
        while True:
            match t.peek(None):
                case OperatorToken('+'):
                    next(t)
                    ast = BinOp('+', ast, parse_mul())
                case _:
                    return ast

    def parse_mul():
        ast = parse_div()
        while True:
            match t.peek(None):
                case OperatorToken('*'):
                    next(t)
                    ast = BinOp('*', ast, parse_div())
                case _:
                    return ast
    def parse_div():
        ast = parse_brackets()
        while True:
            match t.peek(None):
                case OperatorToken('/'):
                    next(t)
                    ast = BinOp("/", ast, parse_brackets())
                case _:
                    return ast

    def parse_brackets():
        match t.peek(None):
            case OperatorToken('('):
                next(t) 
                ast = parse_sub() 
                match t.peek(None):
                    case OperatorToken(')'):
                        next(t)  
                        return ast
                    case _:
                        raise SyntaxError("Expected ')'")
            case _:
                return parse_string() 

    def parse_string():
        match t.peek(None):
            case StringToken(s):
                next(t)
                return String(s)
            case _:
                return parse_atom()
    def parse_atom():
        match t.peek(None):
            case NumberToken(v):
                next(t)
                return Number(v)

    return parse_display()

if __name__=="__main__":
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
    expr="display (3 *(3+1*(4-1)) /2) "
    exp_2="display ('hello peeps')"
    # t = peekable(lex(expr))
    # print(t.peek(None))
    # next(t)
    # print(t.peek(None))
    print(parse(expr))
    e(parse(expr))
    # loop <condition> then <statement> end
