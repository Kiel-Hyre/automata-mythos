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

    def __repr__(self):
        return f"""
        title: {self.title} value: {self.value} line: {self.line} desc: {self.description}"""

    def __str__(self):
        return self.value, self.line


class ReservedWordToken(Token):
    description = 'reserved-words'

class ReservedSymbolToken(Token):
    description = 'reserved-symbols'

class TextLiteralToken(Token):
    description = 'text-literal'

class CommentToken(Token):
    description = 'comment'


class OlympusToken(ReservedWordToken):
    title = 'olympus'

class EchoColumnToken(ReservedWordToken):
    title = 'ouput-call'

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
    'OLYMPUS': OlympusToken,
    '|<|': OpeningColumnToken,
    '|>|': CloseColumnToken,
    'ECHO': EchoColumnToken,
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
                tokenize_arr.append( # BOGGED pa pano pag wla tlga end quote
                    text_to_token(text=_text, line=line, type_lit='TEXT-LIT'))

                # if index == 5: raise Exception(char, _text, _index)


                index, text= index + _index + 1, ""

            elif char == ' ':
                if text: tokenize_arr.append(text_to_token(text, index))
                text, index = "", index + 1

            else:
                text, index = text + char, index + 1
            tokenize_arr = list(filter(None, tokenize_arr)) # non-efficient, use for NONE error in ( )

    #return list(map(lambda x: x.value, tokenize_arr))
    raise Exception(tokenize_arr)

            # comments

            # special cases of columns
            # operators

            # single delims here?
            # if char in ['(', ')']:
            #     if tokenize_arr[-1] != text: # not yet already
            #         tokenize_arr.append(text_to_token(text, line)) # ECHO
            #     tokenize_arr.append(text_to_token(i, line)) # (
            #     text = ""
            #     continue






        # for index in range(len(string_strip)):
        #     char = string_strip[index] # due to the bug, enumerate does not change val

        #     # print(char, text)

        #     if char == '"':
        #         replace = string_strip[index::]
        #         _text = ""

        #         for _index, _char in enumerate(replace):
        #             _text += _char
        #             if _index == 0: continue
        #             elif _char == 0: break
        #         tokenize_arr.append(
        #             text_to_token(text=_text, line=line, type_lit='TEXT-LIT'))
        #         index, text= _index+1, ""

        #         print(index)
        #         continue

        #     if char == '$':
        #         if text:
        #             raise Exception(text)
        #             tokenize_arr.append(text_to_token(text, index))
        #         text = ""
        #         continue



        # for index, char in enumerate(string_strip):
        #     print(index, char, string_strip, text)
        #     if char == '"':
        #         replace = string_strip[index::] # from current to last
        #         _text = ""

        #         for _index, _char in enumerate(replace):
        #             _text += _char
        #             if _index == 0: continue
        #             elif _char == 0: break

        #         tokenize_arr.append(text_to_token(text=_text, line=line, type_lit='TEXT-LIT'))
        #         string_strip = replace[_index+1::]
        #         continue



            # if str_main == ' ': # basic delim
            #     if text:
            #         raise Exception(text)
            #         tokenize_arr.append(text_to_token(text, index))
            #     text = ""
            #     continue



        #     # comment?
        #     # if text == "??":
        #     #     tokenize_arr.append(text_to_token(
        #     #         string_strip[string_strip.find(text)::],
        #     #         index,
        #     #         type_lit='#')
        #     #     )
        #     #     break

        #     # single delims here?
        #     if i in ['(', ')', ';']:
        #         if tokenize_arr[-1] != text: # not yet already
        #             tokenize_arr.append(text_to_token(text, index)) # ECHO
        #         tokenize_arr.append(text_to_token(i, index)) # (
        #         text = ""
        #         continue


