"""
Read and excute strings to lexical tokens
"""
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _
from .base import (
    IntegerLiteralToken,
    IdentifierToken,
    DecimalLiteralToken,
    TextLiteralToken,
    CommentToken,
)
from .tokens import TOKEN_DICT

import re


class LexicalValidationError(ValidationError):

    def __init__(self, message, code=None, params=None, line=0, char_line=0):
        super().__init__(message, code, params)
        self.line = line
        self.char_line = char_line


class LexExecute:
    LIMIT_INTEGER = 9 # not here maybe
    LIMIT_DECIMAL = 5

    def __init__(self):
        self.ERROR_LIST = []
        self.tokenize_arr = []

    def append_token(self, text="", line=0, index=0, type_lit=None):
        self.tokenize_arr.append(self.text_to_token(text, line, index, type_lit))

    def append_error(self, message=" ", code="root", line=0, char_line=0):
        # bugged not reading code
        self.ERROR_LIST.append(LexicalValidationError(_(message),
            code=code, line=line, char_line=char_line))

    def text_to_token(self, text="", line=0, index=0, type_lit=None):
        if text:
            try:
                if type_lit: return TOKEN_DICT[type_lit](text, line)
                return TOKEN_DICT[text](text, line)
            except Exception as e:

                # if a number and  whole number is within 9 go lexical?
                if text.isdigit() and len(text) <= self.LIMIT_INTEGER:
                    return TOKEN_DICT[IntegerLiteralToken](text, line)

                if '.' in text:
                    num_arr = text.split('.')
                    if len(num_arr[0]) <= self.LIMIT_INTEGER \
                        and len(num_arr[1]) <= self.LIMIT_DECIMAL \
                        and num_arr[1] and all(map(lambda x: x.isdigit(), num_arr)):
                        return TOKEN_DICT[DecimalLiteralToken](text, line)

                if re.match(r"^[\_a-zA-Z][\_A-Za-z0-9]{0,31}$", text):
                    return TOKEN_DICT[IdentifierToken](text, line)

                self.append_error(
                    f"No lexical conversion found for {text}",
                    code='conversion', line=line, char_line=index)
        # return (text, line, type_lit)
        return None

    def execute(self, string_arr=[]):
        if not string_arr: return []

        for line, string in enumerate(string_arr, start=1):
            string_strip = string.strip() + ' '  # clean side +  ' ' detect last
            text, index = "", 0

            while index < len(string_strip):
                # raise Exception(list(string_strip))
                # print(char, index, line, text)
                char = string_strip[index]

                if char == '.' \
                    and text and not text.isdigit():
                    self.append_token(text, line, index)
                    self.append_token(char, line, index)
                    text , index = "", index + 1

                elif char == '|':
                    try:
                        if string_strip[index+1] in ['>', '<'] \
                            and string_strip[index+1+1] == '|':
                            char += string_strip[index+1:index+1+1+1]
                            index = index + 1 + 1 + 1
                        else: index = index + 1
                        if text: self.append_token(text, line, index)
                        self.append_token(char, line, index)
                    except Exception as e:
                        if text: self.append_token(text, line, index)
                        self.append_token(char, line, index)
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
                        if text: self.append_token(text, line, index)
                        self.append_token(char, line, index)
                    except:
                        if text: self.append_token(text, line, index)
                        self.append_token(char, line, index)
                        index = index+1
                    text = ""

                elif char in [
                            '(', ')', '[', ']', '{', '}',
                            ';', ':', ',',
                        ]:
                    if text: self.append_token(text, line, index)
                    self.append_token(char, line, index)
                    text, index = "", index +1

                elif char == '"':
                    replace, _text = string_strip[index::], ""
                    for _index, _char in enumerate(replace):
                        _text += _char
                        if _index == 0: continue
                        elif _char == '"': break

                    if _text[-1] != '"':
                        self.append_error(
                            f'Line: {line}: Not ending with quotation mark (")',
                            code='quote', line=line, char_line=_index)
                    self.append_token(text=_text, line=line, index=_index,
                        type_lit=TextLiteralToken)
                    index, text= index + _index + 1, ""

                # comment?
                elif text == "??":
                    self.append_token(
                        text=string_strip[string_strip.find(text)::],
                        line=line, index=index,type_lit=CommentToken)
                    break

                elif char == ' ':
                    if text: self.append_token(text, line, index)
                    text, index = "", index + 1

                else:
                    text, index = text + char, index + 1
                self.tokenize_arr = list(filter(None, self.tokenize_arr))
                # non-efficient, use for NONE bug  in ( )

        # raise Exception(self.ERROR_LIST)
        # raise Exception(list(map(lambda x: x.syntax_token, self.tokenize_arr)))
        if self.ERROR_LIST: raise LexicalValidationError(self.ERROR_LIST)
        return list(map(lambda x: x.val_to_dict(), self.tokenize_arr))


