from parser import *
from pprint import pprint

HALT, NOP, PUSH, POP, ADD, SUB, MUL, NEG = range(8)

def do_codegen(t, code):
    match t:
        case Number(v):
            code.append(PUSH)
            code.append(int(v))
        case BinOp("+", l, r):
            do_codegen(l, code)
            do_codegen(r, code)
            code.append(ADD)
        case BinOp("-", l, r):
            do_codegen(l, code)
            do_codegen(r, code)
            code.append(SUB)
        case BinOp("*", l, r):
            do_codegen(l, code)
            do_codegen(r, code)
            code.append(MUL)
    return code

def codegen(ast):
    bytecode = bytearray()
    for statement in ast.statements:
        do_codegen(statement, bytecode)
    bytecode.append(HALT)
    return bytecode

