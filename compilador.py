# Esse é o programa base do BroLang

with open('codigo.bro', 'r') as file:
    codigo = file.read()

# Printa o código
print(codigo)

# Importa o lexer criado
from lex import lexer

# Seta o input
lexer.input(codigo)

# Pega todos os tokens
for tok in lexer:
    print(tok)