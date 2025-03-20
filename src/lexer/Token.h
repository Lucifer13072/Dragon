#pragma once

#include <string>
#include <vector>

enum class TokenType {
    NUMBER,
    STRING,
    ID,
    LPAREN,
    RPAREN,
    COMMA,
    SEMICOLON,
    PLUS,
    MINUS,
    MULTIPLY,
    DIVIDE,
    EQUAL,
    ARROW,
    NOT,
    AND,
    OR,
    GREATER,
    LESS,
    LBRACKET,
    RBRACKET,
    LBRACE,
    RBRACE,
    SPACE,
    TAB,
    NEWLINE,
    OUTPUT
};

struct Token {
    TokenType type;
    std::string value;
    int line;
    int column;

    Token(TokenType type, const std::string& value, int line, int column);
};

class Lexer {
public:
    Lexer(const std::string& inputStr);
    std::vector<Token> tokenize();

private:
    std::string input;
    size_t pos;
    int line;
    int column;
}; 