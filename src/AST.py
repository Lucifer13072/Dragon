class Number:
    def __init__(self, value):
        self.value = value

class StringLiteral:
    def __init__(self, value):
        self.value = value
        
class Float:
    def __init__(self, value):
        self.value = value

class BoolLiteral:
    def __init__(self, value):
        self.value = value

class Var:
    def __init__(self, name):
        self.name = name

class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op  # например, PLUS, MINUS, MUL, DIV, EQ, NEQ, GT, LT, GTE, LTE, AND, OR
        self.right = right

class UnaryOp:
    def __init__(self, op, expr):
        self.op = op  # например, NOT
        self.expr = expr

class Assignment:
    def __init__(self, var_name, expr):
        self.var_name = var_name
        self.expr = expr

class FuncCall:
    def __init__(self, func_name, args):
        self.func_name = func_name
        self.args = args

# Новый узел для условного оператора if
class IfStatement:
    def __init__(self, clauses, else_block):
        """
        clauses: список кортежей (condition, block)
        else_block: блок инструкций (список), либо None
        """
        self.clauses = clauses
        self.else_block = else_block

class WhileStatement:
    def __init__(self, condition, body):
        self.condition = condition  # Условие
        self.body = body