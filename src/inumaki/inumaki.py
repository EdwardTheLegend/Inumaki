import argparse
import sys

from inu_interpreter import Interpreter
from inu_lexer import Lexer
from inu_parser import Parser
from inu_stdlib import inu_stdlib
from inu_exceptions import InumakiException

parser = argparse.ArgumentParser(prog="inumaki", description="Inumkai programming language")
parser.add_argument("file", type=str, help="Inumaki source code file", nargs="?", default=None)

args = parser.parse_args()


def run(text, filename=None):
    try:
        lexer = Lexer(text)
        lexer.scan_tokens()

        parser = Parser(lexer.tokens)
        parser.parse()

        interpreter = Interpreter(parser.ast, scope=inu_stdlib, cursed=0)
        interpreter.run()
    except InumakiException as e:
        # Print the enhanced error message
        if filename:
            print(f"Error in {filename}:", file=sys.stderr)
        print(str(e), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        # Handle any unexpected errors
        if filename:
            print(f"Unexpected error in {filename}: {e}", file=sys.stderr)
        else:
            print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if args.file:
    with open(args.file, "r") as file:
        text = file.read()

    run(text, args.file)
else:
    print("Inumaki Interactive Shell")
    print("Enter Inumaki code (Ctrl+C or Ctrl+D to exit)")
    while True:
        try:
            text = input("inumaki> ")
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if text.strip():  # Only run if there's actual content
            try:
                run(text)
            except SystemExit:
                pass  # Error already handled and printed
