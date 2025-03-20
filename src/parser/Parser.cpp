#include "Parser.h"
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include "../lexer/Token.h"

Parser::Parser(const std::string& path) : filePath(path), lexer("") {
    std::cout << "Parser created for file: " << path << std::endl;
}

std::vector<Token> Parser::parseFile() {
    std::cout << "Attempting to open file: " << filePath << std::endl;
    std::ifstream file(filePath);
    if (!file.is_open()) {
        std::cerr << "Error: Could not open file: " << filePath << std::endl;
        throw std::runtime_error("Could not open file: " + filePath);
    }

    std::string content;
    std::string line;
    while (std::getline(file, line)) {
        content += line + "\n";
    }
    file.close();

    std::cout << "File contents:" << std::endl;
    std::cout << content << std::endl;

    std::cout << "Creating lexer..." << std::endl;
    lexer = Lexer(content);
    
    std::cout << "Tokenizing..." << std::endl;
    tokens = lexer.tokenize();
    
    std::cout << "Tokens:" << std::endl;
    printTokens();
    
    return tokens;
}

void Parser::printTokens() {
    for (const auto& token : tokens) {
        std::cout << "Type: " << static_cast<int>(token.type) 
                  << ", Value: " << token.value 
                  << ", Line: " << token.line 
                  << ", Column: " << token.column << std::endl;
    }
}
