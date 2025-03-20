#pragma once
#include <string>
#include <vector>
#include "../lexer/Token.h"

class Parser {
public:
    Parser(const std::string& path);
    std::vector<Token> parseFile();
    void printTokens();

private:
    std::string filePath;
    Lexer lexer;
    std::vector<Token> tokens;
}; 