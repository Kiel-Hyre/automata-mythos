from .base import *

class Syntax:
    def __init__(self, lexes):
        self.lexes = lexes # tokenize_arr full of OBJS
        self.execute()

    def execute(self):
        return True
