from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _

from backend.apps.lexxer.generate.ply import lex

reserved_words = {
    'AND': 'AND_OP', # operator
    "BESTOW": 'BESTOW',
    "CHEST": 'CHEST',
    "CHOP": 'CHOP',
    "CHRONO": 'CHRONO',
    "DAY": 'DAY',
    "ECHO": 'ECHO',
    "FATE": 'FATE',
    "FUTURE": 'FUTURE',
    "GOLD": 'GOLD',
    "HEAD": 'HEAD',
    "HERMES": 'HERMES',
    "HYDRA": 'HYDRA',
    "IN": 'IN',
    "NONE": 'NONE',
    "NOT": 'NOT_OP', # operator
    "OFFER": 'OFFER',
    "OLYMPUS": 'OLYMPUS',
    "OR": 'OR_OP', # operator
    "PANDORA": 'PANDORA',
    "PAST": 'PAST',
    "PROPHECY": 'PROPHECY',
    "QUEST": 'QUEST',
    "RETRIAL": 'RETRIAL',
    "REWARD": 'REWARD',
    "SILVER": 'SILVER',
    "SKIP": 'SKIP',
    "SLAIN": 'SLAIN',
    "SONG": 'SONG',
    "STOP": 'STOP',
    "TRIAL": 'TRIAL',
    "VERDICT": 'VERDICT'
}


class LexicalValidationError(ValidationError):

    def __init__(self, message, code='lexical', params=None, line=0, char_line=0):
        super().__init__(message, code, params)
        self.line = line
        self.char_line = char_line


class MythLexer:
    tokens = [
        'NUM', #conflicts with DECIMAL, DOT, ID NO LIMIT YET
        'TEXT', # NO LIMIT YET
        'ID',
        'BOOL',
    ] +  list(reserved_words.values())
    tokens.extend(
        [ # groupings
            'OPCOLUMN',
            'CLCOLUMN',
            'OPPAR',
            'CLPAR',
            'OPBRACK',
            'CLBRACK',
            'OPCURL',
            'CLCURL',
          # terminators and such dots
            'COLON',
            'SEMICOLON',
            'COMMA',
            'DOT',
          # operators
            'PLUS_OP',
            'MINUS_OP',
            'PRODUCT_OP',
            'DIV_OP',
            'MOD_OP',
            'POW_OP',
          # relation
            'GT_OP',
            'LT_OP',
            'GTE_OP',
            'LTE_OP',
            'NE_OP',
            'EQ_OP',
          # assign
            'ASSIGN',
            'ADD_ASSIGN',
            'SUB_ASSIGN',
            'MUL_ASSIGN',
            'DIV_ASSIGN',
            'MOD_ASSIGN',
            'POW_ASSIGN',
        ]
    )


    t_ignore = ' \t'
    # t_ignore_COMMENT = r'\?\?.*'

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_COMMENT(self, t):
        r'\?\?.*'
        pass

    def t_OPCOLUMN(self, t):
        r'\|\<\|'
        t.type = 'OPCOLUMN'
        t.char_line = self.find_column(t)
        t.description = 'open-column'
        return t

    def t_CLCOLUMN(self, t):
        r'\|\>\|'
        t.type = 'CLCOLUMN'
        t.char_line = self.find_column(t)
        t.description = 'close-column'
        return t

    def t_OPPAR(self, t):
        r'\('
        t.type = 'OPPAR'
        t.char_line = self.find_column(t)
        t.description = 'open-parenthesis'
        return t

    def t_CLPAR(self, t):
        r'\)'
        t.type = 'CLPAR'
        t.char_line = self.find_column(t)
        t.description = 'close-parenthesis'
        return t

    def t_OPBRACK(self, t):
        r'\['
        t.type = 'OPBRACK'
        t.char_line = self.find_column(t)
        t.description = 'open-brack'
        return t

    def t_CLBRACK(self, t):
        r'\]'
        t.type = 'CLBRACK'
        t.char_line = self.find_column(t)
        t.description = 'close-brack'
        return t

    def t_OPCURL(self, t):
        r'\{'
        t.type = 'OPCURL'
        t.char_line = self.find_column(t)
        t.description = 'open-curl'
        return t

    def t_CLCURL(self, t):
        r'\}'
        t.type = 'CLCURL'
        t.char_line = self.find_column(t)
        t.description = 'close-curl'
        return t

    def t_COLON(self, t):
        r'\:'
        t.type = 'COLON'
        t.char_line = self.find_column(t)
        t.description = 'colon'
        return t

    def t_COMMA(self ,t):
        r'\,'
        t.type = 'COMMA'
        t.char_line = self.find_column(t)
        t.description = 'comma'
        return t

    def t_SEMICOLON(self, t):
        r'\;'
        t.type = 'SEMICOLON'
        t.char_line = self.find_column(t)
        t.description = 'semicolon'
        return t

    def t_DOT(self, t):
        r'\.'
        t.type = 'DOT'
        t.char_line = self.find_column(t)
        t.description = 'dot'
        return t

    def t_ADD_ASSIGN(self, t):
        r'\+\='
        t.type = 'ADD_ASSIGN'
        t.char_line = self.find_column(t)
        t.description = 'add-assign'
        return t

    def t_SUB_ASSIGN(self, t):
        r'\-\='
        t.type = 'SUB_ASSIGN'
        t.char_line = self.find_column(t)
        t.description = 'sub-assign'
        return  t

    def t_MUL_ASSIGN(self, t):
        r'\*\='
        t.type = 'MUL_ASSIGN'
        t.char_line = self.find_column(t)
        t.description = 'mul-assign'
        return t

    def t_DIV_ASSIGN(self, t):
        r'\/\='
        t.type = 'DIV_ASSIGN'
        t.char_line = self.find_column(t)
        t.description = 'div-assign'
        return t

    def t_POW_ASSIGN(self, t):
        r'\^\='
        t.type = 'POW_ASSIGN'
        t.char_line = self.find_column(t)
        t.description = 'pow-assign'
        return t

    def t_PLUS_OP(self, t):
        r'\+'
        t.type = 'PLUS_OP'
        t.char_line = self.find_column(t)
        t.description = 'plus-operator'
        return t

    def t_MINUS_OP(self, t):
        r'\-'
        t.type = 'MINUS_OP'
        t.char_line = self.find_column(t)
        t.description = 'minus-operator'
        return t

    def t_PRODUCT_OP(self, t):
        r'\*'
        t.type = 'PRODUCT_OP'
        t.char_line = self.find_column(t)
        t.description = 'product-operator'
        return t

    def t_DIV_OP(self, t):
        r'\/'
        t.type = 'DIV_OP'
        t.char_line = self.find_column(t)
        t.description = 'div-operator'
        return t

    def t_MOD_OP(self, t):
        r'\%'
        t.type = 'MOD_OP'
        t.char_line = self.find_column(t)
        t.description = 'mod-operator'
        return t

    def t_POW_OP(self, t):
        r'\^'
        t.type = 'POW_OP'
        t.char_line = self.find_column(t)
        t.description = 'pow-operator'
        return t

    def t_GTE_OP(self, t):
        r'\>\='
        t.type = 'GTE_OP'
        t.char_line = self.find_column(t)
        t.description = 'gte-operator'
        return t

    def t_LTE_OP(self, t):
        r'\<\='
        t.type = 'LTE_OP'
        t.char_line = self.find_column(t)
        t.description = 'lte-operator'
        return t

    def t_NE_OP(self, t):
        r'\!\='
        t.type = 'NE_OP'
        t.char_line = self.find_column(t)
        t.description ='ne-operator'
        return t

    def t_EQ_OP(self, t):
        r'\=\='
        t.type = 'EQ_OP'
        t.char_line = self.find_column(t)
        t.description = 'eq-operator'
        return t

    def t_GT_OP(self, t):
        r'\>'
        t.type = 'GT_OP'
        t.char_line = self.find_column(t)
        t.description = 'gt-operator'
        return t

    def t_LT_OP(self, t):
        r'\<'
        t.type = 'LT_OP'
        t.char_line = self.find_column(t)
        t.description = 'lt-operator'
        return t

    def t_ASSIGN(self, t):
        r'\='
        t.type = 'ASSIGN'
        t.char_line = self.find_column(t)
        t.description = 'assign'
        return t

    def t_NUM(self, t):
        r'(0|[1-9][0-9]{0,8})(\.[0-9]{1,5})?'
        t.type = 'NUM'
        t.char_line = self.find_column(t)
        t.description = 'num-literal'
        t.value = t.value
        # r'^0|[1-9][0-9]{0,8}\.?[\d]{0,4}'
        # ^(?=.\d{0,8}(|(\.\d{1,5}))$)(0$|[1-9][0-9]*)([.][\d]+)?
        return t

    def t_TEXT(self, t):
        r'\".*\"'
        t.type = 'TEXT'
        t.char_line = self.find_column(t)
        t.description = 'text-literal'
        return t

    def t_ID(self, t):
        r'[_a-zA-Z][a-zA-Z0-9]{0,31}'
        t.type = reserved_words.get(t.value, 'ID')
        t.char_line = self.find_column(t)
        if t.value in ['BLESSED', 'CURSED']:
            t.type = 'BOOL'
        if t.type == 'ID': t.description = 'identifer'
        else: t.description = 'reserved word'
        return t

    def t_error(self, t):
        char_line = self.find_column(t)

        self.append_error(
            f'Character not found {t.value[0]}',
                code='lexical', line=t.lexer.lineno, char_line=char_line)
        # print(f"Line {t.lexer.lineno} char_line {char_line} Illegal character {t.value[0]}")
        t.lexer.skip(1)

    def __init__(self, debug=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.build(debug, **kwargs)

    def find_column(self, token):
        line_start = self.data.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1

    def append_error(self, message=" ", code="lexical", line=0, char_line=0):

        # bugged not reading code
        self.ERROR_LIST.append(LexicalValidationError(_(message),
            code=code, line=line, char_line=char_line))

    def build(self, debug=False, **kwargs):
        self.lexer = lex.lex(debug=debug, module=self, **kwargs)

    def input(self, data="", run=False):
        # save data and clear at first
        self.data = data
        self.ERROR_LIST = []
        self.TOKEN_LIST = []
        if run: self.test()

    def test(self):
        self.lexer.input(self.data)
        while True:
             tok = self.lexer.token()
             if not tok:
                 break
             #print(tok)
             self.TOKEN_LIST.append(tok)


# mini class
def parse(string=""):
    mythLex = MythLexer()
    mythLex.input(string, run=True)
    if mythLex.ERROR_LIST: raise LexicalValidationError(mythLex.ERROR_LIST)
    return mythLex.TOKEN_LIST

