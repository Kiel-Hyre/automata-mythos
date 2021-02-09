"""
    generate lexical tokens
"""

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

class CommentToken(Token):
    description = 'comment'

class TextLiteralToken(Token):
    description = 'text-literal'



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

class TerminatorToken(ReservedSymbolToken):
    title = 'terminator'



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

    '|<|': OpeningColumnToken,
    '|>|': CloseColumnToken,

    '(': OpenParenthesisToken,
    ')': CloseParenthesisToken,
    'TEXT-LIT': TextLiteralToken,
    '#': CommentToken,
    ';': TerminatorToken,
}


def text_to_token(text="", line=0, type_lit=None):
    if text:
        try:
            if type_lit: return TOKEN_DICT[type_lit](text, line)
            return TOKEN_DICT[text](text, line)
        except Exception as e:
            # raise Exception(e)
            pass
            # mostly do something for identifier, numlit, declit

            # the rest is error


    # return (text, line, type_lit)
    return None


def lex_execute(string_arr=[]):
    if not string_arr: return []

    tokenize_arr = []
    for line, string in enumerate(string_arr, start=1):
        string_strip = string.strip() + ' '  # clean side +  ' ' detect last
        text, index = "", 0

        while index < len(string_strip):

            char = string_strip[index] # for some reason bugged in for-loop

            print(char, index, line, text)
            if char in ['(', ')']:
                if text: tokenize_arr.append(text_to_token(text, index))
                tokenize_arr.append(text_to_token(char, index))
                text, index = "", index +1

            elif char == '"':
                replace, _text = string_strip[index::], ""
                for _index, _char in enumerate(replace):
                    _text += _char
                    if _index == 0: continue
                    elif _char == '"': break


                if _text[-1] != '"': raise Exception(
                    f'Not ending in quotation mark line: {line}'
                )
                tokenize_arr.append(
                    text_to_token(text=_text, line=line, type_lit='TEXT-LIT'))

                index, text= index + _index + 1, ""

            # comment?
            elif text == "??":
                tokenize_arr.append(text_to_token(
                    string_strip[string_strip.find(text)::],
                    index,
                    type_lit='#')
                )
                break

            elif char == ' ':
                if text: tokenize_arr.append(text_to_token(text, index))
                text, index = "", index + 1

            else:
                text, index = text + char, index + 1
            tokenize_arr = list(filter(None, tokenize_arr)) # non-efficient, use for NONE error in ( )

    return list(map(lambda x: x.val_to_dict(), tokenize_arr))
    # raise Exception(tokenize_arr)

