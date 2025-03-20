#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <cctype>
#include <any>
#include "Token.cpp"

class AST {
public:
    std::vector<Token> tokens;
    std::map<std::string, std::any> variables;

    AST(const std::vector<Token>& tokens) : tokens(tokens) {}
};


class Variable {
public:
    std::string name;
    std::any value;

    Variable(const std::string& name, const std::any& value) : name(name), value(value) {}
};

class Function {
public:
    std::string name;
    std::vector<Token> parameters;
    std::vector<Token> body;
};

class IfStatement {
public:
    std::vector<Token> condition;
    std::vector<Token> body;
    std::vector<Token> elseIfBody;
    std::vector<Token> elseBody;
};

class WhileStatement {
public:
    std::vector<Token> condition;
    std::vector<Token> body;
};

class ForStatement {
public:
    std::vector<Token> initialization;
    std::vector<Token> condition;
    std::vector<Token> update;
    std::vector<Token> body;
};

class ReturnStatement {
public:
    std::vector<Token> value;
};




