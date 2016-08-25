import string


class CodeGenerator:
    def __init__(self):
        pass

    def __del__(self):
        pass

    def begin(self, tab="    "):
        self.code = []
        self.tab = tab
        self.level = 0

    def getCode(self):
        return string.join(self.code, "")

    def write(self, string, withIndent = True):
        self.code.append(withIndent * (self.tab * self.level) + string)

    def indent(self):
        self.level = self.level + 1

    def dedent(self):
        if self.level == 0:
            raise SyntaxError, "internal error in code generator"
        self.level = self.level - 1




# TEST CODE.
'''
c = CodeGenerator()

c.begin()

c.write("for i in range(1000):\n")
c.indent()
c.write("print 'code generation is trivial'")
c.dedent()

print(c.getCode())
'''


