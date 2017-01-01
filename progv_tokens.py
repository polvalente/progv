import ply.lex as lex

tokens = (
        'COMMA',
        'DIVIDE',
        'ELSE',
        'EQUAL',
        'FALSE',
        'FUNCTION',
        'GE',
        'GT',
        'IDENTIFIER',
        'IF',
        'LBRACE',
        'LE',
        'LOGICAL_AND',
        'LOGICAL_OR',
        'LOGICAL_EQUAL',
        'LOGICAL_NOT',
        'LPAREN',
        'LT',
        'MINUS',
        'NUMBER',
        'PLUS',
        'POWER',
        'RBRACE',
        'RETURN',
        'RPAREN',
        'SEMICOLON',
        'STRING',
        'TIMES',
        'TRUE',
        'VAR')

states = (('comment','exclusive'),('linecomment','exclusive'))

def t_linecomment(token):
    r'//'
    token.lexer.begin('linecomment')

def t_linecomment_newline(token):
    r'\n'
    token.lexer.lineno += 1
    token.lexer.begin('INITIAL')

def t_comment(token):
    r'/\*'
    token.lexer.begin('comment')

def t_comment_end(token):
    r'\*/'
    token.lexer.lineno += token.value.count('\n')
    token.lexer.begin('INITIAL')

def t_comment_error(token):
    token.lexer.skip(1)

def t_linecomment_error(token):
    token.lexer.skip(1)

t_comment_ignore = ''
t_linecomment_ignore = ''


def t_COMMA(token):
    r','
    return token

def t_DIVIDE(token):
    r'/'
    return token

def t_ELSE(token):
    r'else'
    return token

def t_LOGICAL_EQUAL(token):
    r'\=\='
    return token

def t_EQUAL(token):
    r'\='
    return token

def t_FALSE(token):
    r'false'
    return token

def t_FUNCTION(token):
    r'function'
    return token

def t_GE(token):
    r'>='
    return token

def t_GT(token):
    r'>'
    return token

def t_IF(token):
    r'if'
    return token

def t_LBRACE(token):
    r'{'
    return token

def t_LE(token):
    r'<='
    return token

def t_LOGICAL_AND(token):
    r'&&'
    return token

def t_LOGICAL_OR(token):
    r'\|\|'
    return token


def t_LOGICAL_NOT(token):
    r'\!'
    return token

def t_LPAREN(token):
    r"\("
    return token

def t_LT(token):
    r'<'
    return token

def t_MINUS(token):
    r'\-'
    return token

def t_PLUS(token):
    r'\+'
    return token

def t_POWER(token):
    r'\*\*'
    return token

def t_RBRACE(token):
    r'}'
    return token

def t_RETURN(token):
    r'return'
    return token

def t_RPAREN(token):
    r"\)"
    return token

def t_SEMICOLON(token):
    r';'
    return token

def t_TIMES(token):
    r'\*'
    return token

def t_TRUE(token):
    r'true'
    return token

def t_VAR(token):
    r'var'
    return token

def t_STRING(token):
    r'"(?:[\\\\\.]|[^\\])*"'
    token.value = token.value[1:-1]
    return token

def t_NUMBER(token):
    r'-?[0-9]+\.?[0-9]*'
    token.value = float(token.value)
    return token

t_IDENTIFIER = r'[a-zA-Z]+[_a-zA-Z0-9]*'


t_ignore = ' \t\v\r'

def t_newline(token):
    r'\n'
    token.lexer.lineno += 1

def t_error(token):
    print 'PROGV Lexer: Illegal Character ' + token.value
    token.lexer.skip(1)
