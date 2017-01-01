import ply.yacc as yacc
import ply.lex as lex
import progv_tokens
from progv_tokens import tokens

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
    "element : stmt SEMICOLON"
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

def p_compound_stmt(p):
    'compoundstmt : LBRACE stmts RBRACE'
    p[0] = p[2]

def p_stmts_empty(p):
    'stmts : '
    p[0] = []

def p_stmts(p):
    'stmts : stmt SEMICOLON stmts'
    p[0] = [p[1]] + p[3]

def p_stmt_if(p):
    'stmt : IF exp compoundstmt'
    p[0] = ("if-then",p[2],p[3])

def p_stmt_if_else(p):
    'stmt : IF exp compoundstmt ELSE compoundstmt'
    p[0] = ("if-then-else",p[2],p[3],p[5])

def p_stmt_assignment(p):
    'stmt : IDENTIFIER EQUAL exp'
    p[0] = ("assign", p[1], p[3])

def p_stmt_return(p):
    'stmt : RETURN exp'
    p[0] = ("return", p[2])

def p_stmt_var(p):
    'stmt : VAR IDENTIFIER EQUAL exp'
    p[0] = ("var",p[2],p[4])

def p_stmt_exp(p):
    'stmt : exp'
    p[0] = ("exp", p[1])

###############
# expressions #
###############

def p_exp_identifier(p):
    'exp : IDENTIFIER'
    p[0] = ("identifier", p[1])


#TESTS

progv_lexer = lex.lex(module=progv_tokens)
progv_parser = yacc.yacc()

def test_parser(input_string):
    progv_lexer.input(input_string)
    parse_tree = progv_parser.parse(input_string,lexer=progv_lexer)
    return parse_tree


# Simple function with no arguments and a one-statement body. 
jstext1 = "function myfun() { return nothing ; }" 
jstree1 = [('function', 'myfun', [], [('return', ('identifier', 'nothing'))])]  
print test_parser(jstext1) == jstree1  
# Function with multiple arguments. 

jstext2 = "function nobletruths(dukkha,samudaya,nirodha,gamini) { return buddhism ; }" 
jstree2 = [('function', 'nobletruths', ['dukkha', 'samudaya', 'nirodha', 'gamini'], [('return', ('identifier', 'buddhism'))])] 
print test_parser(jstext2) == jstree2  

# Multiple top-level elemeents, each of which is a var, assignment or 
# expression statement. 
jstext3 = """
var view = right;
var intention = right;
var speech = right;
action = right;
livelihood = right;
effort_right;
mindfulness_right;
concentration_right;
""" 
jstree3 = [('stmt', ('var', 'view', ('identifier', 'right'))), ('stmt', ('var', 'intention', ('identifier', 'right'))), ('stmt', ('var', 'speech', ('identifier', 'right'))), ('stmt', ('assign', 'action', ('identifier', 'right'))), ('stmt', ('assign', 'livelihood', ('identifier', 'right'))), ('stmt', ('exp', ('identifier', 'effort_right'))), ('stmt', ('exp', ('identifier', 'mindfulness_right'))), ('stmt', ('exp', ('identifier', 'concentration_right')))]

print test_parser(jstext3) == jstree3  
# if-then and if-then-else and compound statements. 
jstext4 = """
if cherry {
    orchard;
    if uncle_vanya {
        anton ;
        chekov ;
    } else {} ;
    nineteen_oh_four;
};""" 

jstree4 = [('stmt', ('if-then', ('identifier', 'cherry'), [('exp', ('identifier', 'orchard')), ('if-then-else', ('identifier', 'uncle_vanya'), [('exp', ('identifier', 'anton')), ('exp', ('identifier', 'chekov'))], []), ('exp', ('identifier', 'nineteen_oh_four'))]))] 
print test_parser(jstext4) == jstree4
