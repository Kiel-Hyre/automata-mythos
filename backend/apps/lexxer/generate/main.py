"""
    generate lexical tokens
"""

import re

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

    def __repr__(self):
        return f"""
        title: {self.title} value: {self.value} line: {self.line} desc: {self.description}"""

    def __str__(self):
        return self.value


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

ERROR_LIST = []


import re

def text_to_token(text="", line=0, type_lit=None):
    if text:
        try:
            if type_lit: return TOKEN_DICT[type_lit](text, line)
            return TOKEN_DICT[text](text, line)
        except Exception as e:

            # if a number and  whole number is within 9 go lexical?
            if text.isdigit() and len(text) <= 9: return TOKEN_DICT[IntegerLiteralToken](text, line)

            # decimal ?
            if '.' in text:
                num_arr = text.split('.')
                if len(num_arr[0]) <= 9 and len(num_arr[1]) <= 5 \
                    and num_arr[1] and all(map(lambda x: x.isdigit(), num_arr)):
                    return TOKEN_DICT[DecimalLiteralToken](text, line)

            # [_a-z][]$* dapat mali pa to
            if re.match(r"^[\_a-zA-Z][\_A-Za-z0-9]{0,31}$", text):
                return TOKEN_DICT[IdentifierToken](text, line)

            raise Exception(f"line {line} no lexical conversion found for {text}")
    # return (text, line, type_lit)
    return None


def lex_execute(string_arr=[]):
    if not string_arr: return []

    tokenize_arr = []
    for line, string in enumerate(string_arr, start=1):
        string_strip = string.strip() + ' '  # clean side +  ' ' detect last
        text, index = "", 0

        while index < len(string_strip):
            # raise Exception(list(string_strip))
            char = string_strip[index] # for some reason bugged in for-loop
            print(char, index, line, text)             #notsure yet

            # special case .
            if char == '.' \
                and text and not text.isdigit():
                tokenize_arr.append(text_to_token(text, line))
                tokenize_arr.append(text_to_token(char, line))
                text , index = "", index + 1

            elif char == '|':
                try:
                    if string_strip[index+1] in ['>', '<'] \
                        and string_strip[index+1+1] == '|':
                        char += string_strip[index+1:index+1+1+1]
                        index = index + 1 + 1 + 1
                    else: index = index + 1
                    if text: tokenize_arr.append(text_to_token(text, line))
                    tokenize_arr.append(text_to_token(char, line))
                except Exception as e:
                    if text: tokenize_arr.append(text_to_token(text, line))
                    tokenize_arr.append(text_to_token(char, line))
                    index = index+1
                text = ""

            elif char in ['+', '-', '*', '/', '%', '^', '>', '<', '=', '!']:
                try:
                    if string_strip[index+1] == '=': # check if equals
                        # if so take it also as a char
                        char += string_strip[index+1]
                        index = index + 1 + 1
                    else: index = index + 1

                    # check before text
                    if text: tokenize_arr.append(text_to_token(text, line))
                    tokenize_arr.append(text_to_token(char, line))
                except:
                    if text: tokenize_arr.append(text_to_token(text, line))
                    tokenize_arr.append(text_to_token(char, line))
                    index = index+1
                text = ""

            elif char in [
                        '(', ')', '[', ']', '{', '}',
                        ';', ':',
                    ]:
                if text: tokenize_arr.append(text_to_token(text, line))
                tokenize_arr.append(text_to_token(char, line))
                text, index = "", index +1

            elif char == '"':
                replace, _text = string_strip[index::], ""
                for _index, _char in enumerate(replace):
                    _text += _char
                    if _index == 0: continue
                    elif _char == '"': break

                if _text[-1] != '"': raise Exception(
                    f'line: {line}: Not ending with quotation mark (")')
                tokenize_arr.append(
                    text_to_token(text=_text, line=line, type_lit=TextLiteralToken))
                index, text= index + _index + 1, ""

            # comment?
            elif text == "??":
                tokenize_arr.append(text_to_token(
                    string_strip[string_strip.find(text)::],
                    line,
                    type_lit=CommentToken)
                )
                break

            elif char == ' ':
                if text: tokenize_arr.append(text_to_token(text, line))
                text, index = "", index + 1

            else:
                text, index = text + char, index + 1
            tokenize_arr = list(filter(None, tokenize_arr)) # non-efficient, use for NONE error in ( )

    # if ERROR_LIST: raise Exception(ERROR_LIST)
    return list(map(lambda x: x.val_to_dict(), tokenize_arr))
    # raise Exception(tokenize_arr)

