from .base import *

ASSIGN_OP = 'assign-op'
ARITH_OP = 'arithmetic-op'
UNARY_RELATIONAL_OP = 'unary-relational-op'
RELATIONAL_OP = 'relational-op'
LOGICAL_OP = 'logical-op'
RESERVED_WORD = 'reserved-word'
RESERVED_SYMBOL = 'reserved-symbol'

TEXT_LIT = 'text-literal'
INT_LIT = 'integer-literal'
DEC_LIT = 'decimal-literal'
IDENTIFIER = 'identifier'

DESC_TOKEN_DICT = {
    # logical-op
    'AND': LOGICAL_OP,
    "BESTOW": RESERVED_WORD,
    "BLESSED": RESERVED_WORD,
    "CHEST": RESERVED_WORD,
    "CHOP": RESERVED_WORD,
    "CHRONO": RESERVED_WORD,
    "CURSED": RESERVED_WORD,
    "DAY": RESERVED_WORD,
    "ECHO": RESERVED_WORD,
    "FATE": RESERVED_WORD,
    "FUTURE": RESERVED_WORD,
    "GOLD": RESERVED_WORD,
    "HEAD": RESERVED_WORD,
    "HERMES": RESERVED_WORD,
    "HYDRA": RESERVED_WORD,
    "IN": RESERVED_WORD,
    "NONE": RESERVED_WORD,
    "NOT": RESERVED_WORD,
    "OFFER": RESERVED_WORD,
    "OLYMPUS": RESERVED_WORD,
    "OR": LOGICAL_OP,
    "PANDORA": RESERVED_WORD,
    "PAST": RESERVED_WORD,
    "PROPHECY": RESERVED_WORD,
    "QUEST": RESERVED_WORD,
    "RETRIAL": RESERVED_WORD,
    "REWARD": RESERVED_WORD,
    "SILVER": RESERVED_WORD,
    "SKIP": RESERVED_WORD,
    "SLAIN": RESERVED_WORD,
    "SONG": RESERVED_WORD,
    "STOP": RESERVED_WORD,
    "TRIAL": RESERVED_WORD,
    "VERDICT": RESERVED_WORD,

    # symbols
    '|<|': RESERVED_SYMBOL,
    '|>|': RESERVED_SYMBOL,

    # groupings
    '(': RESERVED_SYMBOL,
    ')': RESERVED_SYMBOL,
    '[': RESERVED_SYMBOL,
    ']': RESERVED_SYMBOL,
    '{': RESERVED_SYMBOL,
    '}': RESERVED_SYMBOL,

    # seperator and terminators
    ';': RESERVED_SYMBOL,
    ',': RESERVED_SYMBOL,
    ':': RESERVED_SYMBOL,
    '.': RESERVED_SYMBOL,

    # operators
    '+': ARITH_OP,
    '-': ARITH_OP,
    '*': ARITH_OP,
    '/': ARITH_OP,
    '%': ARITH_OP,
    '^': ARITH_OP,

    '>': RELATIONAL_OP,
    '>=': RELATIONAL_OP,
    '<': RELATIONAL_OP,
    '<=': RELATIONAL_OP,
    '!=': RELATIONAL_OP,
    '==': RELATIONAL_OP,
    '=': RELATIONAL_OP,

    '+=': ASSIGN_OP,
    '-=': ASSIGN_OP,
    '*=': ASSIGN_OP,
    '/=': ASSIGN_OP,
    '%=': ASSIGN_OP,
    '^=': ASSIGN_OP,

    TextLiteralToken: TEXT_LIT,
    IntegerLiteralToken: INT_LIT,
    DecimalLiteralToken: DEC_LIT,
    IdentifierToken: IDENTIFIER,
}
