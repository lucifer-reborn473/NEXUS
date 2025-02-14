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
                    if (s[i+1] == "="):
                        i += 2
                        yield OperatorToken("-=")
                    elif (
                        prev_char is None or prev_char in "+-*/(<>!=%"
                    ):  # check if it is a negative number
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
                            # yield (-1 * varibleIdentifier) <= 3 tokens
                            yield NumberToken("-1")
                            yield OperatorToken("*")
                            yield VarToken(t[1:])  # variable name
                    else:  # check if it is a token
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
                case "w":
                    if s[i:i+4] == "while":
                        i += 5  # skip "while"
                        yield WhileToken()
                case _:
                    prev_char = s[i]
                    i += 1

# ==========================================================================================
# ================================= END OF LEXER ==========================================
