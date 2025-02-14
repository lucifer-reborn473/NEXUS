from dataclasses import dataclass

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
    pass  # Token for the 'while' keyword

# Add any additional tokens as needed for your compiler project.