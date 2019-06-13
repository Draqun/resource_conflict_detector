class Function:
    def __init__(self, function_declaration_src):
        self.declaration = function_declaration_src
        self.body = self.declaration
        temp_split = self.declaration.split("(")
        self.name = temp_split[0].split()[-1].strip()
        self.type = temp_split[0].replace(self.name, '').strip()

    def feed(self, line):
        self.body += line

    def __repr__(self):
        return 'Function<'+', '.join("%s: %s" % item for item in vars(self).items())+'>'
