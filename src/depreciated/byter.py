HALT, NOP, PUSH, POP, ADD, SUB, MUL, NEG = range(8)

def execute(insns):
    ip = 0
    operand = []

    def push(x):
        operand.append(x)

    def pop():
        return operand.pop()

    while True:
        opcode = insns[ip]

        if opcode == HALT:
            break
        elif opcode == NOP:
            pass
        elif opcode == PUSH:
            ip += 1
            push(insns[ip])
        elif opcode == ADD:
            r = pop()
            l = pop()
            push(l + r)
        elif opcode == SUB:
            r = pop()
            l = pop()
            push(l - r)
        elif opcode == MUL:
            r = pop()
            l = pop()
            push(l * r)
        elif opcode == NEG:
            l = pop()
            push(-l)

        ip += 1

    return pop()

# Test the interpreter
insns = [
    PUSH, 2,
    PUSH, 3,
    ADD,  # 0 is ignored
    PUSH, 5,
    MUL,
    HALT, 0,
]

print(execute(insns))  # Output: 25
