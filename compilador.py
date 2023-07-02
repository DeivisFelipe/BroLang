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
result = parser.parse(codigo, lexer=lexer, debug=False,tracking=True)

if result:
    print("Compilado com sucesso!")
    print("Resultado:")
    print(result)

    # Cria o arquivo de saída
    with open('saida.c', 'w') as file:
        file.write(str(result))

else:
    print("Erro de compilacao")
