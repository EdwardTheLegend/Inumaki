import argparse

from .interpreter import Interpreter
from .lexer import Lexer
from .parser import Parser

parser = argparse.ArgumentParser(prog="inumaki", description="Inumkai programming language")
parser.add_argument("file", type=str, help="Inumaki source code file", nargs="?", default=None)

args = parser.parse_args()

if args.file:
    with open(args.file, "r") as file:
        text = file.read()

    lexer = Lexer(text)
    lexer.scan_tokens()

    parser = Parser(lexer.tokens)
    parser.parse()

    interpreter = Interpreter(parser.ast)
    interpreter.interpret()
else:
    while True:
        try:
            text = input("inumaki> ")
        except (EOFError, KeyboardInterrupt):
            break

        lexer = Lexer(text)
        lexer.scan_tokens()

        parser = Parser(lexer.tokens)
        parser.parse()

        interpreter = Interpreter(parser.ast)
        interpreter.interpret()
