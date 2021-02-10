from .base import *

TOKEN_DICT = {
    # logical-op
    'AND': AndToken,
    "BESTOW": BestowToken,
    "BLESSED": BlessedToken,
    "CHEST": ChestToken,
    "CHOP": ChopToken,
    "CHRONO": ChronoToken,
    "CURSED": CursedToken,
    "DAY": DayToken,
    "ECHO": EchoToken,
    "FATE": FateToken,
    "FUTURE": FutureToken,
    "GOLD": GoldToken,
    "HEAD": HeadToken,
    "HERMES": HermesToken,
    "HYDRA": HydraToken,
    "IN": InToken,
    "NONE": NoneToken,
    "NOT": NotToken,
    "OFFER": OfferToken,
    "OLYMPUS": OlympusToken,
    "OR": OrToken,
    "PANDORA": PandoraToken,
    "PAST": PastToken,
    "PROPHECY": ProphecyToken,
    "QUEST": QuestToken,
    "RETRIAL": RetrialToken,
    "REWARD": RewardToken,
    "SILVER": SilverToken,
    "SKIP": SkipToken,
    "SLAIN": SlainToken,
    "SONG": SongToken,
    "STOP": StopToken,
    "TRIAL": TrialToken,
    "VERDICT": VerdictToken,

    # symbols
    '|<|': OpeningColumnToken,
    '|>|': CloseColumnToken,

    # groupings
    '(': OpenParenthesisToken,
    ')': CloseParenthesisToken,
    '[': OpenBracketToken,
    ']': CloseBracketToken,
    '{': OpenCurlyToken,
    '}': CloseCurlyToken,

    # seperator and terminators
    ';': TerminatorToken,
    ',': CommaToken,
    ':': ColonToken,
    '.': AccessToken,

    # operators
    '+': AddOPToken,
    '-': SubOPToken,
    '*': MulOPToken,
    '/': DivOPToken,
    '%': ModuloOPToken,
    '^': ExpOPToken,

    '>': GTOPToken,
    '>=': GTEOPToken,
    '<': LTOPToken,
    '<=': LTEOPToken,
    '!=': NEOPToken,
    '==': EqualityOPToken,
    '=': EqualOPToken,

    '+=': AddEqOPToken,
    '-=': SubEqOPToken,
    '*=': MulEqOPToken,
    '/=': DivEqOPToken,
    '%=': MulEqOPToken,
    '^=': ExpEqOPToken,

    TextLiteralToken: TextLiteralToken, # breachable example "  TEXT-LIT ECHO()"
    CommentToken: CommentToken,  # breachable example   " # ECHO()"
    IntegerLiteralToken: IntegerLiteralToken,
    DecimalLiteralToken: DecimalLiteralToken,
    IdentifierToken: IdentifierToken,
}
