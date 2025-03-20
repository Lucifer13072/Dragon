#include "Token.h"
#include <iostream>
#include <string>
#include <vector>
#include <cctype>

Token::Token(TokenType type, const std::string& tokenValue, int line, int column)
    : type(type), value(tokenValue), line(line), column(column) {}

Lexer::Lexer(const std::string& inputStr) : input(inputStr), pos(0), line(1), column(1) {}

std::vector<Token> Lexer::tokenize() {
    std::vector<Token> tokens;

    while (pos < input.size()) {
        char current = input[pos];

        if (std::isspace(current)) {
            if (current == '\n') {
                line++;
                column = 1;
            } else {
                column++;
            }
            pos++;
            continue;
        }

        if (std::isdigit(current)) {
            std::string number;
            while (std::isdigit(current)) {
                number += current;
                pos++;
                current = input[pos];
            }

            tokens.push_back(Token(TokenType::NUMBER, number, line, column));
            column += static_cast<int>(number.size());
            continue;
        }   

        if (current == '"') {
            std::string str;
            pos++; // Skip opening quote
            column++;
            
            while (pos < input.size() && input[pos] != '"') {
                str += input[pos];
                pos++;
                column++;
            }
            
            if (pos < input.size()) {
                pos++; // Skip closing quote
                column++;
            }
            
            std::cout << "Found string literal in lexer: " << str << std::endl;
            std::cout << "Creating STRING token with value: " << str << std::endl;
            tokens.push_back(Token(TokenType::STRING, str, line, column));
            continue;
        }

        if (current == '(') {
            tokens.push_back(Token(TokenType::LPAREN, "(", line, column));
            pos++;
            column++;
            continue;
        }
        
        if (current == ')') {
            tokens.push_back(Token(TokenType::RPAREN, ")", line, column));
            pos++;
            column++;
            continue;
        }

        if (current == ',') {
            tokens.push_back(Token(TokenType::COMMA, ",", line, column));
            pos++;
            column++;
            continue;
        }   

        if (current == ';') {
            tokens.push_back(Token(TokenType::SEMICOLON, ";", line, column));
            pos++;
            column++;
            continue;
        }

        if (current == '+') {
            tokens.push_back(Token(TokenType::PLUS, "+", line, column));
            pos++;
            column++;
            continue;
        }

        if (current == '-') {   
            tokens.push_back(Token(TokenType::MINUS, "-", line, column));
            pos++;
            column++;
            continue;
        }

        if (current == '*') {
            tokens.push_back(Token(TokenType::MULTIPLY, "*", line, column));
            pos++;
            column++;
            continue;
        }

        if (current == '/') {
            tokens.push_back(Token(TokenType::DIVIDE, "/", line, column));
            pos++;
            column++;
            continue;
        }

        if (current == '=') {
            if (pos + 1 < input.size() && input[pos + 1] == '>') {
                tokens.push_back(Token(TokenType::ARROW, "=>", line, column));
                pos += 2;
                column += 2;
                continue;
            }
            tokens.push_back(Token(TokenType::EQUAL, "=", line, column));
            pos++;
            column++;
            continue;
        }       

        if (current == '!') {
            tokens.push_back(Token(TokenType::NOT, "!", line, column));
            pos++;
            column++;
            continue;
        }
        
        if (current == '&') {
            tokens.push_back(Token(TokenType::AND, "&", line, column));
            pos++;
            column++;
            continue;
        }

        if (current == '|') {
            tokens.push_back(Token(TokenType::OR, "|", line, column));
            pos++;
            column++;
            continue;
        }

        if (current == '>') {
            tokens.push_back(Token(TokenType::GREATER, ">", line, column));
            pos++;
            column++;
            continue;
        }

        if (current == '<') {
            tokens.push_back(Token(TokenType::LESS, "<", line, column));
            pos++;
            column++;
            continue;
        }
        
        if (current == ']') {
            tokens.push_back(Token(TokenType::RBRACKET, "]", line, column));
            pos++;
            column++;
            continue;
        }
        
        if (current == '[') {
            tokens.push_back(Token(TokenType::LBRACKET, "[", line, column));
            pos++;
            column++;
            continue;
        }   

        if (current == '}') {
            tokens.push_back(Token(TokenType::RBRACE, "}", line, column));
            pos++;
            column++;
            continue;
        }

        if (current == '{') {
            tokens.push_back(Token(TokenType::LBRACE, "{", line, column));
            pos++;
            column++;
            continue;
        }

        // Обработка функции output
        if (current == 'o' && pos + 5 < input.size() && 
            input[pos + 1] == 'u' && input[pos + 2] == 't' && 
            input[pos + 3] == 'p' && input[pos + 4] == 'u' && 
            input[pos + 5] == 't') {
            tokens.push_back(Token(TokenType::OUTPUT, "output", line, column));
            pos += 6;
            column += 6;
            continue;
        }

        // Обработка идентификаторов
        if (std::isalpha(current) || current == '_') {
            std::string identifier;
            while (pos < input.size() && (std::isalnum(current) || current == '_')) {
                identifier += current;
                pos++;
                column++;
                current = input[pos];
            }
            tokens.push_back(Token(TokenType::ID, identifier, line, column));
            continue;
        }
        
        pos++;
        column++;
    }
    return tokens;
}

            
            

            
        
            

                
            
            

