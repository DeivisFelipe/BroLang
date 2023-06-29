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
    'entao': 'ENTAO',
}

# Lista de nomes de tokens
tokens = [
    'EPAREN',
    'DPAREN',
    'ECHAVES',
    'DCHAVES',
    'PVIRGULA',
    'VIRGULA',

    # Variáveis
    'NAME',

    # Operadores
    'SOMA',
    'SUBTRACAO',
    'MULTIPLICACAO',
    'DIVISAO',
    'IGUAL',
    'MAIOR',
    'MENOR',
    'MAIORIGUAL',
    'MENORIGUAL',
    'DIFERENTE',
    'ATRIBUICAO',
    'ELOGICO',
    'OULOGICO',
    'NEGACAO',
] + list(palavras_reservadas.values())

# Expressões regulares para tokens simples
t_EPAREN = r'\('
t_DPAREN = r'\)'
t_ECHAVES = r'\{'
t_DCHAVES = r'\}'
t_PVIRGULA = r';'
t_VIRGULA = r','
t_SOMA = r'\+'
t_SUBTRACAO = r'-'
t_MULTIPLICACAO = r'\*'
t_DIVISAO = r'/'
t_IGUAL = r'=='
t_MAIOR = r'>'
t_MENOR = r'<'
t_MAIORIGUAL = r'>='
t_MENORIGUAL = r'<='
t_DIFERENTE = r'!='
t_ATRIBUICAO = r'='
t_ELOGICO = r'&&'
t_OULOGICO = r'\|\|'
t_NEGACAO = r'!'
t_ignore = ' \t'

# Expressões regulares com ações
def t_REAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTEIRO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CHAR(t):
    r'\"[\w|\d|\s|\t|\n]*\"'
    t.value = str(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    # Verifica se é uma palavra reservada, se for seta o tipo como a palavra reservada, se não, seta como NAME
    t.type = palavras_reservadas.get(t.value, 'NAME')
    return t

# Comentários
def t_COMENTARIO(t):
    r'(/\*(.|\n)*?\*/)|(//.*)'
    pass

# contato de linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Erro
def t_error(t):
    print("Caractere ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

# Constrói o lexer
lexer = lex.lex()