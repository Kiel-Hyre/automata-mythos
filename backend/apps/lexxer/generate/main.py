"""
Read and excute strings to lexical tokens
"""
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .base import (
    IntegerLiteralToken,
    IdentifierToken,
    DecimalLiteralToken,
)
from .tokens import TOKEN_DICT

import re

class LexExecute:
    LIMIT_INTEGER = 9 # not here maybe
    LIMIT_DECIMAL = 5

    def __init__(self):
        self.ERROR_LIST = []

    def append_error(self, message=" ", code="root"):
        self.ERROR_LIST.append(ValidationError(_(message), code=code))

    def text_to_token(self, text="", line=0, type_lit=None):
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
                    f"Line {line}: No lexical conversion found for {text}",
                    code='invalid')

        # return (text, line, type_lit)
        return None

    def execute(self, string_arr=[]):
        if not string_arr: return []

        tokenize_arr = []
        for line, string in enumerate(string_arr, start=1):
            string_strip = string.strip() + ' '  # clean side +  ' ' detect last
            text, index = "", 0

            while index < len(string_strip):
                # raise Exception(list(string_strip))
                # print(char, index, line, text)
                char = string_strip[index]

                if char == '.' \
                    and text and not text.isdigit():
                    tokenize_arr.append(self.text_to_token(text, line))
                    tokenize_arr.append(self.text_to_token(char, line))
                    text , index = "", index + 1

                elif char == '|':
                    try:
                        if string_strip[index+1] in ['>', '<'] \
                            and string_strip[index+1+1] == '|':
                            char += string_strip[index+1:index+1+1+1]
                            index = index + 1 + 1 + 1
                        else: index = index + 1
                        if text: tokenize_arr.append(self.text_to_token(text, line))
                        tokenize_arr.append(self.text_to_token(char, line))
                    except Exception as e:
                        if text: tokenize_arr.append(self.text_to_token(text, line))
                        tokenize_arr.append(self.text_to_token(char, line))
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
                        if text: tokenize_arr.append(self.text_to_token(text, line))
                        tokenize_arr.append(self.text_to_token(char, line))
                    except:
                        if text: tokenize_arr.append(self.text_to_token(text, line))
                        tokenize_arr.append(self.text_to_token(char, line))
                        index = index+1
                    text = ""

                elif char in [
                            '(', ')', '[', ']', '{', '}',
                            ';', ':', ',',
                        ]:
                    if text: tokenize_arr.append(self.text_to_token(text, line))
                    tokenize_arr.append(self.text_to_token(char, line))
                    text, index = "", index +1

                elif char == '"':
                    replace, _text = string_strip[index::], ""
                    for _index, _char in enumerate(replace):
                        _text += _char
                        if _index == 0: continue
                        elif _char == '"': break

                    if _text[-1] != '"':
                        self.append_error(
                            f'Line: {line}: Not ending with quotation mark (")')
                    tokenize_arr.append(
                        self.text_to_token(text=_text, line=line, type_lit=TextLiteralToken))
                    index, text= index + _index + 1, ""

                # comment?
                elif text == "??":
                    tokenize_arr.append(self.text_to_token(
                        string_strip[string_strip.find(text)::],
                        line,
                        type_lit=CommentToken)
                    )
                    break

                elif char == ' ':
                    if text: tokenize_arr.append(self.text_to_token(text, line))
                    text, index = "", index + 1

                else:
                    text, index = text + char, index + 1
                tokenize_arr = list(filter(None, tokenize_arr))
                # non-efficient, use for NONE error in ( )

        if self.ERROR_LIST: raise ValidationError(self.ERROR_LIST)
        return list(map(lambda x: x.val_to_dict(), tokenize_arr))
        # raise Exception(tokenize_arr)

