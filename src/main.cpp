#include "lexer/Token.h"
#include "parser/Parser.h"
#include "interpret/Interpretator.h"
#include <iostream>
#include <string>
#include <windows.h>

int main() {
    // Set console encoding for Windows
    setlocale(LC_ALL, "Russian");

    std::cout << "Program started" << std::endl;
    
    std::string filePath = "src/dragon/main.drg";
    std::cout << "File path: " << filePath << std::endl;
    
    try {
        // Create parser and parse file
        std::cout << "Creating parser..." << std::endl;
        Parser parser(filePath);
        std::cout << "Parsing file..." << std::endl;
        std::vector<Token> tokens = parser.parseFile();
        
        // Create interpreter and execute code
        std::cout << "Creating interpreter..." << std::endl;
        Interpretator interpreter(tokens);
        std::cout << "Interpreting code..." << std::endl;
        interpreter.interpret();
        
        // Print variable values
        std::cout << "\nVariable values:" << std::endl;
        for (const auto& [name, value] : interpreter.variables) {
            if (value.type() == typeid(int)) {
                std::cout << name << " = " << std::any_cast<int>(value) << std::endl;
            } else if (value.type() == typeid(std::string)) {
                std::cout << name << " = " << std::any_cast<std::string>(value) << std::endl;
            }
        }
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        std::cout << "Press Enter to exit..." << std::endl;
        std::cin.get();
        return 1;
    }

    std::cout << "Program finished" << std::endl;
    std::cout << "Press Enter to exit..." << std::endl;
    std::cin.get();
    return 0;
}