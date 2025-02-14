from dataclasses import dataclass
from typing import Any
from context import Context

context = Context()  # context as a global variable

def e(tree: Any) -> Any:
    match tree:
        case Number(n):
            return int(n)
        case String(s):
            return s
        case Variable(v):
            if context.has_variable(v):
                return context.get_variable(v).value
            else:
                raise NameError(f"name '{v}' is not defined")
        
        # Operators
        case BinOp("+", l, r):
            return e(l) + e(r)
        case BinOp("*", l, r):
            return e(l) * e(r)
        case BinOp("-", l, r):
            return e(l) - e(r)
        case BinOp("÷", l, r):
            return e(l) / e(r)
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
        case BinOp("%", l, r):
            return e(l) % e(r)
        
        case UnaryOp("~", val):
            return ~e(val)
        case UnaryOp("!", val):
            return not e(val)
        
        # Conditional
        case If(cond, sat, else_):
            return e(sat) if e(cond) else e(else_)
        
        # Display
        case Display(val):
            return print(e(val))
        
        # While loop
        case While(cond, body):
            while e(cond):
                e(body)
        
        # Variables (evaluates to value)
        case CompoundAssignment(var_name, op, value):
            var_value = context.get_variable(var_name).value
            var_value_updated = e(BinOp(op[0], Number(var_value), value))
            context.update_variable(var_name, var_value_updated)
            return var_value_updated
        
        case Binding(name, dtype, value):
            value = e(value)
            context.add_variable(name, value, dtype)
            return value

        # Add other cases as necessary for your AST nodes

if __name__ == "__main__":
    # Entry point for testing or running the evaluator
    pass