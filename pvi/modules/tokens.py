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
        'MOD',
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
        'VAR',
        'WHILE')

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

t_COMMA         = r','
t_DIVIDE        = r'/'
t_ELSE          = r'else'
t_LOGICAL_EQUAL = r'\=\='
t_EQUAL         = r'\='
t_FALSE         = r'false'
t_FUNCTION      = r'function'
t_GE            = r'>='
t_GT            = r'>'
t_IF            = r'if'
t_LBRACE        = r'{'
t_LE            = r'<='
t_LOGICAL_AND   = r'&&'
t_LOGICAL_OR    = r'\|\|'
t_LOGICAL_NOT   = r'\!'
t_LPAREN        = r"\("
t_LT            = r'<'
t_MINUS         = r'\-'
t_MOD           = r'\%'
t_PLUS          = r'\+'
t_POWER         = r'\*\*'
t_RBRACE        = r'}'
t_RETURN        = r'return'
t_RPAREN        = r'\)'
t_SEMICOLON     = r';'
t_TIMES         = r'\*'
t_TRUE          = r'true'
t_VAR           = r'var'
t_WHILE         = r'while'

def t_STRING(token):
    r'"(?:[^"\\]|(?:\\.))*"'
    token.value = token.value[1:-1]
    return token

def t_NUMBER(token):
    r'-?[0-9]+\.?[0-9]*'
    token.value = float(token.value)
    return token

reserved = ['function', 'if', 'var', 'return', 'else', 'true', 'false', 'while']

def t_IDENTIFIER(token):
    r'[a-zA-Z]+[_a-zA-Z0-9]*'
    if token.value in reserved:
        token.type = token.value.upper()
    return token


t_ignore = ' \t\v\r'

def t_newline(token):
    r'\n'
    token.lexer.lineno += 1

def t_error(token):
    print 'PROGV Lexer: Illegal Character ' + token.value
    token.lexer.skip(1)