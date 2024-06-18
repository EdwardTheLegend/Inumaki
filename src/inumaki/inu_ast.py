class Set:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    __match_args__ = ("name", "value")


class Var:
    def __init__(self, name):
        self.name = name

    __match_args__ = ("name",)


class Function:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    __match_args__ = ("name", "params", "body")


class Return:
    def __init__(self, value):
        self.value = value

    __match_args__ = ("value",)


class Conditional:
    def __init__(self, condition, body, else_body):
        self.condition = condition
        self.body = body
        self.else_body = else_body

    __match_args__ = ("condition", "body", "else_body")


class For:
    def __init__(self, variable, condition, increment, body):
        self.variable = variable
        self.condition = condition
        self.increment = increment
        self.body = body

    __match_args__ = ("variable", "condition", "increment", "body")


class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    __match_args__ = ("condition", "body")


class Call:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    __match_args__ = ("name", "args")


class Get:
    def __init__(self, obj, prop):
        self.obj = obj
        self.prop = prop

    __match_args__ = ("obj", "prop")


class UnaryOp:
    def __init__(self, op, right):
        self.op = op
        self.right = right

    __match_args__ = ("op", "right")


class BinaryOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    __match_args__ = ("left", "op", "right")


class Literal:
    def __init__(self, value):
        self.value = value

    __match_args__ = ("value",)
