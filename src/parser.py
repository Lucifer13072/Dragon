import sys
from tokens import *
from interpret import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[self.pos]
    
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.pos += 1
            self.current_token = self.tokens[self.pos]
        else:
            raise Exception(f"Ошибка парсинга: ожидался {token_type}, получено {self.current_token.type}")
    
    def parse(self):
        statements = []
        while self.current_token.type != "EOF":
            stmt = self.parse_statement()
            statements.append(stmt)
        return statements

    def parse_statement(self):
        # Распознаём if как специальный синтаксический элемент
        if self.current_token.type == TOKENS["IDENT"] and self.current_token.value == "if":
            return self.parse_if_statement()
        # Если это присваивание
        if self.current_token.type == TOKENS["IDENT"]:
            next_token = self.tokens[self.pos+1]
            if next_token.type in (TOKENS["ASSIGN"], TOKENS["ARROW"]):
                return self.parse_assignment()
            else:
                stmt = self.parse_expr()
                if self.current_token.type == TOKENS["SEMICOLON"]:
                    self.eat(TOKENS["SEMICOLON"])
                return stmt
        else:
            stmt = self.parse_expr()
            if self.current_token.type == TOKENS["SEMICOLON"]:
                self.eat(TOKENS["SEMICOLON"])
            return stmt

    def parse_assignment(self):
        var_token = self.current_token
        self.eat(TOKENS["IDENT"])
        if self.current_token.type in (TOKENS["ASSIGN"], TOKENS["ARROW"]):
            self.eat(self.current_token.type)
        else:
            raise Exception("Ожидался оператор присваивания")
        expr = self.parse_expr()
        if self.current_token.type == TOKENS["SEMICOLON"]:
            self.eat(TOKENS["SEMICOLON"])
        return Assignment(var_token.value, expr)

    # Метод для распознавания блока инструкций внутри фигурных скобок
    def parse_block(self):
        self.eat(TOKENS["LBRACE"])
        statements = []
        while self.current_token.type != TOKENS["RBRACE"]:
            statements.append(self.parse_statement())
        self.eat(TOKENS["RBRACE"])
        return statements

    # Метод для распознавания условного оператора if
    def parse_if_statement(self):
        # Ожидаем "if"
        self.eat(TOKENS["IDENT"])  # потребляем "if"
        self.eat(TOKENS["LPAREN"])
        condition = self.parse_expr()
        self.eat(TOKENS["RPAREN"])
        block = self.parse_block()
        clauses = [(condition, block)]
        else_block = None
        # Обрабатываем цепочку "else if" и "else"
        while self.current_token.type == TOKENS["IDENT"] and self.current_token.value == "else":
            self.eat(TOKENS["IDENT"])  # потребляем "else"
            if self.current_token.type == TOKENS["IDENT"] and self.current_token.value == "if":
                self.eat(TOKENS["IDENT"])  # потребляем "if"
                self.eat(TOKENS["LPAREN"])
                condition = self.parse_expr()
                self.eat(TOKENS["RPAREN"])
                block = self.parse_block()
                clauses.append((condition, block))
            else:
                else_block = self.parse_block()
                break
        return IfStatement(clauses, else_block)

    def parse_expr(self):
        return self.parse_or()

    def parse_or(self):
        node = self.parse_and()
        while self.current_token.type == TOKENS["OR"]:
            op = self.current_token
            self.eat(TOKENS["OR"])
            right = self.parse_and()
            node = BinOp(node, op.type, right)
        return node

    def parse_and(self):
        node = self.parse_equality()
        while self.current_token.type == TOKENS["AND"]:
            op = self.current_token
            self.eat(TOKENS["AND"])
            right = self.parse_equality()
            node = BinOp(node, op.type, right)
        return node

    def parse_equality(self):
        node = self.parse_relational()
        while self.current_token.type in (TOKENS["EQ"], TOKENS["NEQ"]):
            op = self.current_token
            self.eat(op.type)
            right = self.parse_relational()
            node = BinOp(node, op.type, right)
        return node

    def parse_relational(self):
        node = self.parse_add()
        while self.current_token.type in (TOKENS["GT"], TOKENS["LT"], TOKENS["GTE"], TOKENS["LTE"]):
            op = self.current_token
            self.eat(op.type)
            right = self.parse_add()
            node = BinOp(node, op.type, right)
        return node

    def parse_add(self):
        node = self.parse_term()
        while self.current_token.type in (TOKENS["PLUS"], TOKENS["MINUS"]):
            op = self.current_token
            self.eat(op.type)
            right = self.parse_term()
            node = BinOp(node, op.type, right)
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.current_token.type in (TOKENS["MUL"], TOKENS["DIV"]):
            op = self.current_token
            self.eat(op.type)
            right = self.parse_factor()
            node = BinOp(node, op.type, right)
        return node

    def parse_factor(self):
        token = self.current_token
        if token.type == TOKENS["NUMBER"]:
            self.eat(TOKENS["NUMBER"])
            return Number(token.value)
        elif token.type == TOKENS["FLOAT"]:
            self.eat(TOKENS["FLOAT"])
            return Float(token.value)
        elif token.type == TOKENS["BOOL"]:
            self.eat(TOKENS["BOOL"])
            return BoolLiteral(token.value)
        elif token.type == TOKENS["STRING"]:
            self.eat(TOKENS["STRING"])
            return StringLiteral(token.value)
        elif token.type == TOKENS["IDENT"]:
            # Если следующий токен — открывающая круглая скобка, это вызов функции
            if self.tokens[self.pos+1].type == TOKENS["LPAREN"]:
                return self.parse_func_call()
            else:
                self.eat(TOKENS["IDENT"])
                return Var(token.value)
        elif token.type == TOKENS["LPAREN"]:
            self.eat(TOKENS["LPAREN"])
            node = self.parse_expr()
            self.eat(TOKENS["RPAREN"])
            return node
        elif token.type == TOKENS["NOT"]:
            self.eat(TOKENS["NOT"])
            expr = self.parse_factor()
            return UnaryOp(TOKENS["NOT"], expr)
        else:
            raise Exception(f"Ошибка парсинга в факторе: {token.type}")

    def parse_func_call(self):
        func_name = self.current_token.value
        self.eat(TOKENS["IDENT"])
        self.eat(TOKENS["LPAREN"])
        args = []
        if self.current_token.type != TOKENS["RPAREN"]:
            args.append(self.parse_expr())
            while self.current_token.type == TOKENS["COMMA"]:
                self.eat(TOKENS["COMMA"])
                args.append(self.parse_expr())
        self.eat(TOKENS["RPAREN"])
        if self.current_token.type == TOKENS["SEMICOLON"]:
            self.eat(TOKENS["SEMICOLON"])
        return FuncCall(func_name, args)