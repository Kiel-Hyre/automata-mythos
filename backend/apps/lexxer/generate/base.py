

# Base
class LexToken:

    def __init__(self, name="", value="", description="", line=0, char_line=0):
        self.name = name
        self.value = value
        self.description = description
        self.line = line
        self.char_line = char_line + 1

    def val_to_dict(self):
        return {
            'name': self.name,
            'value': self.value,
            'description': self.description,
            'line': self.line,
            'char_line': self.char_line
        }

    @property
    def syntax_token(self):
        return self.__class__.__name__

    def __repr__(self):
        return f"""
        title: {self.name} value: {self.value} line: {self.line} desc: {self.description} charline: {self.char_line}"""

    def __str__(self):
        return self.value


class IntegerLiteralToken:
    name = 'IntLit'
    # description = 'integer-literal'

class DecimalLiteralToken:
    name = 'DecLit'
    # description = 'decimal-literal'

class TextLiteralToken:
    name = 'TextLit'
    # description = 'text-literal'

class IdentifierToken:
    name = 'Id'
    # description = 'identifier'