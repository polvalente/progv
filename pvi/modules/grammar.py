import ply.yacc as yacc
import ply.lex as lex
import tokens
from tokens import tokens

start = 'progv'

def p_progv(p):
    'progv : element progv'
    p[0] = [p[1]] + p[2]

def p_progv_empty(p):
    'progv : '
    p[0] = []

def p_element_function(p):
    '''element : FUNCTION IDENTIFIER LPAREN optparams RPAREN compoundstmt'''
    p[0] = ("function", p[2], p[4], p[6])

def p_element_stmt(p):
    "element : sstmt"
    p[0] = ("stmt", p[1])

def p_optparams(p):
    "optparams : params"
    p[0] = p[1]

def p_optparams_empty(p):
    "optparams : "
    p[0] = []

def p_params(p):
    'params : IDENTIFIER COMMA params'
    p[0] = [p[1]] + p[3]

def p_params_one(p):
    'params : IDENTIFIER'
    p[0] = [p[1]]

def p_compoundstmt(p):
    'compoundstmt : LBRACE stmts RBRACE'
    p[0] = p[2]

def p_stmts(p):
    'stmts : sstmt stmts'
    p[0] = [p[1]] + p[2]

def p_stmt_or_compound(p):
    'stmt_or_compound : sstmt'
    p[0] = [p[1]]

def p_stmt_or_compound_c(p):
    'stmt_or_compound : compoundstmt'
    p[0] = p[1]


def p_optsemi_none(p):
    'optsemi : '
    p[0] = p[0]

def p_optsemi_some(p):
    'optsemi : SEMICOLON'
    p[0] = p[0]

def p_stmts_empty(p):
    'stmts : '
    p[0] = []


def p_sstmt_break(p):
    'sstmt : BREAK'
    p[0] = ("break",)

def p_sstmt_continue(p):
    'sstmt : CONTINUE'
    p[0] = ("continue",)

def p_sstmt_if(p):
    'sstmt : IF exp stmt_or_compound optsemi %prec LOWER_THAN_ELSE'
    p[0] = ("if-then",p[2],p[3])

def p_sstmt_while(p):
    'sstmt : WHILE exp stmt_or_compound optsemi'
    p[0] = ("while", p[2], p[3])

def p_sstmt_do_while(p):
    'sstmt : DO compoundstmt WHILE exp optsemi'
    p[0] = ("do-while", p[2],p[4])

def p_sstmt_if_else(p):
    'sstmt : IF exp compoundstmt ELSE stmt_or_compound optsemi'
    p[0] = ("if-then-else",p[2],p[3],p[5])

def p_sstmt_assignment(p):
    'sstmt : IDENTIFIER EQUAL exp optsemi'
    p[0] = ("assign", p[1], p[3])

def p_sstmt_return(p):
    'sstmt : RETURN exp optsemi'
    p[0] = ("return", p[2])

def p_sstmt_var(p):
    'sstmt : VAR IDENTIFIER EQUAL exp optsemi'
    p[0] = ("var",p[2],p[4])

def p_sstmt_exp(p):
    'sstmt : exp optsemi'
    p[0] = ("exp", p[1])

def p_assign_or_var(p):
    'assign_or_var : IDENTIFIER EQUAL exp'
    p[0] = ("assign", p[1], p[3])

def p_assign_or_var_v(p):
    'assign_or_var : VAR IDENTIFIER EQUAL exp'
    p[0] = ("var",p[2],p[4])

def p_assign_or_stmt(p):
    'assign_or_var_stmt : sstmt'
    p[0] = p[1]

def p_assign_or_stmt_a(p):
    'assign_or_stmt : IDENTIFIER EQUAL exp'
    p[0] = ("assign", p[1], p[3])

def p_assign_or_var_empty(p):
    'assign_or_var : '
    p[0] = []

def p_sstmt_for(p):
    'sstmt : FOR LPAREN assign_or_var SEMICOLON exp SEMICOLON assign_or_stmt RPAREN stmt_or_compound optsemi'
    p[0] = ("for", p[3], p[5], p[7], p[9])

###############
# expressions #
###############
precedence = (
        ('left','LOGICAL_OR'),        
        ('left','LOGICAL_AND'),        
        ('left','LOGICAL_EQUAL','LOGICAL_DIFF'),        
        ('left','LE','LT','GE','GT'),        
        ('left','PLUS','MINUS'),        
        ('left','TIMES','DIVIDE','MOD'),
        ('left','POWER'),
        ('right','LOGICAL_NOT'),
        ('nonassoc', 'LOWER_THAN_ELSE'),
        ('nonassoc', 'ELSE')
)

def p_exp_identifier(p):
    'exp : IDENTIFIER'
    p[0] = ("identifier", p[1])

def p_exp_number(p):
    'exp : NUMBER'
    p[0] = ('number', p[1])

def p_exp_string(p):
    'exp : STRING'
    p[0] = ("string", p[1])

def p_exp_true(p):
    'exp : TRUE'
    p[0] = ("true","true")

def p_exp_false(p):
    'exp : FALSE'
    p[0] = ("false","false")

def p_exp_logical_not(p):
    'exp : LOGICAL_NOT exp'
    p[0] = ("not", p[2])

def p_exp_parens(p):
    'exp : LPAREN exp RPAREN'
    p[0] = p[2]

def p_exp_lambda(p):
    'exp : FUNCTION LPAREN optparams RPAREN compoundstmt'
    p[0] = ("function", p[3], p[5])

def p_exp_binop(p):
    '''exp : exp LOGICAL_OR exp
           | exp LOGICAL_AND exp
           | exp LOGICAL_EQUAL exp
           | exp LOGICAL_DIFF exp
           | exp LT exp
           | exp GT exp
           | exp LE exp
           | exp GE exp
           | exp PLUS exp
           | exp MINUS exp
           | exp TIMES exp
           | exp DIVIDE exp
           | exp POWER exp
           | exp MOD exp'''
    p[0] = ('binop', p[1], p[2], p[3])


def p_exp_call(p):
    'exp : IDENTIFIER LPAREN optargs RPAREN'
    p[0] = ("call", p[1], p[3])

def p_optargs(p):
    'optargs : args'
    p[0] = p[1]

def p_optargs_empty(p):
    'optargs : '
    p[0] = []

def p_args(p):
    'args : exp COMMA args'
    p[0] = [p[1]] + p[3]

def p_args_one(p):
    'args : exp'
    p[0] = [p[1]]
