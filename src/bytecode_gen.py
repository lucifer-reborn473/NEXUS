from parser import *
from pprint import pprint

HALT, NOP, PUSH, POP, ADD, SUB, MUL, NEG = range(8)
DIV, MOD, POW, LT, GT, EQ, NEQ, LE, GE, AND, OR, BAND, BOR, BXOR, SHL, SHR, NOT, BNOT, ASCII, CHAR = range(8, 28)
VARBIND, DISPLAY, DISPLAYL = range(28, 31)  # Add new opcodes

def do_codegen(t, code, scope):
    match t:
        case Number(v):
            code.append(PUSH)
            code.append(int(v))
        case BinOp("+", l, r):
            do_codegen(l, code, scope)
            do_codegen(r, code, scope)
            code.append(ADD)
        case BinOp("-", l, r):
            do_codegen(l, code, scope)
            do_codegen(r, code, scope)
            code.append(SUB)
        case BinOp("*", l, r):
            do_codegen(l, code, scope)
            do_codegen(r, code, scope)
            code.append(MUL)
        case BinOp("÷", l, r) | BinOp("/", l, r):
            do_codegen(l, code, scope)
            do_codegen(r, code, scope)
            code.append(DIV)
        case BinOp("%", l, r):
            do_codegen(l, code, scope)
            do_codegen(r, code, scope)
            code.append(MOD)
        case BinOp("^", l, r):
            do_codegen(l, code, scope)
            do_codegen(r, code, scope)
            code.append(POW)
        case BinOp("<", l, r):
            do_codegen(l, code, scope)
            do_codegen(r, code, scope)
            code.append(LT)
        case BinOp(">", l, r):
            do_codegen(l, code, scope)
            do_codegen(r, code, scope)
            code.append(GT)
        case BinOp("==", l, r):
            do_codegen(l, code, scope)
            do_codegen(r, code, scope)
            code.append(EQ)
        case BinOp("!=", l, r):
            do_codegen(l, code, scope)
            do_codegen(r, code, scope)
            code.append(NEQ)
        case BinOp("<=", l, r):
            do_codegen(l, code, scope)
            do_codegen(r, code, scope)
            code.append(LE)
        case BinOp(">=", l, r):
            do_codegen(l, code, scope)
            do_codegen(r, code, scope)
            code.append(GE)
        case BinOp("and", l, r):
            do_codegen(l, code, scope)
            do_codegen(r, code, scope)
            code.append(AND)
        case BinOp("or", l, r):
            do_codegen(l, code, scope)
            do_codegen(r, code, scope)
            code.append(OR)
        case BinOp("&", l, r):
            do_codegen(l, code, scope)
            do_codegen(r, code, scope)
            code.append(BAND)
        case BinOp("|", l, r):
            do_codegen(l, code, scope)
            do_codegen(r, code, scope)
            code.append(BOR)
        case BinOp("<<", l, r):
            do_codegen(l, code, scope)
            do_codegen(r, code, scope)
            code.append(SHL)
        case BinOp(">>", l, r):
            do_codegen(l, code, scope)
            do_codegen(r, code, scope)
            code.append(SHR)
        case BinOp("not", l, _):
            do_codegen(l, code, scope)
            code.append(NOT)
        case BinOp("~", l, _):
            do_codegen(l, code, scope)
            code.append(BNOT)
        case UnaryOp("~", val):
            do_codegen(val, code, scope)
            code.append(BNOT)
        case UnaryOp("not", val) | UnaryOp("!", val):
            do_codegen(val, code, scope)
            code.append(NOT)
        case UnaryOp("ascii", val):
            do_codegen(val, code, scope)
            code.append(ASCII)
        case UnaryOp("char", val):
            do_codegen(val, code, scope)
            code.append(CHAR)
        case String(s):
            code.append(PUSH)
            code.extend(s.encode('utf-8'))  # Encode string as bytes
        case Boolean(b):
            code.append(PUSH)
            code.append(1 if b else 0)
        case Variable(v):
            code.append(PUSH)
            val = scope.lookup(v)
            code.extend(val)  # Encode variable name as bytes
        case Array(val):
            for element in val:
                do_codegen(element, code, scope)
            code.append(PUSH)
            code.append(len(val))  # Push array size
        case Hash(val):
            for k, v in val.items():
                do_codegen(k, code, scope)
                do_codegen(v, code, scope)
            code.append(PUSH)
            code.append(len(val))  # Push hash size
        case VarBind(name, dtype, value, category):
            do_codegen(value, code, scope)  # Generate code for the value
            code.append(VARBIND)
            code.extend(name.encode('utf-8'))  # Push variable name as bytes
        case Display(val):
            do_codegen(val, code, scope)  # Generate code for the value
            code.append(DISPLAY)
        case DisplayL(val):
            do_codegen(val, code, scope)  # Generate code for the value
            code.append(DISPLAYL)
    return code

def codegen(ast,scope,not_list=False):
    bytecode = bytearray()
    if (not_list):
        bytecode=[]
    for statement in ast.statements:
        do_codegen(statement, bytecode,scope)
    bytecode.append(HALT)
    return bytecode

