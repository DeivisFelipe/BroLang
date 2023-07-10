import ply.lex as lex

# Palavras reservadas
palavras_reservadas = {
    'nulo': 'NULO',
    'principal': 'PRINCIPAL',
    'inteiro': 'INTEIRO',
    'real': 'REAL',
    'char': 'CHAR',
    'se': 'SE',
    'senao': 'SENAO',
    'enquanto': 'ENQUANTO',
    'ler': 'LER',
    'escrever': 'ESCREVER',
}

# Lista de nomes de tokens
tokens = [
    # Variáveis
    'NAME',

    # Operadores
    'IGUAL',
    'MAIORIGUAL',
    'MENORIGUAL',
    'DIFERENTE',
    'ELOGICO',
    'OULOGICO',
] + list(palavras_reservadas.values())

# Expressões regulares para tokens simples
t_IGUAL = r'=='
t_MAIORIGUAL = r'>='
t_MENORIGUAL = r'<='
t_DIFERENTE = r'!='
t_ELOGICO = r'&&'
t_OULOGICO = r'\|\|'

literals = ['=', '+', '-', '*', '/', '(', ')', '{', '}', ';', ',', '>','<', '=', '!']

# Ignora espaços e tabs
t_ignore = ' \t'

# Expressões regulares com ações
def t_REAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Converte o valor para inteiro
def t_INTEIRO(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Converte o valor para string, aceita qualquer coisa que esteja dentro de aspas duplas
def t_CHAR(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = str(t.value)
    return t

# Verifica se é uma palavra reservada, senão seta como NAME, aceitar _ na variável
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # Verifica se é uma palavra reservada, se for seta o tipo como a palavra reservada, se não, seta como NAME
    t.type = palavras_reservadas.get(t.value, 'NAME')
    return t

# Comentários
def t_COMENTARIO(t):
    r'(/\*(.|\n)*?\*/)|(//.*)'
    pass

# Contato de linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Erro
def t_error(t):
    print("Caractere ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

# Constrói o lexer
lexer = lex.lex()