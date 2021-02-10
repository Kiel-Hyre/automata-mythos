"""
<ProgramToken> : <global> OLYMPUS |<| <body> |>|
    <global> : <CHEST> <global>, <QUEST> <global> , <declaration> <global>
               <PANDORA> <global> <comment> <global> ε




"""

from .base import *


CFG_DICT = {
    '<program>': ['<global>', OlympusToken, OpeningColumnToken,
            '<body>', CloseColumnToken],
    '<global>': ['<comment>', None],
    '<comment>': [CommentToken]
}


"""          <program>
             /    \
    <global>    OLYMPUS
                /   |      \
             |>|  <body>  |<|

1 + 1;

OLYMPUS |<|
|>|


[Opc, Cpc,]

[OLYMPUS, OpC, CpC]

"""


class Tree:
    description = ''
    children = []

    def __init__(self, data=None):
        self.data = data

class ProgramTree(Tree):
    description = '<program>'
    children = [GlobalTree, OlympusTree, None]

class GlobalTree(Tree):
    description = '<global>'
    children = [CommentTree, None]

class CommentTree(Tree):
    description = '<comment>'
    children = [CommentToken, None]



class Syntax:

    def __init__(self, lexes):
        self.lexes = lexes # tokenize_arr full of OBJS
        self.syntax = []
        self.ERRORS = []
        self.execute()

    def execute(self):
        # recursive?

        # base
        cfg_arr = CFG_DICT['<program>']

        for cfg in cfg_arr:



        return True

