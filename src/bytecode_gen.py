from parser import *
from dataclasses import dataclass
from enum import IntEnum

# ================ OPCODE DEFINITIONS ================
# Create a structured enum for all opcodes (existing and new)
class OpCode(IntEnum):
    # Original opcodes
    HALT = 0
    NOP = 1
    PUSH = 2
    POP = 3
    ADD = 4
    SUB = 5
    MUL = 6
    NEG = 7
    DIV = 8
    MOD = 9
    POW = 10
    LT = 11
    GT = 12
    EQ = 13
    NEQ = 14
    LE = 15
    GE = 16
    AND = 17
    OR = 18
    BAND = 19
    BOR = 20
    BXOR = 21
    SHL = 22
    SHR = 23
    NOT = 24
    BNOT = 25
    ASCII = 26
    CHAR = 27
    VARBIND = 28
    DISPLAY = 29
    DISPLAYL = 30
    
    # New opcodes for remaining AST nodes
    ASSIGN = 31
    CALLARRAY = 32
    PUSHFRONT = 33
    PUSHBACK = 34
    POPFRONT = 35
    POPBACK = 36
    ASSIGNTOARRAY = 37
    CALLHASHVAL = 38
    ADDHASHPAIR = 39
    REMOVEHASHPAIR = 40
    ASSIGNHASHVAL = 41
    ASSIGNFULLARRAY = 42
    INSERTAT = 43
    REMOVEAT = 44
    GETLENGTH = 45
    CLEARARRAY = 46
    JUMP = 47
    JUMP_IF_TRUE = 48
    JUMP_IF_FALSE = 49
    LABEL = 50
    FEED = 51
    FUNC_DEF = 52
    FUNC_CALL = 53
    RETURN = 54
    BREAK = 55
    MOVEON = 56
    COMPOUND_ASSIGN = 57


# ================ BYTECODE GENERATOR CLASS ================
class BytecodeGenerator:
    def __init__(self):
        self.code = []
        self.labels = {}
        self.pending_jumps = []
        self.label_counter = 0
        
    def create_label(self):
        """Create a new label for control flow"""
        label_id = self.label_counter
        self.label_counter += 1
        return label_id
        
    def place_label(self, label_id):
        """Place a label at the current position in code"""
        self.labels[label_id] = len(self.code)
        
    def emit_jump(self, opcode, label_id):
        """Emit a jump instruction with placeholder target"""
        self.code.append(opcode)
        jump_pos = len(self.code)
        self.code.append(0)  # Placeholder
        self.pending_jumps.append((jump_pos, label_id))
        
    def patch_jumps(self):
        """Replace jump placeholders with actual offsets"""
        for pos, label_id in self.pending_jumps:
            if label_id in self.labels:
                self.code[pos] = self.labels[label_id] - pos
            else:
                raise ValueError(f"Label {label_id} not defined")
                
    def push_string(self, s):
        """Add a string to the bytecode"""
        bytes_val = s.encode('utf-8')
        self.code.append(len(bytes_val))
        self.code.extend(bytes_val)
        
    def generate(self, ast, scope):
        """Generate bytecode for an entire AST"""
        for statement in ast.statements:
            self.generate_node(statement, scope)
            
        self.code.append(OpCode.HALT)
        self.patch_jumps()
        return self.code
        
    def generate_node(self, node, scope):
        """Generate bytecode for a single AST node"""
        # Delegate to specific handler methods based on node type
        if isinstance(node, Number):
            self.handle_number(node)
        elif isinstance(node, BinOp):
            self.handle_binop(node, scope)
        elif isinstance(node, UnaryOp):
            self.handle_unaryop(node, scope)
        elif isinstance(node, String):
            self.handle_string(node)
        elif isinstance(node, Boolean):
            self.handle_boolean(node)
        elif isinstance(node, Variable):
            self.handle_variable(node)
        elif isinstance(node, Array):
            self.handle_array(node, scope)
        elif isinstance(node, Hash):
            self.handle_hash(node, scope)
        elif isinstance(node, VarBind):
            self.handle_varbind(node, scope)
        elif isinstance(node, Display):
            self.handle_display(node, scope)
        elif isinstance(node, DisplayL):
            self.handle_displayl(node, scope)
        elif isinstance(node, CallArr):
            self.handle_callarray(node, scope)
        elif isinstance(node, PushFront):
            self.handle_pushfront(node, scope)
        elif isinstance(node, PushBack):
            self.handle_pushback(node, scope)
        elif isinstance(node, PopFront):
            self.handle_popfront(node)
        elif isinstance(node, PopBack):
            self.handle_popback(node)
        elif isinstance(node, AssigntoArr):
            self.handle_assigntoarray(node, scope)
        elif isinstance(node, CallHashVal):
            self.handle_callhashval(node, scope)
        elif isinstance(node, AddHashPair):
            self.handle_addhashpair(node, scope)
        elif isinstance(node, RemoveHashPair):
            self.handle_removehashpair(node, scope)
        elif isinstance(node, AssignHashVal):
            self.handle_assignhashval(node, scope)
        elif isinstance(node, AssignFullArray):
            self.handle_assignfullarray(node, scope)
        elif isinstance(node, InsertAt):
            self.handle_insertat(node, scope)
        elif isinstance(node, RemoveAt):
            self.handle_removeat(node, scope)
        elif isinstance(node, GetLength):
            self.handle_getlength(node)
        elif isinstance(node, ClearArray):
            self.handle_cleararray(node)
        elif isinstance(node, Break):
            self.handle_break()
        elif isinstance(node, CompoundAssignment):
            self.handle_compoundassignment(node, scope)
        elif isinstance(node, WhileLoop):
            self.handle_whileloop(node, scope)
        elif isinstance(node, Feed):
            self.handle_feed(node, scope)
        elif isinstance(node, ForLoop):
            self.handle_forloop(node, scope)
        elif isinstance(node, BreakOut):
            self.handle_breakout()
        elif isinstance(node, MoveOn):
            self.handle_moveon()
        elif isinstance(node, AssignToVar):
            self.handle_assigntovar(node, scope)
        elif isinstance(node, If):
            self.handle_if(node, scope)
        elif isinstance(node, FuncDef):
            self.handle_funcdef(node, scope)
        elif isinstance(node, FuncCall):
            self.handle_funccall(node, scope)
        
    # ================ NODE HANDLER METHODS ================
    def handle_number(self, node):
        """Handle Number node"""
        self.code.append(OpCode.PUSH)
        num = int(node.val)
        num_bytes = num.to_bytes((num.bit_length() + 7) // 8 or 1, byteorder='big', signed=True)
        self.code.append(len(num_bytes))
        self.code.extend(num_bytes)
    
    def handle_binop(self, node, scope):
        """Handle BinOp node"""
        op_map = {
            "+": OpCode.ADD, "-": OpCode.SUB, "*": OpCode.MUL, "/": OpCode.DIV,
            "%": OpCode.MOD, "^": OpCode.POW, "<": OpCode.LT, ">": OpCode.GT,
            "==": OpCode.EQ, "!=": OpCode.NEQ, "<=": OpCode.LE, ">=": OpCode.GE,
            "and": OpCode.AND, "or": OpCode.OR, "&": OpCode.BAND, "|": OpCode.BOR,
            "<<": OpCode.SHL, ">>": OpCode.SHR
        }
        
        # Special cases for unary-like binary operators
        if node.op in ["not", "~"]:
            self.generate_node(node.left, scope)
            self.code.append(OpCode.NOT if node.op == "not" else OpCode.BNOT)
            return
            
        self.generate_node(node.left, scope)
        self.generate_node(node.right, scope)
        self.code.append(op_map.get(node.op))
    
    def handle_unaryop(self, node, scope):
        """Handle UnaryOp node"""
        self.generate_node(node.val, scope)
        
        if node.op == "~":
            self.code.append(OpCode.BNOT)
        elif node.op in ["not", "!"]:
            self.code.append(OpCode.NOT)
        elif node.op == "ascii":
            self.code.append(OpCode.ASCII)
        elif node.op == "char":
            self.code.append(OpCode.CHAR)
    
    def handle_string(self, node):
        """Handle String node"""
        self.code.append(OpCode.PUSH)
        self.push_string(node.val)
    
    def handle_boolean(self, node):
        """Handle Boolean node"""
        self.code.append(OpCode.PUSH)
        self.code.append(1 if node.val else 0)
    
    def handle_variable(self, node):
        """Handle Variable node"""
        self.code.append(OpCode.PUSH)
        self.push_string(node.var_name)
    
    def handle_array(self, node, scope):
        """Handle Array node"""
        for element in node.val:
            self.generate_node(element, scope)
        self.code.append(OpCode.PUSH)
        self.code.append(len(node.val))
    
    def handle_hash(self, node, scope):
        """Handle Hash node"""
        for k, v in node.val:
            self.generate_node(k, scope)
            self.generate_node(v, scope)
        self.code.append(OpCode.PUSH)
        self.code.append(len(node.val))
    
    def handle_varbind(self, node, scope):
        """Handle VarBind node"""
        self.generate_node(node.val, scope)
        self.code.append(OpCode.VARBIND)
        self.push_string(node.var_name)
    
    def handle_display(self, node, scope):
        """Handle Display node"""
        self.generate_node(node.val, scope)
        self.code.append(OpCode.DISPLAY)
    
    def handle_displayl(self, node, scope):
        """Handle DisplayL node"""
        self.generate_node(node.val, scope)
        self.code.append(OpCode.DISPLAYL)
    
    def handle_callarray(self, node, scope):
        """Handle CallArr node"""
        self.code.append(OpCode.PUSH)
        self.push_string(node.xname)
        self.generate_node(node.index, scope)
        self.code.append(OpCode.CALLARRAY)
    
    def handle_pushfront(self, node, scope):
        """Handle PushFront node"""
        self.code.append(OpCode.PUSH)
        self.push_string(node.xname)
        self.generate_node(node.val, scope)
        self.code.append(OpCode.PUSHFRONT)
    
    def handle_pushback(self, node, scope):
        """Handle PushBack node"""
        self.code.append(OpCode.PUSH)
        self.push_string(node.xname)
        self.generate_node(node.val, scope)
        self.code.append(OpCode.PUSHBACK)
    
    def handle_popfront(self, node):
        """Handle PopFront node"""
        self.code.append(OpCode.PUSH)
        self.push_string(node.xname)
        self.code.append(OpCode.POPFRONT)
    
    def handle_popback(self, node):
        """Handle PopBack node"""
        self.code.append(OpCode.PUSH)
        self.push_string(node.xname)
        self.code.append(OpCode.POPBACK)
    
    def handle_assigntoarray(self, node, scope):
        """Handle AssigntoArr node"""
        self.code.append(OpCode.PUSH)
        self.push_string(node.xname)
        self.generate_node(node.index, scope)
        self.generate_node(node.val, scope)
        self.code.append(OpCode.ASSIGNTOARRAY)
    
    def handle_callhashval(self, node, scope):
        """Handle CallHashVal node"""
        self.code.append(OpCode.PUSH)
        self.push_string(node.name)
        self.generate_node(node.key, scope)
        self.code.append(OpCode.CALLHASHVAL)
    
    def handle_addhashpair(self, node, scope):
        """Handle AddHashPair node"""
        self.code.append(OpCode.PUSH)
        self.push_string(node.name)
        self.generate_node(node.key, scope)
        self.generate_node(node.val, scope)
        self.code.append(OpCode.ADDHASHPAIR)
    
    def handle_removehashpair(self, node, scope):
        """Handle RemoveHashPair node"""
        self.code.append(OpCode.PUSH)
        self.push_string(node.name)
        self.generate_node(node.key, scope)
        self.code.append(OpCode.REMOVEHASHPAIR)
    
    def handle_assignhashval(self, node, scope):
        """Handle AssignHashVal node"""
        self.code.append(OpCode.PUSH)
        self.push_string(node.name)
        self.generate_node(node.key, scope)
        self.generate_node(node.new_val, scope)
        self.code.append(OpCode.ASSIGNHASHVAL)
    
    def handle_assignfullarray(self, node, scope):
        """Handle AssignFullArray node"""
        self.code.append(OpCode.PUSH)
        self.push_string(node.xname)
        for element in node.val:
            self.generate_node(element, scope)
        self.code.append(OpCode.PUSH)
        self.code.append(len(node.val))
        self.code.append(OpCode.ASSIGNFULLARRAY)
    
    def handle_insertat(self, node, scope):
        """Handle InsertAt node"""
        self.code.append(OpCode.PUSH)
        self.push_string(node.xname)
        self.generate_node(node.index, scope)
        self.generate_node(node.val, scope)
        self.code.append(OpCode.INSERTAT)
    
    def handle_removeat(self, node, scope):
        """Handle RemoveAt node"""
        self.code.append(OpCode.PUSH)
        self.push_string(node.xname)
        self.generate_node(node.index, scope)
        self.code.append(OpCode.REMOVEAT)
    
    def handle_getlength(self, node):
        """Handle GetLength node"""
        self.code.append(OpCode.PUSH)
        self.push_string(node.xname)
        self.code.append(OpCode.GETLENGTH)
    
    def handle_cleararray(self, node):
        """Handle ClearArray node"""
        self.code.append(OpCode.PUSH)
        self.push_string(node.xname)
        self.code.append(OpCode.CLEARARRAY)
    
    def handle_break(self):
        """Handle Break node"""
        self.code.append(OpCode.BREAK)
    
    def handle_compoundassignment(self, node, scope):
        """Handle CompoundAssignment node"""
        # Get current value
        self.code.append(OpCode.PUSH)
        self.push_string(node.var_name)
        
        # Get new value to apply operation with
        self.generate_node(node.val, scope)
        
        # Apply operation
        op_map = {
            "+": OpCode.ADD, "-": OpCode.SUB, "*": OpCode.MUL, "/": OpCode.DIV,
            "%": OpCode.MOD, "^": OpCode.POW, "&": OpCode.BAND, "|": OpCode.BOR,
            "<<": OpCode.SHL, ">>": OpCode.SHR
        }
        self.code.append(op_map.get(node.op, OpCode.ADD))
        
        # Store back to variable
        self.code.append(OpCode.ASSIGN)
        self.push_string(node.var_name)
    
    def handle_whileloop(self, node, scope):
        """Handle WhileLoop node"""
        # Create labels for loop start and end
        loop_start = self.create_label()
        loop_end = self.create_label()
        
        # Place start label
        self.place_label(loop_start)
        
        # Generate condition code
        self.generate_node(node.condition, node.whileScope)
        
        # Jump to end if condition is false
        self.emit_jump(OpCode.JUMP_IF_FALSE, loop_end)
        
        # Generate loop body
        for stmt in node.body.statements:
            self.generate_node(stmt, node.whileScope)
        
        # Jump back to condition
        self.emit_jump(OpCode.JUMP, loop_start)
        
        # Place end label
        self.place_label(loop_end)
    
    def handle_feed(self, node, scope):
        """Handle Feed node"""
        self.generate_node(node.msg, scope)
        self.code.append(OpCode.FEED)
    
    def handle_forloop(self, node, scope):
        """Handle ForLoop node"""
        # Generate initialization code
        self.generate_node(node.initialization, node.forScope)
        
        # Create labels for loop
        loop_start = self.create_label()
        loop_end = self.create_label()
        
        # Place start label
        self.place_label(loop_start)
        
        # Generate condition
        self.generate_node(node.condition, node.forScope)
        
        # Jump to end if condition is false
        self.emit_jump(OpCode.JUMP_IF_FALSE, loop_end)
        
        # Generate loop body
        for stmt in node.body.statements:
            self.generate_node(stmt, node.forScope)
        
        # Generate increment code
        self.generate_node(node.increment, node.forScope)
        
        # Jump back to condition
        self.emit_jump(OpCode.JUMP, loop_start)
        
        # Place end label
        self.place_label(loop_end)
    
    def handle_breakout(self):
        """Handle BreakOut node"""
        self.code.append(OpCode.BREAK)
    
    def handle_moveon(self):
        """Handle MoveOn node"""
        self.code.append(OpCode.MOVEON)
    
    def handle_assigntovar(self, node, scope):
        """Handle AssignToVar node"""
        self.generate_node(node.val, scope)
        self.code.append(OpCode.ASSIGN)
        self.push_string(node.var_name)
    
    def handle_if(self, node, scope):
        """Handle If node"""
        # Create labels for then and end
        else_label = self.create_label()
        end_label = self.create_label()
        
        # Generate condition
        self.generate_node(node.c, node.condScope)
        
        # Jump to else if condition is false
        self.emit_jump(OpCode.JUMP_IF_FALSE, else_label)
        
        # Generate then branch
        if node.t:
            if hasattr(node.t, 'statements'):
                for stmt in node.t.statements:
                    self.generate_node(stmt, node.condScope)
            else:
                self.generate_node(node.t, node.condScope)
        
        # Jump to end (after else branch)
        self.emit_jump(OpCode.JUMP, end_label)
        
        # Place else label
        self.place_label(else_label)
        
        # Generate else branch
        if node.e:
            if hasattr(node.e, 'statements'):
                for stmt in node.e.statements:
                    self.generate_node(stmt, node.condScope)
            else:
                self.generate_node(node.e, node.condScope)
        
        # Place end label
        self.place_label(end_label)
    
    def handle_funcdef(self, node, scope):
        """Handle FuncDef node"""
        # Create labels for function body and after function
        func_start = self.create_label()
        func_end = self.create_label()
        
        # Jump over function body
        self.emit_jump(OpCode.JUMP, func_end)
        
        # Place function start label
        self.place_label(func_start)
        
        # Generate function body
        if hasattr(node.funcBody, 'statements'):
            for stmt in node.funcBody.statements:
                self.generate_node(stmt, node.funcScope)
        else:
            self.generate_node(node.funcBody, node.funcScope)
        
        # Add return instruction
        self.code.append(OpCode.RETURN)
        
        # Place function end label
        self.place_label(func_end)
        
        # Define function in bytecode
        self.code.append(OpCode.FUNC_DEF)
        self.push_string(node.funcName)
        self.code.append(func_start)
        self.code.append(len(node.funcParams))
        self.code.append(1 if node.isRec else 0)
    
    def handle_funccall(self, node, scope):
        """Handle FuncCall node"""
        # Push arguments onto stack
        for arg in node.funcArgs:
            self.generate_node(arg, scope)
        
        # Call function
        self.code.append(OpCode.FUNC_CALL)
        self.push_string(node.funcName)
        self.code.append(len(node.funcArgs))


# ================ WRAPPER FUNCTION ================
def codegen(ast, scope, not_list=False):
    """Generate bytecode for an AST"""
    generator = BytecodeGenerator()
    bytecode = generator.generate(ast, scope)
    
    if not_list:
        return bytecode
    else:
        return bytearray(bytecode)

if __name__ == "__main__":
    # Example usage
    code ="""var x = 10;
    var y = 20;
    var z = x + y;
    display z;
    """

    code="""
    var x = 10;

    if x > 5 then {
        displayl "x is greater than 5";
    } else {
        displayl "x is 5 or less";
    } end;

    while (x > 0) {
        displayl x;
        x = x - 1;
    }
"""

    code ="""
    var x = 10;
var arr = [1, 2, 3];
var hash = {"key1": 10, "key2": 20};

arr.PushBack(4);
hash.Add("key3", 30);

fn multiply(a, b) {
     a * b;
}


if x > 5 then {
    displayl "x is greater than 5";
} else {
    displayl "x is 5 or less";
} end;

while (x > 0) {
    displayl x;
    x = x - 1;
}
displayl ("array display:");
for (var integer i = 0; i < arr.Length; i = i + 1) {
    displayl arr[i];
}

displayl multiply(hash["key1"], 2);
"""
    ast,scope = parse(code)  # Assuming parse function is defined elsewhere
    # pprint(ast)
    pprint(codegen(ast,scope,True))
