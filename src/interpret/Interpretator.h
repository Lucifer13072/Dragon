#pragma once
#include <vector>
#include <map>
#include <any>
#include "../lexer/Token.h"

class Interpretator {
public:
    Interpretator(const std::vector<Token>& inputTokens);
    void interpret();
    std::map<std::string, std::any> variables;

private:
    std::vector<Token> tokens;
    std::any evaluateExpression(const std::vector<Token>& expression);
}; 