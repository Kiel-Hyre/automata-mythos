from django.conf import settings
from django.forms import ValidationError
from backend.apps.lexxer.generate.ply import yacc
from .lex import (
    RESERVED_WORDS_LIST,
    MythLexer
)

DEBUG = settings.DEBUG

class SyntaxValidationError(ValidationError):
    def __init__(self, message, code='syntax', params=None, line=0, char_line=0):
        super().__init__(message, code, params)
        self.line = line
        self.char_line = char_line

class MythSyntax:
    lexer = MythLexer
    tokens = MythLexer.tokens
    start = 'program'

    def p_program(self, p):
        '''program : global OLYMPUS OPCOLUMN body CLCOLUMN excess'''

    def p_excess(self, p):
        '''excess : empty'''

    def p_program_olympus_error(self, p):
        '''program : global error OPCOLUMN body CLCOLUMN excess'''
        self.append_error('OLYMPUS keyword is missing',
            line=p.lineno(2),
            char_line=p[2].char_line)

    def p_program_excess_error(self, p):
        '''program : global OLYMPUS OPCOLUMN body CLCOLUMN error'''
        self.append_error('Unwanted characters after OLYMPUS block',
            line=p.lineno(6), char_line=self.lexer.find_column_lex(p.lexpos(6)))

    def p_global(self, p):
        '''global : pandora global
                  | chest global
                  | quest global
                  | declaration global
                  | SEMICOLON global
                  | empty'''

    # ID
    def p_dataType(self, p):
        '''dataType : SONG
                    | GOLD
                    | SILVER
                    | FATE'''

    def p_id(self, p):
        '''id : ID arrayChestQuestOption'''


    def p_arrayChestQuestOption(self, p):
        '''arrayChestQuestOption : arrayIndex chestArray
                                 | OPPAR questParamCall CLPAR'''

    def p_extraId(self, p):
        '''extraId : COMMA ID init extraId
                   | empty'''

    def p_body(self, p):
        '''body : statement
                | empty'''

    def p_declaration(self, p):
        '''declaration : SONG ID init extraId SEMICOLON
                       | GOLD ID init extraId SEMICOLON
                       | FATE ID init extraId SEMICOLON
                       | SILVER ID init extraId SEMICOLON
                       | ID ID init extraId SEMICOLON'''

    # brute due to ID ID ambiguity, it detects the 2nd ID as 1st ID
    # others dont need because once 1st ID it tries the RW
    # note maybe bugging the statement
    def p_declaration_ID_error(self, p):
        '''declaration : ID error init extraId SEMICOLON'''
        self.append_error(
            'Improper declaration : Specify a type',
            line=p.lineno(2),
            char_line=self.lexer.find_column_lex(p.lexpos(2)-1))

    def p_declaration_SEMICOLON(self, p):
        '''declaration : SONG ID init extraId error
                       | GOLD ID init extraId error
                       | FATE ID init extraId error
                       | SILVER ID init extraId error
                       | ID ID init extraId error'''
        self.append_error('Declaration missing terminator(;)',
            line=p.lineno(5),
            char_line=self.lexer.find_column_lex(p.lexpos(5)))

    def p_init(self, p):
        '''init : ASSIGN valueExpression
                | OPBRACK valueExpression CLBRACK arrayIndex arrayContinue
                | empty'''


    # questCall
    def p_value(self, p):
        '''value : TEXT
                 | NUM
                 | BOOL
                 | NONE
                 | id'''

    def p_parameter(self, p):
        '''parameter : dataType ID arrayInit parameterContinue
                     | empty'''

    def p_parameterContinue(self, p):
        '''parameterContinue : COMMA parameter
                             | empty'''

    # Array

    def p_arrayIndex(self, p):
        '''arrayIndex : OPBRACK valueExpression CLBRACK arrayIndex
                      | empty'''

    def p_arrayContinue(self, p):
        '''arrayContinue : ASSIGN OPCURL arrayValue CLCURL
                         | empty'''

    def p_arrayInit(self, p):
        '''arrayInit : OPBRACK CLBRACK arrayInit
                     | empty'''

    def p_arrayValue(self, p):
        '''arrayValue : OPCURL valueExpression extraArrayValue CLCURL extraMemoryArrayValue
                      | valueExpression extraArrayValue
                      | empty'''

    def p_extraArrayValue(self, p):
        '''extraArrayValue : COMMA valueExpression extraArrayValue
                           | empty'''

    def p_extraMemoryArrayValue(self, p):
        '''extraMemoryArrayValue : COMMA OPCURL valueExpression extraArrayValue CLCURL extraMemoryArrayValue
                                 | empty'''

    # Array

    # Expression

    def p_expression(self, p):
        '''expression : arithmeticExpression
                      | relationalExpression
                      | logicalExpression
                      | empty'''

    # ambiguity
    def p_valueExpression(self, p):
        '''valueExpression : OPPAR valueExpression CLPAR
                           | unaryOP valueExpression
                           | unaryOP value expression
                           | value expression'''

    def p_assignExpression(self, p):
        '''assignExpression : id assignOP valueExpression SEMICOLON'''

    def p_assignExpression_semicolon_error(self, p):
        '''assignExpression : id assignOP valueExpression error'''
        self.append_error('Missing terminator(;)',
            line=p.lineno(4),
            char_line=self.lexer.find_column_lex(p.lexpos(4))
        )

    def p_assignExpression_valueExpression_error(self, p):
        '''assignExpression : id assignOP error SEMICOLON'''
        self.append_error('No value to assigned to',
            line=p.lineno(3),
            char_line=self.lexer.find_column_lex(p.lexpos(3))
        )

    def p_assignOP(self, p):
        '''assignOP : ASSIGN
                    | ADD_ASSIGN
                    | SUB_ASSIGN
                    | MUL_ASSIGN
                    | DIV_ASSIGN
                    | MOD_ASSIGN
                    | POW_ASSIGN'''

    def p_arithmeticExpression(self, p):
        '''arithmeticExpression : arithmeticOP valueExpression'''

    def p_arithmeticExpression_valueExpression_error(self, p):
        '''arithmeticExpression : arithmeticOP error'''
        self.append_error('Missing value in expression', line=p.lineno(2),
            char_line=self.lexer.find_column_lex(p.lexpos(2)))

    def p_arithmeticOP(self, p):
        '''arithmeticOP : PLUS_OP
                        | MINUS_OP
                        | PRODUCT_OP
                        | DIV_OP
                        | MOD_OP
                        | POW_OP'''

    def p_logicalExpression(self, p):
        '''logicalExpression : logicalOP valueExpression'''

    def p_logicalExpression_valueExpression_error(self, p):
        '''logicalExpression : logicalOP error'''
        self.append_error('Missing value in expression', line=p.lineno(2),
            char_line=self.lexer.find_column_lex(p.lexpos(2)))

    def p_logicalOP(self, p):
        '''logicalOP : AND_OP
                     | OR_OP'''

    def p_relationalExpression(self, p):
        '''relationalExpression : relationalOP valueExpression'''

    def p_relationalExpression_valueExpression_error(self, p):
        '''relationalExpression : relationalOP error'''
        self.append_error('Missing value in expression', line=p.lineno(2),
            char_line=self.lexer.find_column_lex(p.lexpos(2)))

    def p_relationalOP(self, p):
        '''relationalOP : EQ_OP
                        | GT_OP
                        | GTE_OP
                        | LT_OP
                        | LTE_OP
                        | NE_OP'''

    def p_unaryOP(self, p):
        '''unaryOP : NOT_OP unaryOP
                   | MINUS_OP unaryOP
                   | empty'''

    # Expression

    # Chest

    def p_chest(self, p):
        '''chest : CHEST ID OPCOLUMN chestBody CLCOLUMN'''

    def p_idWithoutQuest(self, p):
        '''idWithoutQuest : ID arrayIndex chestArray'''

    def p_chestArray(self, p):
        '''chestArray : DOT idWithoutQuest chestArray
                      | empty'''

    def p_chestBody(self, p):
        '''chestBody : pandora chestBody
                     | declaration chestBody
                     | empty'''

    # Chest

    # Reserved Words

    def p_pandora(self, p):
        '''pandora : PANDORA declaration'''

    def p_slain(self, p):
        '''slain : SLAIN COLON statement
                 | empty'''

    def p_breaker(self, p):
        '''breaker : SKIP SEMICOLON
                   | STOP SEMICOLON
                   | empty'''

    def p_chrono(self, p):
        '''chrono : CHRONO OPPAR loopValueContainer past future day CLPAR OPCOLUMN loopBody CLCOLUMN'''

    def p_past(self, p):
        '''past : PAST valueExpression'''

    def p_future(self, p):
        '''future : FUTURE valueExpression'''

    def p_day(self, p):
        '''day : DAY valueExpression
               | empty'''

    def p_hermes(self, p):
        '''hermes : HERMES OPPAR loopValueContainer IN value CLPAR OPCOLUMN loopBody CLCOLUMN'''

    def p_prophecy(self, p):
        '''prophecy : PROPHECY OPPAR valueExpression CLPAR OPCOLUMN loopBody CLCOLUMN'''

    def p_head(self, p):
        '''head : HEAD OPPAR valueExpression CLPAR COLON statement chop head
                | empty'''


    def p_chop(self, p):
        '''chop : CHOP SEMICOLON
                | empty'''


    # Reserved Words

    # QUEST

    def p_quest(self, p):
        '''quest : QUEST ID OPPAR parameter CLPAR questReturn OPCOLUMN questStatement CLCOLUMN'''

    def p_questReturn(self, p):
        '''questReturn : REWARD dataType
                       | empty'''

    def p_questParamCall(self, p):
        '''questParamCall : valueExpression questCallContinue
                          | empty'''

    def p_questCallContinue(self, p):
        '''questCallContinue : COMMA questParamCall
                             | empty'''

    def p_questStatement(self, p):
        '''questStatement : BESTOW valueExpression SEMICOLON questStatement
                          | questTrial questStatement
                          | questIterationStatement questStatement
                          | questHydra questStatement
                          | singleStatement questStatement
                          | empty'''

    def p_questIterationStatement(self, p):
        '''questIterationStatement : questChrono
                                   | questProphecy
                                   | questHermes'''

    def p_questTrial(self, p):
        '''questTrial : TRIAL OPPAR valueExpression CLPAR OPCOLUMN questStatement CLCOLUMN questNextTrial questEndTrial'''

    def p_questNextTrial(self, p):
        '''questNextTrial : RETRIAL OPPAR valueExpression CLPAR OPCOLUMN questStatement CLCOLUMN questNextTrial
                          | empty'''

    def p_questEndTrial(self, p):
        '''questEndTrial : VERDICT OPCOLUMN questStatement CLCOLUMN
                         | empty'''

    def p_questHydra(self, p):
        '''questHydra : HYDRA OPPAR id CLPAR OPCOLUMN questCases CLCOLUMN'''

    def p_questCases(self, p):
        '''questCases : questHead questSlain
                      | empty'''

    def p_questHead(self, p):
        '''questHead : HEAD OPPAR valueExpression CLPAR COLON questStatement chop questHead
                     | empty'''

    def p_questSlain(self, p):
        '''questSlain : SLAIN COLON questStatement
                      | empty'''

    def p_questChrono(self, p):
        '''questChrono : CHRONO OPPAR loopValueContainer past future day CLPAR OPCOLUMN questLoopBody CLCOLUMN'''

    def p_loopValueContainer(self, p):
        '''loopValueContainer : dataType ID
                              | id'''

    def p_questLoopBody(self, p):
        '''questLoopBody : questLoopStatement breaker questLoopBody
                         | empty'''

    def p_questProphecy(self, p):
        '''questProphecy : PROPHECY OPPAR valueExpression CLPAR OPCOLUMN questLoopBody CLCOLUMN'''

    def p_questHermes(self, p):
        '''questHermes : HERMES OPPAR loopValueContainer IN value CLPAR OPCOLUMN questLoopBody CLCOLUMN'''

    def p_questForTrial(self, p):
        '''questForTrial : TRIAL OPPAR valueExpression CLPAR OPCOLUMN questLoopBody CLCOLUMN questForNextTrial questForEndTrial'''

    def p_questForNextTrial(self, p):
        '''questForNextTrial : RETRIAL OPPAR valueExpression CLPAR OPCOLUMN questLoopBody CLCOLUMN questForNextTrial
                             | empty'''

    def p_questForEndTrial(self, p):
        '''questForEndTrial : VERDICT OPCOLUMN questLoopBody CLCOLUMN
                            | empty'''

    def p_questForHydra(self, p):
        '''questForHydra : HYDRA OPPAR id CLPAR OPCOLUMN questForCases CLCOLUMN'''

    def p_questForCases(self, p):
        '''questForCases : questForHead questForSlain
                         | empty'''

    def p_questForHead(self, p):
        '''questForHead : HEAD OPPAR valueExpression CLPAR COLON questLoopBody chop questForHead
                        | empty'''

    def p_questForSlain(self, p):
        '''questForSlain : SLAIN COLON questLoopBody
                         | empty'''

    def p_questLoopStatement(self, p):
        '''questLoopStatement : singleStatement
                              | questForTrial
                              | questForHydra
                              | questIterationStatement
                              | BESTOW valueExpression SEMICOLON
                              | empty'''

    # QUEST

    # Statement

    def p_statement(self, p):
        '''statement : conditionalStatement body
                     | iterationStatement body
                     | singleStatement body
                     | empty'''

    # | questCall SEMICOLON
    def p_singleStatement(self, p):
        '''singleStatement : pandora
                           | declaration
                           | inputOutput
                           | assignExpression
                           | valueExpression SEMICOLON
                           | SEMICOLON'''

    def p_singleStatement_valueExpression_error(self, p):
        '''singleStatement : valueExpression error'''
        self.append_error('Missing terminator(;)',
            line=p.lineno(2),
            char_line=self.lexer.find_column_lex(p.lexpos(2)))

    def p_conditionalStatement(self, p):
        '''conditionalStatement : trial
                                | hydra'''

    def p_iterationStatement(self, p):
        '''iterationStatement : chrono
                              | hermes
                              | prophecy'''

    def p_output(self, p):
        '''output : valueExpression
                  | empty'''

    def p_inputOutput(self, p):
        '''inputOutput : OFFER OPPAR id CLPAR SEMICOLON
                       | ECHO OPPAR output CLPAR SEMICOLON'''

    def p_trial(self, p):
        '''trial : TRIAL OPPAR valueExpression CLPAR OPCOLUMN statement CLCOLUMN nextTrial endTrial'''

    def p_nextTrial(self, p):
        '''nextTrial : RETRIAL OPPAR valueExpression CLPAR OPCOLUMN statement CLCOLUMN nextTrial
                     | empty'''

    def p_endTrial(self, p):
        '''endTrial : VERDICT OPCOLUMN statement CLCOLUMN'''

    def p_hydra(self, p):
        '''hydra : HYDRA OPPAR id CLPAR OPCOLUMN cases CLCOLUMN'''

    def p_cases(self, p):
        '''cases : head slain
                 | empty'''

    def p_loopBody(self, p):
        '''loopBody : loopStatement breaker loopBody
                    | empty'''

    def p_loopStatement(self, p):
        '''loopStatement : singleStatement
                         | loopTrial
                         | loopHydra
                         | iterationStatement
                         | empty'''

    def p_loopTrial(self, p):
        '''loopTrial : TRIAL OPPAR valueExpression CLPAR OPCOLUMN loopBody CLCOLUMN loopNextTrial loopEndTrial'''

    def p_loopNextTrial(self, p):
        '''loopNextTrial : RETRIAL OPPAR valueExpression CLPAR OPCOLUMN loopBody CLCOLUMN loopNextTrial
                         | empty'''

    def p_loopEndTrial(self, p):
        '''loopEndTrial : VERDICT OPCOLUMN loopBody CLCOLUMN
                        | empty'''

    def p_loopHdyra(self, p):
        '''loopHydra : HYDRA OPPAR id CLPAR OPCOLUMN loopCases CLCOLUMN'''

    def p_loopCases(self, p):
        '''loopCases : loopHead loopSlain
                     | empty'''

    def p_loopHead(self, p):
        '''loopHead :  HEAD OPPAR valueExpression CLPAR COLON loopBody chop loopHead
                    | empty'''

    def p_loopSlain(self, p):
        '''loopSlain : SLAIN COLON loopBody
                     | empty'''

    def p_empty(self, p):
        'empty :'
        # print('Empty')
        pass

    def p_error(self, p):
        # None EOF
        if p is None:
            self.append_error(f"End Of File | Tip : put OLYMPUS block")
            return

        message = f"Syntax error : "
        if p.type not in RESERVED_WORDS_LIST: # Reserved words
            message += " before "
        self.append_error(
            message=f"{message} {p.value!r}", line=p.lineno, char_line=p.char_line)
        # self.parser.errok() # disable to use p_name_error


    def __init__(self,lex_debug=False, debug=False):
        self.lexer = self.lexer(debug=lex_debug)
        self.parser = yacc.yacc(start=self.start, module=self, debug=debug)
        self.ERROR_LIST = []
        self.found_MAIN = False

    def append_error(self, message="", code="syntax", params="", line=0, char_line=0):
        self.ERROR_LIST.append(SyntaxValidationError(message, code, params, line, char_line))

    def test(self, data, baseline=1, run_lexical=False):
        self.ERROR_LIST = []
        self.lexer.input(data, baseline)

        tracking = False
        if DEBUG: tracking = True
        result = self.parser.parse(data, lexer=self.lexer.lexer, tracking=False)
        return result



syntax = None
if DEBUG: syntax = MythSyntax(lex_debug=True, debug=True)
else:syntax = MythSyntax()

def parse(data="", baseline=1):

    syntax.test(data, baseline)

    if syntax.ERROR_LIST: raise SyntaxValidationError(syntax.ERROR_LIST)
    return syntax.lexer.TOKEN_LIST, True




