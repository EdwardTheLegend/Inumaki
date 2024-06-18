from inu_ast import BinaryOp, Call, Conditional, For, Function, Get, Literal, Return, UnaryOp, Var, While, Set


class Interpreter:
    class ReturnException(Exception):
        def __init__(self, value):
            self.value = value

    def __init__(self, ast, scope):
        self.ast = ast
        self.scope = scope
        self.cursed = 0

    def run(self):
        for node in self.ast:
            self.execute(node)

        return self.scope

    def run_block(self, block, scope=None):
        if scope is None:
            scope = self.scope
        interpreter = Interpreter(block, scope)
        self.scope = interpreter.run()

    def evaluate(self, node):
        match node:
            case Var(name):
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
            case Literal(value):
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
            case Set(name, value):
                self.scope[name.value] = self.evaluate(value)
            case Function(name, params, body):

                def function(*args):
                    try:
                        self.run_block(body, {**self.scope, **{param.value: arg for param, arg in zip(params, args)}})
                    except self.ReturnException as e:
                        return e.value

                self.scope[name.value] = function
            case Return(value):
                raise self.ReturnException(self.evaluate(value))
            case Conditional(condition, body, else_body):
                if self.evaluate(condition):
                    self.run_block(body)
                else:
                    self.run_block(else_body)
            case For(variable, condition, increment, body):
                self.run_block([variable])
                while self.evaluate(condition):
                    self.run_block(body)
                    self.execute(increment)
            case While(condition, body):
                while self.evaluate(condition):
                    self.run_block(body)
            case _:
                self.evaluate(node)
