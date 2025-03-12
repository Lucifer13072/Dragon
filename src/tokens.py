# Константа с определениями токенов
import sys

# Константа с определениями токенов
TOKENS = {
    "NUMBER": "NUMBER",
    "STRING": "STRING",
    "IDENT": "IDENT",
    "ASSIGN": "ASSIGN",
    "ARROW": "ARROW",
    "PLUS": "PLUS",
    "MINUS": "MINUS",
    "MUL": "MUL",
    "DIV": "DIV",
    "LPAREN": "LPAREN",
    "RPAREN": "RPAREN",
    "LBRACE": "LBRACE",
    "RBRACE": "RBRACE",
    "SEMICOLON": "SEMICOLON",
    "COMMA": "COMMA",
    "EQ": "EQ",
    "NEQ": "NEQ",
    "GT": "GT",
    "LT": "LT",
    "GTE": "GTE",
    "LTE": "LTE",
    "AND": "AND",
    "OR": "OR",
    "NOT": "NOT",
    "FLOAT": "FLOAT",
    "BOOL": "BOOL"
}

# Класс для представления токена
class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

# Функция токенизации
def tokenize(source):
    tokens = []
    i = 0
    while i < len(source):
        c = source[i]
        if c.isspace():
            i += 1
            continue
        # Строковые литералы
        if c == '"':
            i += 1  # пропускаем открывающую кавычку
            str_val = ""
            while i < len(source) and source[i] != '"':
                str_val += source[i]
                i += 1
            if i >= len(source) or source[i] != '"':
                raise Exception("Не найдено закрывающее \" для строкового литерала")
            i += 1  # пропускаем закрывающую кавычку
            tokens.append(Token(TOKENS["STRING"], str_val))
            continue
        # Числа
        if c.isdigit() or (c == '.' and i+1 < len(source) and source[i+1].isdigit()):
            num = c
            i += 1
            has_dot = c == '.'
            while i < len(source) and (source[i].isdigit() or (source[i] == '.' and not has_dot)):
                if source[i] == '.':
                    has_dot = True
                num += source[i]
                i += 1
            if has_dot:
                tokens.append(Token(TOKENS["FLOAT"], float(num)))
            else:
                tokens.append(Token(TOKENS["NUMBER"], int(num)))
            continue
        
        # Булевы значения
        if c in ('t', 'f') and source[i:i+4] in ('true', 'false'):
            value = source[i:i+4] == 'true'
            tokens.append(Token(TOKENS["BOOL"], value))
            i += 4 if value else 5
            continue
        # Идентификаторы (также зарезервированные слова, например if, else)
        if c.isalpha() or c == '_':
            ident = c
            i += 1
            while i < len(source) and (source[i].isalnum() or source[i] == '_'):
                ident += source[i]
                i += 1
            tokens.append(Token(TOKENS["IDENT"], ident))
            continue
        # Фигурные скобки
        if c == '{':
            tokens.append(Token(TOKENS["LBRACE"], "{"))
            i += 1
            continue
        if c == '}':
            tokens.append(Token(TOKENS["RBRACE"], "}"))
            i += 1
            continue
        # Скобки круглые
        if c == '(':
            tokens.append(Token(TOKENS["LPAREN"], "("))
            i += 1
            continue
        if c == ')':
            tokens.append(Token(TOKENS["RPAREN"], ")"))
            i += 1
            continue
        # Точка с запятой
        if c == ';':
            tokens.append(Token(TOKENS["SEMICOLON"], ";"))
            i += 1
            continue
        # Запятая
        if c == ',':
            tokens.append(Token(TOKENS["COMMA"], ","))
            i += 1
            continue
        # Операторы, начинающиеся с '='
        if c == '=':
            if i+1 < len(source) and source[i+1] == '>':
                tokens.append(Token(TOKENS["ARROW"], "=>"))
                i += 2
            elif i+1 < len(source) and source[i+1] == '=':
                tokens.append(Token(TOKENS["EQ"], "=="))
                i += 2
            else:
                tokens.append(Token(TOKENS["ASSIGN"], "="))
                i += 1
            continue
        # Оператор '!'
        if c == '!':
            if i+1 < len(source) and source[i+1] == '=':
                tokens.append(Token(TOKENS["NEQ"], "!="))
                i += 2
            else:
                tokens.append(Token(TOKENS["NOT"], "!"))
                i += 1
            continue
        # Арифметические операторы
        if c == '+':
            tokens.append(Token(TOKENS["PLUS"], "+"))
            i += 1
            continue
        if c == '-':
            tokens.append(Token(TOKENS["MINUS"], "-"))
            i += 1
            continue
        if c == '*':
            tokens.append(Token(TOKENS["MUL"], "*"))
            i += 1
            continue
        if c == '/':
            tokens.append(Token(TOKENS["DIV"], "/"))
            i += 1
            continue
        # Операторы сравнения '>' и '<'
        if c == '>':
            if i+1 < len(source) and source[i+1] == '=':
                tokens.append(Token(TOKENS["GTE"], ">="))
                i += 2
            else:
                tokens.append(Token(TOKENS["GT"], ">"))
                i += 1
            continue
        if c == '<':
            if i+1 < len(source) and source[i+1] == '=':
                tokens.append(Token(TOKENS["LTE"], "<="))
                i += 2
            else:
                tokens.append(Token(TOKENS["LT"], "<"))
                i += 1
            continue
        # Логические операторы && и ||
        if c == '&':
            if i+1 < len(source) and source[i+1] == '&':
                tokens.append(Token(TOKENS["AND"], "&&"))
                i += 2
                continue
            else:
                raise Exception(f"Неизвестный символ: {c}")
        if c == '|':
            if i+1 < len(source) and source[i+1] == '|':
                tokens.append(Token(TOKENS["OR"], "||"))
                i += 2
                continue
            else:
                raise Exception(f"Неизвестный символ: {c}")
        raise Exception(f"Неизвестный символ: {c}")
    tokens.append(Token("EOF", None))
    return tokens
