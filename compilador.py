# Esse é o programa base do BroLang

arquivo = 'teste.bro'
with open(arquivo, 'r') as file:
    codigo = file.read()

# Importa o lexer criado
from lex import lexer

# Seta o input
lexer.input(codigo)

# Importa o yacc criado
from yacc import parser

# Executa o yacc
parser.parse(codigo, lexer=lexer, debug=False,tracking=True)
