from parser import Parser
from interpret import Interpreter
from tokens import tokenize
def main():

    filename = "code-test/main.drg"
    with open(filename, 'r') as f:
        source = f.read()
    tokens = tokenize(source)
    parser = Parser(tokens)
    statements = parser.parse()
    interpreter = Interpreter(statements)
    interpreter.run()

if __name__ == '__main__':
    main()
