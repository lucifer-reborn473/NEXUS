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

    
        case BinOp("and", l, r):
            return e(l) and e(r)
        case BinOp("or", l, r):
            return e(l) or e(r)
        case BinOp("&", l, r):
            return e(l) & e(r)
        case BinOp("|", l, r):
            return e(l) | e(r)
        case BinOp("^", l, r):
            return e(l) ^ e(r)
        case BinOp("<<", l, r):
            return e(l) << e(r)
        case BinOp(">>", l, r):
            return e(l) >> e(r)
        case BinOp("not", l, _):  # Unary logical operator
            return not e(l)
        case BinOp("~", l, _):  # Unary bitwise operator
            return ~e(l)

  
        case If(cond, sat, else_):
            return e(sat) if e(cond) else e(else_)
        case Display(val):
            return print(e(val))


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
    prev = None
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
                case "-":
                    if prev is None or prev in "+-*/(":
                        prev = s[i]
                        i = i + 1
                        yield NumberToken("-" + s[i])
                        i = i + 1
                    else:
                        prev = s[i]
                        i = i + 1
                        yield OperatorToken(t)
                case "+" | "*" | "/" | "(" | ")" | "<" | ">" | "==" | "!=" | "<=" | ">=":
                    prev = s[i]
                    i = i + 1
                    yield OperatorToken(t)


        elif s[i] in {'&', '|', '^', '~'}:
            match t := s[i]:
                case "&" | "|" | "^" | "~":
                    prev = s[i]
                    i += 1
                    yield OperatorToken(t)
                case "<" | ">":
                    if i + 1 < len(s) and s[i + 1] == t:  # << or >>
                    prev = s[i]
                    i += 2
                    yield OperatorToken(t * 2)
                else:
                    prev = s[i]
                    i += 1
                    yield OperatorToken(t)
                    if t in {"and", "or", "not"}:
                    yield KeywordToken(t)



def parse(s: str) -> AST:
    from more_itertools import peekable

    t = peekable(lex(s))

    def expect(what: Token):
        if t.peek(None) == what:
            next(t)
            return
        raise SyntaxError(f"Expected {what}")

    def parse_display():
    match t.peek(None):
        case KeywordToken("display"):
            next(t)
            return Display(parse_logic())
        case _:
            return parse_logic()


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
            case OperatorToken("<"):
                next(t)
                r = parse_sub()
                return BinOp("<", l, r)
            case OperatorToken(">"):
                next(t)
                r = parse_sub()
                return BinOp(">", l, r)
            case OperatorToken("=="):
                next(t)
                r = parse_sub()
                return BinOp("==", l, r)
            case OperatorToken("!="):
                next(t)
                r = parse_sub()
                return BinOp("!=", l, r)
            case OperatorToken("<="):
                next(t)
                r = parse_sub()
                return BinOp("<=", l, r)
            case OperatorToken(">="):
                next(t)
                r = parse_sub()
                return BinOp(">=", l, r)
            case _:
                return l

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
        ast = parse_div()
        while True:
            match t.peek(None):
                case OperatorToken("*"):
                    next(t)
                    ast = BinOp("*", ast, parse_div())
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
        match t.peek(None):
            case OperatorToken("("):
                next(t)
                ast = parse_sub()
                match t.peek(None):
                    case OperatorToken(")"):
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
        ast = parse_shift()
        while True:
            match t.peek(None):
                case OperatorToken("&"):
                    next(t)
                    ast = BinOp("&", ast, parse_shift())
                case OperatorToken("|"):
                    next(t)
                    ast = BinOp("|", ast, parse_shift())
                case OperatorToken("^"):
                    next(t)
                    ast = BinOp("^", ast, parse_shift())
                case _:
                    return ast
    
    def parse_shift():
        ast = parse_brackets()
        while True:
            match t.peek(None):
                case OperatorToken("<<"):
                    next(t)
                    ast = BinOp("<<", ast, parse_brackets())
                case OperatorToken(">>"):
                    next(t)
                    ast = BinOp(">>", ast, parse_brackets())
                case _:
                    return ast



if __name__ == "__main__":
   # Arithmetic Operators
    e(parse("display (2 + 3)"))  
    e(parse("display (10 - 4)"))  
    e(parse("display (5 * 6)"))  
    e(parse("display (20 / 4)"))  
    e(parse("display ((5 + 3) * 2 - 4 / 2)"))  
    e(parse("display (-5 + 2)"))  
    e(parse("display (3 * (4 + 2) / 3 - 1)"))  
    e(parse("display (3 + 2 * 4)"))  
    e(parse("display (-6 / 2)"))  

    # Logical Operators
    e(parse("display (3 < 5 and 4 > 2)"))  
    e(parse("display (5 > 10 or 2 < 3)"))  
    e(parse("display (not 4 > 3)"))  
    e(parse("display (3 == 3 and 4 != 2)"))  
    e(parse("display (5 <= 10 or 8 >= 20)"))  
    e(parse("display (not (4 > 5 and 3 < 1))"))  
    e(parse("display (3 == 3 and 4 == 4)"))  
    e(parse("display (5 < 2 or 7 > 10)"))  

    # Bitwise Operators
    e(parse("display (3 & 1)"))  
    e(parse("display (3 | 1)"))  
    e(parse("display (3 ^ 1)"))  
    e(parse("display (~5)"))  
    e(parse("display (5 << 2)"))  
    e(parse("display (8 >> 2)"))  
    e(parse("display (1024 & 512)"))  
    e(parse("display (-5 << 2)"))  
    e(parse("display (-5 >> 2)"))  

    # Variable Definitions
    e(parse("display ('hello world')"))  
    e(parse("display ('a' + 'b')"))  
    e(parse("display ('num' + 5)"))  # Should throw error
    e(parse("display ('5')"))  

    # Conditional Expressions (If Statements)
    e(parse("display (if 5 < 10 then 1 else 0 end)"))
    e(parse("display (if 5 < 10 then if 2 < 3 then 1 else 0 end else 0 end)"))
    e(parse("display (if 0 < 1 then 1 else 0 end)"))
    e(parse("display (if 2 < 3 then if 4 > 5 then 0 else 1 end else 2 end)"))
    e(parse("display (if 5 == 5 then 10 end)"))

    # Recursive Functions (Factorial Simulation)
    expr = """
    if 5 == 0 then 1 
    else 5 * (if 4 == 0 then 1 else 4 * (if 3 == 0 then 1 else 3 * (if 2 == 0 then 1 else 2 * (if 1 == 0 then 1 else 1)))) end
    """
    e(parse(expr))

    # Edge Cases
    e(parse("display (5 / 0)"))  # Division by zero
    e(parse("display (3 + 'a')"))  # Invalid operation
    e(parse("display (9999999 * 1234567)"))  # Large numbers
    e(parse("display (0.0001 * 0.0002)"))  # Small numbers
    e(parse("display (1 << 1024)"))  # Extremely large shift
    e(parse("display (5 == 5 and 'a' == 'a')"))  # Comparison with string
    print(parse(expr))
    e(parse(expr))
    # loop <condition> then <statement> end
    # int32 x=2
