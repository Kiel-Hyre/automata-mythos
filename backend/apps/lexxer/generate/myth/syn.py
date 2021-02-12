from backend.apps.lexxer.generate.ply import yacc
from .lex import MythLexer

tokens = MythLexer.tokens
start = 'program'


def p_program(p):
    '''program : global OLYMPUS OPCOLUMN body CLCOLUMN'''

def p_global(p):
    '''global : pandora global
              | chest global
              | quest global
              | declaration global
              | empty'''

def p_body(p):
    '''body : statement
            | empty'''

def p_statement(p):
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
def p_dataType(p):
    '''dataType :  SONG
                 | FATE
                 | GOLD
                 | SILVER
                 | ID'''

# value
def p_value(p):
    '''value : TEXT
             | NUM
             | BOOL
             | NONE
             | ID
             | questCall
             | chestAccess'''

def p_valueExpr(p):
    '''valueExpr : OPPAR unaryOp value expression CLPAR
                 | unaryOp value expression'''


# expression
# MAYBE THERE IS ONE MORE OPTION NA MERON ()
def p_expression(p):
    '''expression : OPPAR expressionOption CLPAR
                  | expressionOption
                  | empty'''

def p_expressionOption(p):
    '''expressionOption : arithmeticExpression
                        | relationalExpression
                        | logicalExpression'''

def p_logicalExpression(p):
    '''logicalExpression : logicalOP valueExpr'''

def p_logicalOP(p):
    '''logicalOP : AND_OP
                 | OR_OP'''

def p_relationalExpression(p):
    '''relationalExpression : relationalOP valueExpr'''

def p_relationalOP(p):
    '''relationalOP : EQ_OP
                    | GT_OP
                    | GTE_OP
                    | LT_OP
                    | LTE_OP
                    | NE_OP'''

def p_arithmeticExpression(p):
    '''arithmeticExpression : arithmeticOP valueExpr'''

def p_arithmeticOP(p):
    '''arithmeticOP : PLUS_OP
                    | MINUS_OP
                    | PRODUCT_OP
                    | DIV_OP
                    | MOD_OP
                    | POW_OP'''

# new MINUS  , unaryLocialOP before
def p_unaryOp(p):
    '''unaryOp : NOT_OP unaryLoop
               | MINUS_OP unaryLoop
               | empty'''

# weird?
def p_unaryLoop(p):
    '''unaryLoop : unaryOp'''

def p_assignOp(p):
    '''assignOp : ASSIGN
                | ADD_ASSIGN
                | SUB_ASSIGN
                | MUL_ASSIGN
                | DIV_ASSIGN
                | MOD_ASSIGN
                | POW_ASSIGN'''

# WALANG GAMIT ???
def p_chestAccess(p):
    '''chestAccess : ID DOT ID'''


def p_varOperations(p):
    '''varOperations : ID assignOp valueExpr SEMICOLON'''

# declaration
def p_declaration(p):
    '''declaration : dataType ID init extraId SEMICOLON'''


# id and array
def p_init(p):
    '''init : ASSIGN valueExpr
            | OPBRACK arraySize CLBRACK extraArraySizeDeclaration arrayContinue
            | empty'''

# array
def p_arraySize(p):
    '''arraySize : valueExpr
                 | ID'''

def p_extraArraySizeDeclaration(p):
    '''extraArraySizeDeclaration : OPBRACK arraySize CLBRACK extraArraySizeDeclaration
                                 | empty'''

def p_arrayContinue(p):
    '''arrayContinue : ASSIGN OPCURL arrayValue CLCURL
                     | empty'''

def p_arrayValue(p):
    '''arrayValue : OPCURL valueExpr extraArrayValue CLCURL extraMemoryArrayValue
                  | valueExpr extraArrayValue
                  | empty'''

def p_extraArrayValue(p):
    '''extraArrayValue : COMMA valueExpr extraArrayValue
                       | empty'''

def p_extraMemoryArrayValue(p):
    '''extraMemoryArrayValue : COMMA OPCURL valueExpr extraArrayValue CLCURL extraMemoryArrayValue
                             | empty'''

# id
def p_extraId(p):
    '''extraId : COMMA ID init extraId
               | empty'''


# CHRONO
def p_chrono(p):
    '''chrono : CHRONO OPPAR chronoIterable forStatement CLPAR OPCOLUMN loopBody CLCOLUMN'''

def p_chronoIterable(p):
    '''chronoIterable : chronoDataType ID
                      | ID'''

def p_chronoDataType(p):
    '''chronoDataType : GOLD
                      | SILVER'''

def p_forStatement(p):
    '''forStatement : past future day'''

def p_past(p):
    '''past : PAST valueExpr'''

def p_future(p):
    '''future : FUTURE valueExpr'''

def p_day(p):
    '''day : DAY valueExpr
           | empty'''

def p_loopBody(p):
    '''loopBody : statement breaker loopBody
                | empty'''

def p_breaker(p):
    '''breaker : stop
               | skip'''

def p_stop(p):
    '''stop : STOP SEMICOLON
            | empty'''

def p_skip(p):
    '''skip : SKIP SEMICOLON
            | empty'''

# HERMES
def p_hermes(p):
    '''hermes : HERMES OPPAR forEachStatement CLPAR OPCOLUMN loopBody CLCOLUMN'''

## ???
def p_forEachStatement(p):
    '''forEachStatement : dataType ID IN value'''

# PROPHECY
def p_prophecy(p):
    '''prophecy : PROPHECY OPPAR valueExpr CLPAR OPCOLUMN loopBody CLCOLUMN'''

# TRIAL
def p_trial(p):
    '''trial : TRIAL OPPAR valueExpr CLPAR OPCOLUMN statement CLCOLUMN nextTrial'''

def p_nextTrial(p):
    '''nextTrial : RETRIAL OPPAR valueExpr CLPAR OPCOLUMN statement CLCOLUMN nextTrial
                 | VERDICT OPCOLUMN statement CLCOLUMN
                 | empty'''


# HYDRA
def p_hydra(p):
    '''hydra : HYDRA OPPAR valueExpr CLPAR OPCOLUMN cases CLCOLUMN'''

def p_cases(p):
    '''cases : head slain
             | empty'''

def p_head(p):
    '''head : HEAD OPPAR valueExpr CLPAR COLON body chop head
            | empty'''

def p_chop(p):
    '''chop : CHOP SEMICOLON
            | empty'''

def p_slain(p):
    '''slain : SLAIN COLON body
             | empty'''

# INPUT OUPUT
def p_inputOutput(p):
    '''inputOutput : OFFER OPPAR ID CLPAR SEMICOLON
                   | ECHO OPPAR valueExpr CLPAR SEMICOLON'''

# PANDORA
def p_pandora(p):
    '''pandora : PANDORA declaration'''

# CHEST
def p_chest(p):
    '''chest : CHEST ID OPCOLUMN chestBody CLCOLUMN'''

def p_chestBody(p):
    '''chestBody : pandora chestBody
                 | declaration chestBody
                 | empty'''


# QUEST call
def p_questCall(p):
    '''questCall : ID OPPAR questParamCall CLPAR'''

def p_questParamCall(p):
    '''questParamCall : valueExpr questCallCont
                      | questCall
                      | empty'''

def p_questCallCont(p):
    '''questCallCont : COMMA questParamCall'''

# QUEST
def p_quest(p):
    '''quest : QUEST questBody'''

def p_questBody(p):
    '''questBody : ID OPPAR parameter CLPAR questVoidOrNot'''

def p_questVoidOrNot(p):
    '''questVoidOrNot : REWARD dataType OPCOLUMN body BESTOW returnValue SEMICOLON CLCOLUMN
                        | OPCOLUMN body CLCOLUMN'''

def p_parameter(p):
    '''parameter : dataType ID arrayInit parameterCont
                 | empty'''

def p_arrayInit(p):
    '''arrayInit : OPBRACK CLBRACK arrayInit
                   | empty'''

def p_parameterCont(p):
    '''parameterCont : COMMA parameter
                      | empty'''

def p_returnValue(p):
    '''returnValue : valueExpr'''

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print(f"Syntax error at {p.value!r}")



# lexer = MythLexer()
parser = yacc.yacc(start=start, debug=True)

def parse(data=""):
    result = parser.parse(data, tracking=True)
    print(result)


# data = """
#     OLYMPUS |<|
#         GOLD v = 5;

#         v = -1;

#         GOLD vince[12] = {1,2,3,4};

#         TRIAL(v)|<|
#             GOLD v = 5;
#             ECHO(v);
#         |>|
#     |>|

#     """





