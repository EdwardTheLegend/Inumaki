from inu_lexer import TOKENS, KEYWORDS


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.ast = []

    def peek(self):
        if self.pos >= len(self.tokens):
            return None
        return self.tokens[self.pos]

    def peekn(self, n):
        if self.pos + n >= len(self.tokens):
            return None
        return self.tokens[self.pos + n]

    def eat(self, type):
        if type in TOKENS.keys():
            if peek_type := self.peek().type == type:
                self.pos += 1
                return self.tokens[self.pos - 1]
        elif type in KEYWORDS:
            if peek_type := self.peek().value == type:
                self.pos += 1
                return self.tokens[self.pos - 1]

        raise Exception(f"Expected {type}, got {peek_type}")

    def parse(self):
        while self.peek():
            self.ast.append(self.parse_statement())
        return self.ast

    def parse_statement(self):
        next = self.peek()

        if next.type != TOKENS["Keyword"]:
            raise Exception(f"Expected keyword, got {next.type}")

        match next.value:
            case "Tuna":
                return self.variable_stmt()
            case "Tuna_Mayo":
                return self.function_stmt()
            case "Return":
                return self.return_stmt()
            case "Mustard_Leaf":
                return self.conditional_stmt()
            case "Twist":
                return self.for_stmt()
            case "Plummet":
                return self.while_stmt()
