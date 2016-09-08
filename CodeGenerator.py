import string


class CodeGenerator:
    def __init__(self, tab="    "):
        self.code = []
        self.tab = tab
        self.level = 0

    def __del__(self):
        pass

    def get_code(self):
        return string.join(self.code, "")

    def write(self, code_text, indent=True):
        self.code.append(indent * (self.tab * self.level) + code_text)

    def indent(self):
        self.level += 1

    def dedent(self):
        if self.level == 0:
            raise SyntaxError, 'internal error in code generator'
        self.level -= 1


# TEST CODE.
'''
c = CodeGenerator()

c.write("for i in range(1000):\n")
c.indent()
c.write("print 'code generation is trivial'")
c.dedent()

print(c.getCode())
'''
