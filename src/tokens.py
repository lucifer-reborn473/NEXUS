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
    "displayl",
    "fixed",
    # "loop",
    "while",
    "for",
    "PushFront",
    "PushBack",
    "PopFront",
    "PopBack",
    "Length",
    "Clear",
    "Insert",
    "Remove",
    "Add",
    "var",
    "ascii",
    "char",
    "fn",
    "fnrec",
    "or",
    "not",
    "and",
    "proc",
    "feed",
    "repeat",
    "typeof"
)

math_tokens = (
"abs",
"min",
"max",
"round",
"ceil",
"floor",
"truncate",
"sqrt",
"cbrt",
"pow",
"exp",
"log",
"log10",
"log2",
"sin",
"cos",
"tan",
"asin",
"acos",
"atan",
"atan2",
"sinh",
"cosh",
"tanh",
"asinh",
"acosh",
"atanh",
"PI",
"E",
)

boolean_tokens = (
    "True",
    "False",
)

base_type_tokens = (
    "integer",
    "decimal",
    "uinteger",
    "string",
    "array",
    "Hash",
    "boolean",
)

base_operator_tokens = (
    "+",
    "*",
    "-",
    "÷",
    "/",
    "<",
    ">",
    "=",
    "%",
    "!",
    "**",
)

compound_assigners = (
    "+=",
    "*=",
    "-=",
    "/=",
    "%=",
)

bitwise_ops=(
    "&",
    "|",
    "^",
    "~",
)

shift_ops=(
    "<<",
    ">>",
)

assignment = ("=",) + compound_assigners

logical_compounds = (
    "==",
    "!=",
    "<=",
    ">=",
)

top_level_operator_tokens = compound_assigners + logical_compounds +shift_ops
