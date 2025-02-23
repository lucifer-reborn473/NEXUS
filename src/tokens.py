"""
This module defines tuples of keyword, base type, and base operator tokens used in the Our_Compiler project.

Attributes:
    keyword_tokens (tuple): A tuple of keyword tokens.
    base_type_tokens (tuple): A tuple of base type tokens.
    base_operator_tokens (tuple): A tuple of base operator tokens.
"""

keyword_tokens = (
    "if",
    "else",
    "else if",
    "then",
    "end",
    "display",
    "loop",
    "var",
    "ascii",
    "char",
    "func",
    "or",
    "and",
    "proc",
)

base_type_tokens = (
    "integer",
    "decimal",
    "uinteger",
)

base_operator_tokens = (
    "+",
    "*",
    "-",
    "÷",
    "/",
    "(",
    ")",
    "<",
    ">",
    "=",
    "%",
    "!",
)

compound_assigners = (
    "+=",
    "*=",
    "-=",
    "/=",
    "%=",
)

assignment = ("=",) + compound_assigners

logical_compounds = (
    "==",
    "!=",
    "<=",
    ">=",
)

top_level_operator_tokens = compound_assigners + logical_compounds
