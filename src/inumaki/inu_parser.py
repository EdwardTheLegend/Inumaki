from inu_lexer import TOKENS, KEYWORDS
from inu_ast import Var, Function, Return, Conditional, For, While, Call, UnaryOp, BinaryOp, Literal, Get


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

    def term(self):
        if self.peek().type == TOKENS["Identifier"]:
            name = self.eat("Identifier")
            while self.peek().type in [TOKENS["Dot"], TOKENS["LeftParen"]]:
                if self.peek().type == TOKENS["Dot"]:
                    self.eat("Dot")
                    name = Get(name, self.eat("Identifier"))
                else:
                    self.eat("LeftParen")
                    args = []
                    while self.peek().type != TOKENS["RightParen"]:
                        args.append(self.expression())
                        if self.peek().type == TOKENS["Comma"]:
                            self.eat("Comma")
                    self.eat("RightParen")
                    name = Call(name, args)

            return name

        elif self.peek().type in [TOKENS["Number"], TOKENS["Boolean"], TOKENS["String"]]:
            return Literal(self.eat(self.peek().type).value)
        elif self.peek().type == TOKENS["LeftParen"]:
            self.eat("LeftParen")
            expr = self.expression()
            self.eat("RightParen")
            return expr
        elif self.peek().type == TOKENS["Minus"]:
            self.eat("Minus")
            return UnaryOp("-", self.term())
        elif self.peek().type == TOKENS["Not"]:
            self.eat("Not")
            return UnaryOp("!", self.term())

    def expression(self):
        left = self.term()

        while self.peek().type in [
            TOKENS["Plus"],
            TOKENS["Minus"],
            TOKENS["Asterisk"],
            TOKENS["Slash"],
            TOKENS["Equiv"],
            TOKENS["NotEquiv"],
            TOKENS["Lt"],
            TOKENS["Gt"],
            TOKENS["Lte"],
            TOKENS["Gte"],
            TOKENS["And"],
            TOKENS["Or"],
        ]:
            op = self.eat(self.peek().type)
            right = self.term()
            left = BinaryOp(left, op, right)

        return left

    def parse(self):
        while self.peek():
            self.ast.append(self.parse_statement())
        return self.ast

    def parse_statement(self):
        next = self.peek()

        if next.type == TOKENS["Keyword"]:

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
        else:
            return self.expression()

    def variable_stmt(self):
        self.eat("Tuna")
        name = self.eat("Identifier")
        self.eat("Tuna")
        value = self.expression()

        return Var(name, value)

    def function_stmt(self):
        self.eat("Tuna_Mayo")
        name = self.eat("Identifier")
        self.eat("Tuna")
        params = []
        while self.peek().type != TOKENS["Tuna"]:
            params.append(self.eat("Identifier"))
        self.eat("Tuna")

        self.eat("LeftBrace")
        body = []
        while self.peek().type != TOKENS["RightBrace"]:
            body.append(self.parse_statement())
        self.eat("RightBrace")

        return Function(name, params, body)

    def return_stmt(self):
        self.eat("Return")
        value = self.expression()

        return Return(value)

    def conditional_stmt(self):
        self.eat("Mustard_Leaf")
        self.eat("Tuna")
        condition = self.expression()
        self.eat("Tuna")
        self.eat("LeftBrace")
        body = []
        while self.peek().type != TOKENS["RightBrace"]:
            body.append(self.parse_statement())
        self.eat("RightBrace")
        else_body = None
        if self.peek().value == "Explode":
            self.eat("Explode")
            self.eat("LeftBrace")
            else_body = []
            while self.peek().type != TOKENS["RightBrace"]:
                else_body.append(self.parse_statement())
            self.eat("RightBrace")

        return Conditional(condition, body, else_body)

    def for_stmt(self):
        self.eat("Twist")
        self.eat("Tuna")
        var = self.parse_statement()
        if not isinstance(var, Var):
            raise Exception("Expected variable declaration in for loop")
        self.eat("Tuna")
        condition = self.expression()
        self.eat("Tuna")
        increment = self.parse_statement()
        self.eat("Tuna")

        self.eat("LeftBrace")
        body = []
        while self.peek().type != TOKENS["RightBrace"]:
            body.append(self.parse_statement())
        self.eat("RightBrace")

        return For(var, condition, increment, body)

    def while_stmt(self):
        self.eat("Plummet")
        self.eat("Tuna")
        condition = self.expression()
        self.eat("Tuna")
        self.eat("LeftBrace")
        body = []
        while self.peek().type != TOKENS["RightBrace"]:
            body.append(self.parse_statement())
        self.eat("RightBrace")

        return While(condition, body)
