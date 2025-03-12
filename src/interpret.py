import sys

from tokens import *
from AST import *

def to_int(val):
    if isinstance(val, int):
        return val
    if isinstance(val, str):
        try:
            return int(val)
        except ValueError:
            return None
    return None

class Interpreter:
    def __init__(self, statements):
        self.statements = statements
        self.env = {}
    
    def run(self):
        for stmt in self.statements:
            self.eval(stmt)
    
    def eval(self, node):
        # Вспомогательные функции преобразования типов
        def to_number(x):
            if isinstance(x, bool):
                return 1 if x else 0
            if isinstance(x, (int, float)):
                return x
            if isinstance(x, str):
                try:
                    return float(x) if '.' in x else int(x)
                except ValueError:
                    return 0
            return 0

        def to_bool(x):
            if isinstance(x, bool):
                return x
            if isinstance(x, (int, float)):
                return x != 0
            if isinstance(x, str):
                return len(x) > 0
            return False

        # Обработка узлов AST
        if isinstance(node, Number):
            return int(node.value)
        elif isinstance(node, Float):
            return float(node.value)
        elif isinstance(node, BoolLiteral):
            return bool(node.value)
        elif isinstance(node, StringLiteral):
            return str(node.value)
        elif isinstance(node, Var):
            if node.name in self.env:
                return self.env[node.name]
            raise NameError(f"Переменная '{node.name}' не определена")

        # Бинарные операции
        elif isinstance(node, BinOp):
            left = self.eval(node.left)
            right = self.eval(node.right)
            op = node.op

            # Арифметические операции
            if op in {TOKENS["PLUS"], TOKENS["MINUS"], TOKENS["MUL"], TOKENS["DIV"]}:
                left_num = to_number(left)
                right_num = to_number(right)
                
                if op == TOKENS["PLUS"]:
                    if isinstance(left, str) or isinstance(right, str):
                        return f"{left}{right}"
                    return left_num + right_num
                elif op == TOKENS["MINUS"]:
                    return left_num - right_num
                elif op == TOKENS["MUL"]:
                    if isinstance(left, str) and isinstance(right_num, int):
                        return left * right_num
                    return left_num * right_num
                elif op == TOKENS["DIV"]:
                    if right_num == 0:
                        raise ZeroDivisionError("Деление на ноль")
                    return left_num / right_num

            # Сравнения
            elif op in {TOKENS["EQ"], TOKENS["NEQ"], TOKENS["GT"], TOKENS["LT"], TOKENS["GTE"], TOKENS["LTE"]}:
                if op == TOKENS["EQ"]:
                    return left == right
                elif op == TOKENS["NEQ"]:
                    return left != right
                return to_number(left) > to_number(right) if "G" in op else to_number(left) < to_number(right)

            # Логические операции
            elif op == TOKENS["AND"]:
                return to_bool(left) and to_bool(right)
            elif op == TOKENS["OR"]:
                return to_bool(left) or to_bool(right)

            raise ValueError(f"Неизвестный оператор: {op}")

        # Унарные операции
        elif isinstance(node, UnaryOp):
            value = self.eval(node.expr)
            if node.op == TOKENS["NOT"]:
                return not to_bool(value)
            elif node.op == TOKENS["MINUS"]:
                return -to_number(value)
            raise ValueError(f"Неизвестный унарный оператор: {node.op}")

        # Присваивание
        elif isinstance(node, Assignment):
            value = self.eval(node.expr)
            self.env[node.var_name] = value
            return value

        # Вызов функции
        elif isinstance(node, FuncCall):
            func_name = node.func_name
            args = [self.eval(arg) for arg in node.args]

            if func_name == "write":
                return input(args[0] if args else "")
            elif func_name == "output":
                print(*args)
            elif func_name == "int":
                return int(args[0])
            elif func_name == "float":
                return float(args[0])
            elif func_name == "str":
                return str(args[0])
            elif func_name == "bool":
                return bool(to_bool(args[0]))
            else:
                raise NameError(f"Функция '{func_name}' не определена")

        # Условные конструкции
        elif isinstance(node, IfStatement):
            for condition, block in node.clauses:
                if to_bool(self.eval(condition)):
                    result = None
                    for stmt in block:
                        result = self.eval(stmt)
                    return result
            if node.else_block:
                result = None
                for stmt in node.else_block:
                    result = self.eval(stmt)
                return result
            return None

        if isinstance(node, WhileStatement):
            while self.eval(node.condition):
                for stmt in node.body:
                    self.eval(stmt)
            return None
        
        else:
            raise RuntimeError(f"Неизвестный тип узла: {type(node)}")