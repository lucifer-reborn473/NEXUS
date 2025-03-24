from dataclasses import dataclass
from collections.abc import Iterator
from tokens import  *

# ==========================================================================================
# ==================================== LEXER ===============================================

class Token:
    pass

@dataclass
class VarToken(Token):
    var_name: str # identifier

@dataclass
class NumberToken(Token):
    val: str

@dataclass
class OperatorToken(Token):
    o: str

@dataclass
class StringToken(Token):
    val: str

@dataclass
class KeywordToken(Token):
    kw_name: str

@dataclass
class BooleanToken(Token):
    val: str

@dataclass
class BreakToken(Token):
    pass

@dataclass
class TypeToken(Token):
    type_name: str

@dataclass
class SemicolonToken(Token):
    pass

@dataclass
class CommaToken(Token):
    pass

@dataclass
class LeftBraceToken(Token):
    pass

@dataclass
class LeftSquareToken(Token):
    pass

@dataclass
class RightSquareToken(Token):
    pass

@dataclass
class RightBraceToken(Token):
    pass

@dataclass
class LeftParenToken(Token):
    pass

@dataclass
class RightParenToken(Token):
    pass

# ======================================================================================================
def lex(s: str) -> Iterator[Token]:
    i = 0
    # prev_char = None
    prev_token= None
    while True:
        while i < len(s) and s[i].isspace():
            i = i + 1

        if i >= len(s):
            return
        
        if s[i]==";":
            yield SemicolonToken()
            i+=1

        # variable or reserved keyword token
        elif s[i].isalpha():
            t = ""
            while i < len(s) and s[i].isalpha():
                t += s[i]
                i += 1
            if t in keyword_tokens:
                prevToken = KeywordToken(t)
                yield prevToken
            elif t=="break":
                yield BreakToken()
            elif t in boolean_tokens:
                yield BooleanToken(t)
            elif t in base_type_tokens:
                yield TypeToken(t)
            else:
                prevToken = VarToken(t)
                yield prevToken

        # string token
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

        # positive integers
        elif s[i].isdigit():
            t = s[i]
            prev_char = s[i]
            i = i + 1
            while i < len(s) and s[i].isdigit():
                t = t + s[i]
                i = i + 1
            prevToken = NumberToken(t)
            yield prevToken
        

        # Single-line and Inline comments: /~ ... ~/
        elif s[i:i+2] == "/~":
            i += 2  # skip "/~"
            while i < len(s) and s[i:i+2] != "~/":
                i += 1
            i += 2  # skip "~/"
            continue 

        # Multi-line comments: /~ { ... } ~/
        elif s[i:i+3] == "/~{":
            i += 3  # skip "/~{"
            while i < len(s) and s[i:i+3] != "}~/":
                i += 1
            i += 3  # skip "}~/"
            continue 
        
        else:
            match t := s[i]:
                case "-":
                    if (s[i+1]=="="):
                        i=i+2
                        yield OperatorToken("-=")
                    else:
                        # prev_char = s[i]
                        i = i + 1
                        # must be a number or a variable identifier
                        # consume all spaces
                        while i<len(s) and s[i].isspace():
                            i+=1

                        if s[i].isdigit():
                            # unary negation / subtration on a number
                            # is prevToken is digit or alpha, means subtraction, else unary neg
                            if isinstance(prevToken, NumberToken) or isinstance(prevToken, VarToken):
                                # means subtraction from a number or variable
                                yield OperatorToken('+') # example: -3 => +(-3)

                            # form the number
                            while i < len(s) and (s[i].isdigit() or s[i]=="."):
                                t += s[i] # with the leading `-` sign
                                i += 1
                            yield NumberToken(t)

                        # unary negation on a variable
                        elif s[i].isalpha():
                            while i < len(s) and s[i].isalpha():
                                t += s[i]
                                i += 1
                            yield NumberToken("-1")
                            yield OperatorToken("*")
                            yield VarToken(t[1:]) # variable name (identifier)

                case t if t in (base_operator_tokens+bitwise_ops):
                    prev_char = s[i]
                    i = i + 1
                    if i<len(s) and (t + s[i]) in top_level_operator_tokens:
                        prev_char = s[i]
                        i = i + 1
                        prevToken = OperatorToken(t + prev_char)
                    else:
                        prevToken = OperatorToken(t)
                    yield prevToken
                case '{':
                    i+=1
                    yield LeftBraceToken()
                case '}':
                    i+=1
                    yield RightBraceToken()
                case '(':
                    i+=1
                    yield LeftParenToken()
                case ')':
                    i+=1
                    yield RightParenToken()
                case '[':
                    i+=1
                    yield LeftSquareToken()
                case ']':
                    i+=1
                    yield RightSquareToken()
                case ',':
                    i+=1
                    yield CommaToken()


