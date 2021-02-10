

# Base
class Token:
    title = ""
    description = ""

    def __init__(self, value="", ln=0, char_line=0):
        self.value = value
        self.line = ln
        self.char_line = char_line + 1

    def val_to_dict(self):
        return {
            'value': self.value,
            'title': self.title,
            'description': self.description,
            'line': self.line,
            'char_line': self.char_line
        }

    @property
    def syntax_token(self):
        return self.__class__.__name__

    @property
    def type(self):
        return type(self)

    def __repr__(self):
        return f"""
        title: {self.title} value: {self.value} line: {self.line} desc: {self.description} charline: {self.char_line}"""

    def __str__(self):
        return self.value


# BaseMixin
class ReservedWordToken(Token):
    description = 'reserved-words'

class ReservedSymbolToken(Token):
    description = 'reserved-symbols'

class LogicalOPToken(Token):
    description = 'logical-op'

class UnaryLogicalOPToken(Token):
    description = 'unary-logical-op'

class ArithmeticOPToken(Token):
    description = 'arithmetic-op'

class RelationalOPToken(Token):
    description = 'relational-op'

class AssigmentOPToken(Token):
    description = 'assigment-op'


class AndToken(LogicalOPToken):
    title = 'AND'

class BestowToken(ReservedWordToken):
    title = 'BESTOW'

class BlessedToken(ReservedWordToken):
    title = 'BLESSED'

class ChestToken(ReservedWordToken):
    title = 'CHEST'

class ChopToken(ReservedWordToken):
    title = 'CHOP'

class ChronoToken(ReservedWordToken):
    title = 'CHRONO'

class CursedToken(ReservedWordToken):
    title = 'CURSED'

class DayToken(ReservedWordToken):
    title = 'DAY'

class EchoToken(ReservedWordToken):
    title = 'ECHO'

class FateToken(ReservedWordToken):
    title = 'FATE'

class FutureToken(ReservedWordToken):
    title = 'FUTURE'

class GoldToken(ReservedWordToken):
    title = 'GOLD'

class HeadToken(ReservedWordToken):
    title = 'HEAD'

class HermesToken(ReservedWordToken):
    title = 'HERMES'

class HydraToken(ReservedWordToken):
    title = 'HYDRA'

class InToken(ReservedWordToken):
    title = 'IN'

class NoneToken(ReservedWordToken):
    title = 'NONE'

class NotToken(LogicalOPToken):
    title = 'NOT'

class OfferToken(ReservedWordToken):
    title = 'OFFER'

class OlympusToken(ReservedWordToken):
    title = 'OLYMPUS'

class OrToken(LogicalOPToken):
    title = 'OR'

class PandoraToken(ReservedWordToken):
    title = 'PANDORA'

class PastToken(ReservedWordToken):
    title = 'PAST'

class ProphecyToken(ReservedWordToken):
    title = 'PROPHECY'

class QuestToken(ReservedWordToken):
    title = 'QUEST'

class RetrialToken(ReservedWordToken):
    title = 'RETRIAL'

class RewardToken(ReservedWordToken):
    title = 'REWARD'

class SilverToken(ReservedWordToken):
    title = 'SILVER'

class SkipToken(ReservedWordToken):
    title = 'SKIP'

class SlainToken(ReservedWordToken):
    title = 'SLAIN'

class SongToken(ReservedWordToken):
    title = 'SONG'

class StopToken(ReservedWordToken):
    title = 'STOP'

class TrialToken(ReservedWordToken):
    title = 'TRIAL'

class VerdictToken(ReservedWordToken):
    title = 'VERDICT'


# reserved symbols
class OpeningColumnToken(ReservedSymbolToken):
    title = '|<|'

class CloseColumnToken(ReservedSymbolToken):
    title = '|>|'

class OpenParenthesisToken(ReservedSymbolToken):
    title = '('

class CloseParenthesisToken(ReservedSymbolToken):
    title = ')'

class OpenBracketToken(ReservedSymbolToken):
    title = '['

class CloseBracketToken(ReservedSymbolToken):
    title = ']'

class OpenCurlyToken(ReservedSymbolToken):
    title = '{'

class CloseCurlyToken(ReservedSymbolToken):
    title = '}'

class ColonToken(ReservedSymbolToken):
    title = ':'

class CommaToken(ReservedSymbolToken):
    title = ','

class TerminatorToken(ReservedSymbolToken):
    title = ';'

class AccessToken(ReservedSymbolToken):
    title = '.'


# literals

class IntegerLiteralToken(Token):
    title = 'IntLit'
    description = 'integer-literal'

class DecimalLiteralToken(Token):
    title = 'DecLit'
    description = 'decimal-literal'

class CommentToken(Token):
    title = 'Comment'
    description = 'single-comment'

class TextLiteralToken(Token):
    title = 'TextLit'
    description = 'text-literal'

class IdentifierToken(Token):
    title = 'Id'
    description = 'identifier'


# arithmetic op
class AddOPToken(ArithmeticOPToken):
    title = '+'

class SubOPToken(ArithmeticOPToken):
    title = '-'

class MulOPToken(ArithmeticOPToken):
    title = '*'

class DivOPToken(ArithmeticOPToken):
    title = '/'

class ModuloOPToken(ArithmeticOPToken):
    title = '%'

class ExpOPToken(ArithmeticOPToken):
    title = '^'

class GTOPToken(RelationalOPToken):
    title = '>'

class LTOPToken(RelationalOPToken):
    title = '<'

class GTEOPToken(RelationalOPToken):
    title = '>='

class LTEOPToken(RelationalOPToken):
    title = '<='

class NEOPToken(RelationalOPToken):
    title = '!='

class EqualityOPToken(RelationalOPToken):
    title = '=='

class EqualOPToken(AssigmentOPToken):
    title = '='

class AddEqOPToken(AssigmentOPToken):
    title = '+='

class SubEqOPToken(AssigmentOPToken):
    title = '-='

class MulEqOPToken(AssigmentOPToken):
    title = '+='

class DivEqOPToken(AssigmentOPToken):
    title = '/='

class ModEqOPToken(AssigmentOPToken):
    title = '%='

class ExpEqOPToken(AssigmentOPToken):
    title = '^='
