#include "Interpretator.h"
#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <cctype>
#include <any>
#include "../lexer/Token.h"

Interpretator::Interpretator(const std::vector<Token>& inputTokens) : tokens(inputTokens) {}

std::any Interpretator::evaluateExpression(const std::vector<Token>& expression) {
    if (expression.empty()) return nullptr;
    
    // If expression consists of a single token
    if (expression.size() == 1) {
        const Token& token = expression[0];
        std::cout << "Evaluating single token: Type=" << static_cast<int>(token.type) 
                  << ", Value=" << token.value << std::endl;
        
        switch (token.type) {
            case TokenType::NUMBER:
                return std::stoi(token.value);
            case TokenType::STRING:
                std::cout << "Found string literal: " << token.value << std::endl;
                std::cout << "Returning string value: " << token.value << std::endl;
                return std::string(token.value);
            case TokenType::ID:
                if (variables.find(token.value) != variables.end()) {
                    std::cout << "Found variable " << token.value << " with value: ";
                    if (variables[token.value].type() == typeid(int)) {
                        std::cout << std::any_cast<int>(variables[token.value]) << std::endl;
                    } else if (variables[token.value].type() == typeid(std::string)) {
                        std::cout << std::any_cast<std::string>(variables[token.value]) << std::endl;
                    }
                    return variables[token.value];
                }
                throw std::runtime_error("Variable " + token.value + " is not defined");
            default:
                throw std::runtime_error("Unsupported token type");
        }
    }

    // Handle arithmetic operations
    if (expression.size() == 3) {
        const Token& left = expression[0];
        const Token& op = expression[1];
        const Token& right = expression[2];

        std::cout << "Evaluating operation: " << left.value << " " << op.value << " " << right.value << std::endl;
        
        std::any leftVal = evaluateExpression({left});
        std::any rightVal = evaluateExpression({right});

        if (op.type == TokenType::PLUS) {
            if (leftVal.type() == typeid(int) && rightVal.type() == typeid(int)) {
                return std::any_cast<int>(leftVal) + std::any_cast<int>(rightVal);
            }
            if (leftVal.type() == typeid(std::string) && rightVal.type() == typeid(std::string)) {
                return std::any_cast<std::string>(leftVal) + std::any_cast<std::string>(rightVal);
            }
            throw std::runtime_error("Operation + supports only numbers or strings");
        }
        // Add other operators as needed
    }

    throw std::runtime_error("Unsupported expression");
}

void Interpretator::interpret() {
    for (size_t i = 0; i < tokens.size(); i++) {
        const Token& token = tokens[i];
        
        if (token.type == TokenType::OUTPUT) {
            // Check for opening parenthesis
            if (i + 1 < tokens.size() && tokens[i + 1].type == TokenType::LPAREN) {
                i += 2; // Skip output and (
                
                // Collect expression until closing parenthesis
                std::vector<Token> expr;
                while (i < tokens.size() && tokens[i].type != TokenType::RPAREN) {
                    expr.push_back(tokens[i]);
                    i++;
                }
                
                // Check for closing parenthesis and semicolon
                if (i < tokens.size() && tokens[i].type == TokenType::RPAREN) {
                    i++; // Skip )
                    if (i < tokens.size() && tokens[i].type == TokenType::SEMICOLON) {
                        i++; // Skip ;
                        
                        // Evaluate and print value
                        std::any value = evaluateExpression(expr);
                        if (value.type() == typeid(int)) {
                            std::cout << std::any_cast<int>(value) << std::endl;
                        } else if (value.type() == typeid(std::string)) {
                            std::cout << std::any_cast<std::string>(value) << std::endl;
                        }
                        continue;
                    }
                }
                throw std::runtime_error("Syntax error in output call");
            }
        }
        
        if (token.type == TokenType::ID) {
            // Check next token
            if (i + 1 < tokens.size()) {
                const Token& nextToken = tokens[i + 1];
                
                if (nextToken.type == TokenType::EQUAL) {
                    // Regular assignment
                    std::vector<Token> expr;
                    i += 2; // Skip ID and =
                    while (i < tokens.size() && tokens[i].type != TokenType::SEMICOLON) {
                        expr.push_back(tokens[i]);
                        i++;
                    }
                    std::cout << "Assigning to variable: " << token.value << std::endl;
                    std::cout << "Expression tokens:" << std::endl;
                    for (const auto& t : expr) {
                        std::cout << "  Type=" << static_cast<int>(t.type) << ", Value=" << t.value << std::endl;
                    }
                    std::cout << "Evaluating expression for assignment..." << std::endl;
                    std::any value = evaluateExpression(expr);
                    std::cout << "Expression evaluated successfully" << std::endl;
                    std::cout << "Value type: " << value.type().name() << std::endl;
                    if (value.type() == typeid(std::string)) {
                        std::cout << "String value: " << std::any_cast<std::string>(value) << std::endl;
                    }
                    variables[token.value] = value;
                    std::cout << "Variable " << token.value << " assigned successfully with type: ";
                    if (value.type() == typeid(int)) {
                        std::cout << "int" << std::endl;
                    } else if (value.type() == typeid(std::string)) {
                        std::cout << "string" << std::endl;
                    }
                }
                else if (nextToken.type == TokenType::ARROW) {
                    // Assignment with =>
                    std::vector<Token> expr;
                    i += 2; // Skip ID and =>
                    while (i < tokens.size() && tokens[i].type != TokenType::SEMICOLON) {
                        expr.push_back(tokens[i]);
                        i++;
                    }
                    variables[token.value] = evaluateExpression(expr);
                }
            }
        }
    }
}  




