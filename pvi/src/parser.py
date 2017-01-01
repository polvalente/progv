import ply.yacc as yacc
import ply.lex as lex
import progv_tokens
from progv_tokens import tokens


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
precedence = (
        ('left','LOGICAL_OR'),        
        ('left','LOGICAL_AND'),        
        ('left','LOGICAL_EQUAL'),        
        ('left','LE','LT','GE','GT'),        
        ('left','PLUS','MINUS'),        
        ('left','TIMES','DIVIDE'),
        ('left','POWER'),
        ('right','LOGICAL_NOT')
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
           | exp LT exp
           | exp GT exp
           | exp LE exp
           | exp GE exp
           | exp PLUS exp
           | exp MINUS exp
           | exp TIMES exp
           | exp DIVIDE exp
           | exp POWER exp'''
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

#TESTS





#STATEMENT TESTS
start = 'progv'
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



#EXPRESSION TESTS
start = 'exp'
progv_lexer = lex.lex(module=progv_tokens)
progv_parser = yacc.yacc()

# Simple binary expression. 
jstext5 = "x + 1" 
jstree5 = ('binop', ('identifier', 'x'), '+', ('number', 1.0)) 
print test_parser(jstext5) == jstree5  

# Simple associativity. 
jstext6 = "1 - 2 - 3"   
# means (1-2)-3 
jstree6 = ('binop', ('binop', ('number', 1.0), '-', ('number', 2.0)), '-', ('number', 3.0)) 
print test_parser(jstext6) == jstree6  

# Precedence and associativity. 
jstext7 = "1 + 2 * 3 - 4 / 5 * (6 + 2)"
jstree7 = ('binop', ('binop', ('number', 1.0), '+', ('binop', ('number', 2.0), '*', ('number', 3.0))), '-', ('binop', ('binop', ('number', 4.0), '/', ('number', 5.0)), '*', ('binop', ('number', 6.0), '+', ('number', 2.0)))) 
print test_parser(jstext7) == jstree7  

# String and boolean constants, comparisons. 
jstext8 = ' "hello" == "goodbye" || true && false ' 
jstree8 = ('binop', ('binop', ('string', 'hello'), '==', ('string', 'goodbye')), '||', ('binop', ('true', 'true'), '&&', ('false', 'false')))
print test_parser(jstext8) == jstree8  

# Not, precedence, associativity. 
jstext9 = "! ! tricky || 3 < 5" 
jstree9 = ('binop', ('not', ('not', ('identifier', 'tricky'))), '||', ('binop', ('number', 3.0), '<', ('number', 5.0))) 
print test_parser(jstext9) == jstree9  

# nested function calls! 
jstext10 = "apply(1, 2 + eval(recursion), sqrt(2))" 
jstree10 = ('call', 'apply', [('number', 1.0), ('binop', ('number', 2.0), '+', ('call', 'eval', [('identifier', 'recursion')])), ('call', 'sqrt', [('number', 2.0)])]) 
print test_parser(jstext10) == jstree10  
