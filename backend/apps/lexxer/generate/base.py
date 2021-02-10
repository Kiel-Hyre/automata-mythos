

# Base
class Token:
    title = ""
    description = ""

    def __init__(self, value="", ln=0, type=None):
        self.value = value
        self.line = ln
        self.type = None


    def val_to_dict(self):
        return {
            'value': self.value,
            'title': self.title,
            'description': self.description,
            'line': self.line
        }

    @property
    def syntax_token(self):
        return self.__class__.__name__

    def __repr__(self):
        return f"""
        title: {self.title} value: {self.value} line: {self.line} desc: {self.description}"""

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
    title = 'and'

class BestowToken(ReservedWordToken):
    title = 'bestow'

class BlessedToken(ReservedWordToken):
    title = 'blessed'

class ChestToken(ReservedWordToken):
    title = 'chest'

class ChopToken(ReservedWordToken):
    title = 'chop'

class ChronoToken(ReservedWordToken):
    title = 'chrono'

class CursedToken(ReservedWordToken):
    title = 'cursed'

class DayToken(ReservedWordToken):
    title = 'day'

class EchoToken(ReservedWordToken):
    title = 'ouput-call'

class FateToken(ReservedWordToken):
    title = 'fate'

class FutureToken(ReservedWordToken):
    title = 'future'

class GoldToken(ReservedWordToken):
    title = 'gold'

class HeadToken(ReservedWordToken):
    title = 'head'

class HermesToken(ReservedWordToken):
    title = 'hermes'

class HydraToken(ReservedWordToken):
    title = 'hydra'

class InToken(ReservedWordToken):
    title = 'in'

class NoneToken(ReservedWordToken):
    title = 'none'

class NotToken(LogicalOPToken):
    title = 'not'

class OfferToken(ReservedWordToken):
    title = 'offer'

class OlympusToken(ReservedWordToken):
    title = 'olympus'

class OrToken(LogicalOPToken):
    title = 'or'

class PandoraToken(ReservedWordToken):
    title = 'pandora'

class PastToken(ReservedWordToken):
    title = 'past'

class ProphecyToken(ReservedWordToken):
    title = 'prohecy'

class QuestToken(ReservedWordToken):
    title = 'quest'

class RetrialToken(ReservedWordToken):
    title = 'retrial'

class RewardToken(ReservedWordToken):
    title = 'reward'

class SilverToken(ReservedWordToken):
    title = 'SilverToken'

class SkipToken(ReservedWordToken):
    title = 'skip'

class SlainToken(ReservedWordToken):
    title = 'slain'

class SongToken(ReservedWordToken):
    title = 'song'

class StopToken(ReservedWordToken):
    title = 'stop'

class TrialToken(ReservedWordToken):
    title = 'trial'

class VerdictToken(ReservedWordToken):
    title = 'verdict'


# reserved symbols
class OpeningColumnToken(ReservedSymbolToken):
    title = 'opening-column'

class CloseColumnToken(ReservedSymbolToken):
    title = 'close-column'

class OpenParenthesisToken(ReservedSymbolToken):
    title = 'open-parenthesis'

class CloseParenthesisToken(ReservedSymbolToken):
    title = 'close-parenthesis'

class OpenBracketToken(ReservedSymbolToken):
    title = 'open-bracket'

class CloseBracketToken(ReservedSymbolToken):
    title = 'close-bracket'

class OpenCurlyToken(ReservedSymbolToken):
    title = 'open-curly'

class CloseCurlyToken(ReservedSymbolToken):
    title = 'close-curly'

class ColonToken(ReservedSymbolToken):
    title = 'colon'

class CommaToken(ReservedSymbolToken):
    title = 'comma'

class TerminatorToken(ReservedSymbolToken):
    title = 'terminator'

class AccessToken(ReservedSymbolToken):
    title = 'access'


# literals

class IntegerLiteralToken(Token):
    title = 'integer'
    description = 'integer-literal'

class DecimalLiteralToken(Token):
    title = 'decimal'
    description = 'decimal-literal'

class CommentToken(Token):
    title = 'comment'
    description = 'single-comment'

class TextLiteralToken(Token):
    title = 'text'
    description = 'text-literal'

class IdentifierToken(Token):
    title = 'id'
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
