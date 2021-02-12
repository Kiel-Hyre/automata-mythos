from django.forms import ValidationError
from backend.apps.lexxer.generate.ply import yacc
from .lex import MythLexer


class SyntaxValidationError(ValidationError):

    def __init__(self, message, code='syntax', params=None, line=0, char_line=0):
        super().__init__(message, code, params)
        self.line = line
        self.char_line = char_line

class MythSyntax:
    # lexer = MythLexer
    tokens = MythLexer.tokens
    start = 'program'

    def p_program(self, p):
        '''program : global OLYMPUS OPCOLUMN body CLCOLUMN'''

    def p_global(self, p):
        '''global : pandora global
                  | chest global
                  | quest global
                  | declaration global
                  | empty'''

    def p_body(self, p):
        '''body : statement
                | empty'''

    def p_statement(self, p):
        '''statement : chest body
                     | quest body
                     | declaration body
                     | pandora body
                     | inputOutput body
                     | trial body
                     | hydra body
                     | chrono body
                     | hermes body
                     | prophecy body
                     | questCall body
                     | varOperations body
                     | empty'''


    # missing CHESTID = ID ??
    def p_dataType(self, p):
        '''dataType :  SONG
                     | FATE
                     | GOLD
                     | SILVER
                     | ID'''

    # value
    def p_value(self, p):
        '''value : TEXT
                 | NUM
                 | BOOL
                 | NONE
                 | ID
                 | questCall
                 | chestAccess'''

    def p_valueExpr(self, p):
        '''valueExpr : OPPAR unaryOp value expression CLPAR
                     | unaryOp value expression'''


    # expression
    # MAYBE THERE IS ONE MORE OPTION NA MERON ()
    def p_expression(self, p):
        '''expression : OPPAR expressionOption CLPAR
                      | expressionOption
                      | empty'''

    def p_expressionOption(self, p):
        '''expressionOption : arithmeticExpression
                            | relationalExpression
                            | logicalExpression'''

    def p_logicalExpression(self, p):
        '''logicalExpression : logicalOP valueExpr'''

    def p_logicalOP(self, p):
        '''logicalOP : AND_OP
                     | OR_OP'''

    def p_relationalExpression(self, p):
        '''relationalExpression : relationalOP valueExpr'''

    def p_relationalOP(self, p):
        '''relationalOP : EQ_OP
                        | GT_OP
                        | GTE_OP
                        | LT_OP
                        | LTE_OP
                        | NE_OP'''

    def p_arithmeticExpression(self, p):
        '''arithmeticExpression : arithmeticOP valueExpr'''

    def p_arithmeticOP(self, p):
        '''arithmeticOP : PLUS_OP
                        | MINUS_OP
                        | PRODUCT_OP
                        | DIV_OP
                        | MOD_OP
                        | POW_OP'''

    # new MINUS  , unaryLocialOP before
    def p_unaryOp(self, p):
        '''unaryOp : NOT_OP unaryLoop
                   | MINUS_OP unaryLoop
                   | empty'''

    # weird?
    def p_unaryLoop(self, p):
        '''unaryLoop : unaryOp'''

    def p_assignOp(self, p):
        '''assignOp : ASSIGN
                    | ADD_ASSIGN
                    | SUB_ASSIGN
                    | MUL_ASSIGN
                    | DIV_ASSIGN
                    | MOD_ASSIGN
                    | POW_ASSIGN'''

    # WALANG GAMIT ???
    def p_chestAccess(self, p):
        '''chestAccess : ID DOT ID'''


    def p_varOperations(self, p):
        '''varOperations : ID assignOp valueExpr SEMICOLON'''

    # declaration
    def p_declaration(self, p):
        '''declaration : dataType ID init extraId SEMICOLON'''


    # id and array
    def p_init(self, p):
        '''init : ASSIGN valueExpr
                | OPBRACK arraySize CLBRACK extraArraySizeDeclaration arrayContinue
                | empty'''

    # array
    def p_arraySize(self, p):
        '''arraySize : valueExpr
                     | ID'''

    def p_extraArraySizeDeclaration(self, p):
        '''extraArraySizeDeclaration : OPBRACK arraySize CLBRACK extraArraySizeDeclaration
                                     | empty'''

    def p_arrayContinue(self, p):
        '''arrayContinue : ASSIGN OPCURL arrayValue CLCURL
                         | empty'''

    def p_arrayValue(self, p):
        '''arrayValue : OPCURL valueExpr extraArrayValue CLCURL extraMemoryArrayValue
                      | valueExpr extraArrayValue
                      | empty'''

    def p_extraArrayValue(self, p):
        '''extraArrayValue : COMMA valueExpr extraArrayValue
                           | empty'''

    def p_extraMemoryArrayValue(self, p):
        '''extraMemoryArrayValue : COMMA OPCURL valueExpr extraArrayValue CLCURL extraMemoryArrayValue
                                 | empty'''

    # id
    def p_extraId(self, p):
        '''extraId : COMMA ID init extraId
                   | empty'''


    # CHRONO
    def p_chrono(self, p):
        '''chrono : CHRONO OPPAR chronoIterable forStatement CLPAR OPCOLUMN loopBody CLCOLUMN'''

    def p_chronoIterable(self, p):
        '''chronoIterable : chronoDataType ID
                          | ID'''

    def p_chronoDataType(self, p):
        '''chronoDataType : GOLD
                          | SILVER'''

    def p_forStatement(self, p):
        '''forStatement : past future day'''

    def p_past(self, p):
        '''past : PAST valueExpr'''

    def p_future(self, p):
        '''future : FUTURE valueExpr'''

    def p_day(self, p):
        '''day : DAY valueExpr
               | empty'''

    # statement after breaker?
    def p_loopBody(self, p):
        '''loopBody : statement breaker
                    | empty'''

    def p_breaker(self, p):
        '''breaker : stop
                   | skip'''

    def p_stop(self, p):
        '''stop : STOP SEMICOLON
                | empty'''

    def p_skip(self, p):
        '''skip : SKIP SEMICOLON
                | empty'''

    # HERMES
    def p_hermes(self, p):
        '''hermes : HERMES OPPAR forEachStatement CLPAR OPCOLUMN loopBody CLCOLUMN'''

    ## ???
    def p_forEachStatement(self, p):
        '''forEachStatement : dataType ID IN value'''

    # PROPHECY
    def p_prophecy(self, p):
        '''prophecy : PROPHECY OPPAR valueExpr CLPAR OPCOLUMN loopBody CLCOLUMN'''

    # TRIAL
    def p_trial(self, p):
        '''trial : TRIAL OPPAR valueExpr CLPAR OPCOLUMN statement CLCOLUMN nextTrial'''

    def p_nextTrial(self, p):
        '''nextTrial : RETRIAL OPPAR valueExpr CLPAR OPCOLUMN statement CLCOLUMN nextTrial
                     | VERDICT OPCOLUMN statement CLCOLUMN
                     | empty'''


    # HYDRA
    def p_hydra(self, p):
        '''hydra : HYDRA OPPAR valueExpr CLPAR OPCOLUMN cases CLCOLUMN'''

    def p_cases(self, p):
        '''cases : head slain
                 | empty'''

    def p_head(self, p):
        '''head : HEAD OPPAR valueExpr CLPAR COLON body chop head
                | empty'''

    def p_chop(self, p):
        '''chop : CHOP SEMICOLON
                | empty'''

    def p_slain(self, p):
        '''slain : SLAIN COLON body
                 | empty'''

    # INPUT OUPUT
    def p_inputOutput(self, p):
        '''inputOutput : OFFER OPPAR ID CLPAR SEMICOLON
                       | ECHO OPPAR valueExpr CLPAR SEMICOLON'''

    # PANDORA
    def p_pandora(self, p):
        '''pandora : PANDORA declaration'''

    # CHEST
    def p_chest(self, p):
        '''chest : CHEST ID OPCOLUMN chestBody CLCOLUMN'''

    def p_chestBody(self, p):
        '''chestBody : pandora chestBody
                     | declaration chestBody
                     | empty'''


    # QUEST call
    def p_questCall(self, p):
        '''questCall : ID OPPAR questParamCall CLPAR'''

    def p_questParamCall(self, p):
        '''questParamCall : valueExpr questCallCont
                          | questCall
                          | empty'''

    def p_questCallCont(self, p):
        '''questCallCont : COMMA questParamCall'''

    # QUEST
    def p_quest(self, p):
        '''quest : QUEST questBody'''

    def p_questBody(self, p):
        '''questBody : ID OPPAR parameter CLPAR questVoidOrNot'''

    def p_questVoidOrNot(self, p):
        '''questVoidOrNot : REWARD dataType OPCOLUMN body BESTOW returnValue SEMICOLON CLCOLUMN
                            | OPCOLUMN body CLCOLUMN'''

    def p_parameter(self, p):
        '''parameter : dataType ID arrayInit parameterCont
                     | empty'''

    def p_arrayInit(self, p):
        '''arrayInit : OPBRACK CLBRACK arrayInit
                       | empty'''

    def p_parameterCont(self, p):
        '''parameterCont : COMMA parameter
                          | empty'''

    def p_returnValue(self, p):
        '''returnValue : valueExpr'''

    def p_empty(self, p):
        'empty :'
        pass

    def p_error(self, p):
        # sometimes None
        if p == None: self.append_error(f"Unable to detect!")
        else: self.append_error(f"Syntax error at {p.value!r}")

    def __init__(self):
        # self.lexer = self.lexer()
        self.parser = yacc.yacc(start=self.start, module=self, debug=True)
        self.ERROR_LIST = []

    def append_error(self, message):
        self.ERROR_LIST.append(SyntaxValidationError(message))

    def test(self, data):
        result = self.parser.parse(data ,tracking=True)
        return result

def parse(data=""):
    syntax = MythSyntax()
    syntax.test(data)
    if syntax.ERROR_LIST: raise SyntaxValidationError(syntax.ERROR_LIST)
    return True




