from inu_ast import BinaryOp, Call, Conditional, For, Function, Get, Literal, Return, UnaryOp, Var, While, Set


class Interpreter:
    class ReturnException(Exception):
        def __init__(self, value):
            self.value = value

    def __init__(self, ast, scope, cursed=0):
        self.ast = ast
        self.scope = scope
        self.cursed = cursed

    def run(self):
        for node in self.ast:
            self.execute(node)

        return self.scope

    def run_block(self, block, scope=None):
        if scope is None:
            scope = self.scope
        interpreter = Interpreter(block, scope, cursed=self.cursed)
        try:
            self.scope = interpreter.run()
        except self.ReturnException as e:
            self.cursed = interpreter.cursed
            raise self.ReturnException(e.value)

    def evaluate(self, node):
        match node:
            case Var(name, cursed):
                self.cursed += cursed
                return self.scope[name]
            case UnaryOp(op, right):
                if op == "Not":
                    return not self.evaluate(right)
                elif op == "-":
                    return -self.evaluate(right)
            case BinaryOp(left, op, right):
                left = self.evaluate(left)
                right = self.evaluate(right)

                match op.value:
                    case "+":
                        return left + right
                    case "-":
                        return left - right
                    case "*":
                        return left * right
                    case "/":
                        return left / right
                    case "==":
                        return left == right
                    case "!=":
                        return left != right
                    case ">":
                        return left > right
                    case "<":
                        return left < right
                    case ">=":
                        return left >= right
                    case "<=":
                        return left <= right
                    case "And":
                        return left and right
                    case "Or":
                        return left or right
                    case _:
                        raise Exception(f"Unknown binary operator {op}")
            case Literal(value, cursed):
                self.cursed += cursed
                return value
            case Call(name, args):
                func = self.evaluate(name)
                return func(*[self.evaluate(arg) for arg in args])
            case Get(obj, prop):
                obj = self.evaluate(obj)
                prop = self.evaluate(prop)
                return obj[prop]
            case _:
                raise Exception(f"Unknown node {node}")

    def execute(self, node):
        match node:
            case Set(name, value, cursed):
                self.cursed += cursed
                self.scope[name.value] = self.evaluate(value)
            case Function(name, params, body, cursed):
                self.cursed += cursed

                def function(*args):
                    try:
                        self.run_block(body, {**self.scope, **{param.value: arg for param, arg in zip(params, args)}})
                    except self.ReturnException as e:
                        return e.value

                self.scope[name.value] = function
            case Return(value, cursed):
                self.cursed += cursed
                raise self.ReturnException(self.evaluate(value))
            case Conditional(condition, body, else_body, cursed):
                self.cursed += cursed
                if self.evaluate(condition):
                    self.run_block(body)
                else:
                    self.run_block(else_body)
            case For(variable, condition, increment, body, cursed):
                self.cursed += cursed
                self.run_block([variable])
                while self.evaluate(condition):
                    self.run_block(body)
                    self.execute(increment)
            case While(condition, body, cursed):
                self.cursed += cursed
                while self.evaluate(condition):
                    self.run_block(body)
            case _:
                self.evaluate(node)
