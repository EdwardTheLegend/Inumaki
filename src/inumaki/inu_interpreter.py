from inu_ast import (
    BinaryOp,
    Call,
    Conditional,
    For,
    Function,
    Get,
    Literal,
    Return,
    UnaryOp,
    Var,
    While,
    Set,
    CoughSyrup,
)
from inu_exceptions import (
    CursedSpeechOverloadError, 
    create_undefined_variable_error, 
    create_division_by_zero_error,
    create_invalid_operator_error,
    create_function_call_error,
    InumakiRuntimeError
)


class Interpreter:
    CursedThreshold = 100

    class ReturnException(Exception):
        def __init__(self, value):
            self.value = value

    def __init__(self, ast, scope, cursed):
        self.ast = ast
        self.scope = scope
        self.cursed = cursed

    def run(self):
        for node in self.ast:
            self.execute(node)
            # print(f"Current cursed count: {self.cursed}")  # Debug statement
            if self.cursed > Interpreter.CursedThreshold:
                raise CursedSpeechOverloadError(self.cursed, Interpreter.CursedThreshold)
        return self.scope

    def run_block(self, block, scope=None):
        if scope is None:
            scope = self.scope
        interpreter = Interpreter(block, scope, cursed=self.cursed)
        try:
            self.scope = interpreter.run()
        except self.ReturnException as e:
            raise self.ReturnException(e.value)
        finally:
            self.cursed = interpreter.cursed
            # print(f"Cursed count after block: {self.cursed}")  # Debug statement

    def evaluate(self, node):
        match node:
            case Var(name, cursed):
                self.cursed += cursed
                # print(f"Evaluating Var: {name}, cursed: {self.cursed}")  # Debug statement
                if name not in self.scope:
                    raise create_undefined_variable_error(name)
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
                        if right == 0:
                            raise create_division_by_zero_error()
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
                    case "%":
                        return left % right
                    case "And":
                        return left and right
                    case "Or":
                        return left or right
                    case _:
                        raise create_invalid_operator_error(op.value)
            case Literal(value, cursed):
                self.cursed += cursed
                # print(f"Evaluating Literal: {value}, cursed: {self.cursed}")  # Debug statement
                return value
            case Call(name, args):
                try:
                    func = self.evaluate(name)
                    return func(*[self.evaluate(arg) for arg in args])
                except Exception as e:
                    func_name = name.name if hasattr(name, 'name') else str(name)
                    raise create_function_call_error(func_name, str(e))
            case Get(obj, prop):
                try:
                    obj = self.evaluate(obj)
                    prop = self.evaluate(prop)
                    return obj[prop]
                except (KeyError, IndexError, TypeError) as e:
                    raise InumakiRuntimeError(
                        message=f"Cannot access property/index: {str(e)}",
                        suggestion="Check that the object exists and the property/index is valid"
                    )
            case _:
                raise InumakiRuntimeError(
                    message=f"Unknown expression node: {type(node).__name__}",
                    suggestion="This may be an internal interpreter error"
                )

    def execute(self, node):
        match node:
            case Set(name, value, cursed):
                self.cursed += cursed
                # print(f"Executing Set: {name}, cursed: {self.cursed}")  # Debug statement
                self.scope[name.value] = self.evaluate(value)
            case Function(name, params, body, cursed):
                self.cursed += cursed
                # print(f"Executing Function: {name}, cursed: {self.cursed}")  # Debug statement

                def function(*args):
                    try:
                        self.run_block(body, {**self.scope, **{param.value: arg for param, arg in zip(params, args)}})
                    except self.ReturnException as e:
                        return e.value
                    finally:
                        self.cursed += self.count_cursed_in_body(body)
                        # print(f"Cursed count after function call: {self.cursed}")  # Debug statement

                self.scope[name.value] = function
            case Return(value, cursed):
                self.cursed += cursed
                # print(f"Executing Return, cursed: {self.cursed}")  # Debug statement
                raise self.ReturnException(self.evaluate(value))
            case Conditional(condition, body, else_body, cursed):
                self.cursed += cursed
                # print(f"Executing Conditional, cursed: {self.cursed}")  # Debug statement
                if self.evaluate(condition):
                    self.run_block(body)
                else:
                    self.run_block(else_body)
            case For(variable, condition, increment, body, cursed):
                self.cursed += cursed
                # print(f"Executing For, cursed: {self.cursed}")  # Debug statement
                self.run_block([variable])
                while self.evaluate(condition):
                    self.run_block(body)
                    self.execute(increment)
            case While(condition, body, cursed):
                self.cursed += cursed
                # print(f"Executing While, cursed: {self.cursed}")  # Debug statement
                while self.evaluate(condition):
                    self.run_block(body)
            case CoughSyrup():
                self.cursed = 0
                # print(f"Executing CoughSyrup, cursed reset to: {self.cursed}")  # Debug statement
            case _:
                self.evaluate(node)

    def count_cursed_in_body(self, body):
        cursed_count = 0
        for node in body:
            if hasattr(node, "cursed"):
                cursed_count += node.cursed
        # print(f"Counted cursed in body: {cursed_count}")  # Debug statement
        return cursed_count
