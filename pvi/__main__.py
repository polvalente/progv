import ply.lex as lex
import ply.yacc as yacc
import modules.tokens as tokens
import modules.grammar as grammar
import src.interpreter as interpreter
from sys import argv

lexer = lex.lex(module=tokens)
parser = yacc.yacc(module=grammar,tabmodule="progv_parsetab")
if len(argv) > 1:
    ast = parser.parse(''.join(open(argv[1],'r').readlines()), lexer=lexer)
    interpreter.interpret(ast) 
else:
    print 'No input file'
    print 'Usage: '+argv[0]+' <input filename>'
