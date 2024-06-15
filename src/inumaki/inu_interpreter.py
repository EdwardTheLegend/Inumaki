class Interpreter:
    def __init__(self, ast, scope):
        self.ast = ast
        self.scope = scope

    def run(self):
        for node in self.ast:
            self.execute(node)
    
    def execute(self, node):
        pass