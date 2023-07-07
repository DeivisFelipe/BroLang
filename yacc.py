# Esse código contem o sintático e o semântico

# Importa o yacc
import ply.yacc as yacc

# Tokens
from lex import tokens

# Importa o arquivo interpretador
from interpretador import *

# Precedência
precedence = (
    ('left','ELOGICO','OULOGICO'),
    ('left','>','<', 'MAIORIGUAL', 'MENORIGUAL', 'IGUAL', 'DIFERENTE'),
    ('left','+','-'),
    ('left','*','/'),
    ('left', '(' , ')'),
    ('right','UMINUS'),
)

# Variáveis
variaveis = {}
temporarias = {}

# Declaração inicial
start = 'programa'

# Programa  = PRONTO
def p_programa(p):
    "programa : NULO PRINCIPAL '(' ')' '{' codigo '}'"
    p[0] = p[6]
    global variaveis
    setVariaveis(variaveis)
    executaComandos(p[6])
    variaveis = getVariaveis()
    printaVariaveis()

# Código dentro da função principal = PRONTO
def p_codigo(p):
    "codigo : dec_variavel comando"
    p[0] = p[2]


# DECLARAÇÃO DE VARIÁVEIS
# Declaração de variáveis, estrutura básica: tipo nome_variavel; tipo nome_variavel; ... = PRONTO
def p_dec_variavel(p):
    '''dec_variavel : salva_variavel ';' dec_variavel
                    | vazio'''
    pass

# Salva as variáveis na tabela de símbolos = PRONTO
def p_salva_variavel(p):
    '''salva_variavel : tipo lista_nomes'''
    # Salva as variáveis
    for nome in p[2].split(", "):
        # Verifica se a variável já foi declarada
        if nome in variaveis:
            print("Erro: Variavel", nome, "ja declarada, linha: ", p.lineno(1))
            exit(1)
        # Se não foi, salva
        variaveis[nome] = { 'tipo': p[1], 'valor': None, 'nome': nome, 'linha': p.lineno(1)}

# Lista de nomes = PRONTO
def p_lista_nomes(p):
    "lista_nomes : NAME lista_n"
    p[0] = str(p[1]) + str(p[2])

# Continuação da lista de nomes = PRONTO
def p_lista_n(p):
    '''lista_n : ',' NAME lista_n
               | vazio'''
    if len(p) > 2:
        p[0] = ", " + str(p[2]) + str(p[3])
    else:
        p[0] = ""

# Erro na declaração de variável = PRONTO
def p_salva_variavel_erro(p):
    "dec_variavel : tipo error ';'"
    print("Deve vir uma varivel depois do tipo:", p[1], "\nToken recebido:", p[2], "linha: ", p.lineno(2))
    exit(1)
    
# Tipos de variáveis = PRONTO
def p_tipo(p):
    ''' tipo : INTEIRO 
             | REAL 
             | CHAR '''
    p[0] = p[1]


# FINAL DA DECLARAÇÃO DE VARIÁVEIS

# COMANDOS

# Comandos = PRONTO
def p_comando(p):
    ''' comando : comando_se comando
                | comando_enquanto comando
                | comando_atribuicao comando
                | comando_entrada comando
                | comando_saida comando
                | vazio
    '''
    if(len(p) > 2):
        p[0] = (p[1], p[2])
    else:
        p[0] = None

def p_comando_se(p):
    "comando_se : SE '(' expressao ')' '{' comando '}' senao"
    p[0] = { 'tipo': None, 'valor': p[3], 'nome': None, 'comando_tipo': 'se', 'senao': p[8], 'comando': p[6]}

def p_senao(p):
    ''' senao : SENAO '{' comando '}'
              | vazio '''
    if(len(p) > 2):
        p[0] = p[3]
    else:
        p[0] = None

def p_comando_enquanto(p):
    "comando_enquanto : ENQUANTO '(' expressao ')' '{' comando '}'"
    p[0] = { 'tipo': None, 'valor': p[3], 'nome': None, 'comando_tipo': 'enquanto', 'comando': p[6]}

# Atribuição de variável = PRONTO
def p_comando_atribuicao(p):
    "comando_atribuicao : name '=' expressao ';'"
    tipo = type(p[3]).__name__
    if (isinstance(p[3], dict)):
        tipo = p[3]['tipo']

    if tipo == 'str':
        tipo = 'char'
    if tipo == 'int':
        tipo = 'inteiro'
    if tipo == 'float':
        tipo = 'real'

    # Verifica se o tipo da variável é compatível com o valor atribuído
    if p[1]['tipo'] != tipo:
        print("Erro: Tipo incompativel: esperado:", p[1]['tipo'], ", recebido:", tipo, "linha: ", p.lineno(1))
        exit(1)
    # Se for compatível, seta o valor da variável
    #variaveis[p[1]['nome']] = { 'tipo': p[1]['tipo'], 'valor': p[3], 'nome': p[1]['nome']}
    p[0] = { 'tipo': p[1]['tipo'], 'valor': p[3], 'nome': p[1]['nome'], 'comando_tipo': 'atribuicao' }

# Expressões = PRONTO
def p_expressao(p):
    ''' expressao : expressao '+' expressao
                  | expressao '-' expressao
                  | expressao '*' expressao
                  | expressao '/' expressao
                  | expressao '>' expressao
                  | expressao '<' expressao
                  | expressao IGUAL expressao
                  | expressao MAIORIGUAL expressao
                  | expressao MENORIGUAL expressao
                  | expressao DIFERENTE expressao
                  | expressao ELOGICO expressao
                  | expressao OULOGICO expressao
                  | '(' expressao ')'
                  | '!' expressao
                  | INTEIRO
                  | REAL
                  | CHAR
                  | name '''
    if(len(p) == 4):
        if(p[1] == '('):
            p[0] = p[2]
        else:
            tipo1 = type(p[1]).__name__
            tipo2 = type(p[3]).__name__
            # Verifica se os parâmetros são diciários
            if (isinstance(p[1], dict)):
                tipo1 = p[1]['tipo']
            if (isinstance(p[3], dict)):
                tipo2 = p[3]['tipo']

            # as duas expressoes são do mesmo tipo
            if(tipo1 == tipo2):
                p[0] = { 'tipo': tipo1, 'op1': p[1], 'operador': p[2], 'op2': p[3], 'comando_tipo': 'binaria'}
            # as duas expressoes são de tipos diferentes
            else:
                print("Erro: Tipos incompativeis: " + tipo1 + " " + str(p[2]) + " " + tipo2 + " linha: ", p.lineno(1))
                exit(1)
    elif(len(p) == 3):
        if(p[1] == "!"):
            p[0] = { 'tipo': 'inteiro', 'op1': p[2], 'operador': p[1], 'comando_tipo': 'unaria'}
    else:
        # Verifica se o p[1] é um dicionário
        if (isinstance(p[1], dict)):
            p[0] = { 'tipo': p[1]['tipo'], 'op1': p[1], 'operador': None, 'comando_tipo': 'variavel'}
        else:
            p[0] = { 'tipo': mudaTipo(type(p[1]).__name__), 'op1': p[1], 'operador': None, 'comando_tipo': 'constante'}



# Expressão negativa = PRONTO
def p_expressao_negativa(p):
    "expressao : '-' expressao %prec UMINUS"
    p[0] = { 'tipo': p[2]['tipo'], 'op1': p[2], 'operador': p[1], 'comando_tipo': 'negacao'}

# Expressão com nome = PRONTO
def p_name(p):
    "name : NAME"
    if p[1] not in variaveis:
        print("Erro: Variavel", p[1], "nao declarada")
        exit(1)
    p[0] = variaveis[p[1]]

# Função de leitura = PRONTO
def p_comando_entrada(p):
    "comando_entrada : LER '(' NAME ')' ';'"
    # Verifica se a variável já foi declarada
    if p[3] not in variaveis:
        print("Erro: Variavel", p[3], "nao declarada, linha: ", p.lineno(1))
        exit(1)
    valor = { 'tipo': variaveis[p[3]]['tipo'], 'op1': variaveis[p[3]], 'operador': None, 'comando_tipo': 'variavel'}
    p[0] = { 'tipo': None, 'valor': valor, 'nome': p[3], 'comando_tipo': 'entrada'}

# Função de escrita = PRONTO
def p_comando_saida(p):
    '''comando_saida : ESCREVER '(' CHAR ')' ';'
                     | ESCREVER '(' expressao ')' ';' 
                     | ESCREVER '(' name ')' ';' '''
    if not isinstance(p[3], dict):
        valor = { 'tipo': type(p[3]).__name__, 'op1': p[3], 'operador': None, 'comando_tipo': 'constante'}
        # Verifica se o tipo do valor
        if type(p[3]).__name__ == 'str':
            # Tira as aspas da string
            p[0] = { 'tipo': 'char', 'valor': valor, 'nome': None, 'comando_tipo': 'print'}
        else:
            p[0] = { 'tipo': 'numero', 'valor': valor, 'nome': None, 'comando_tipo': 'print'}
    else:
        # Verifica se o p[3] tem o atributo 'nome', se tiver, é uma variável
        if 'nome' in p[3]:
            valor = { 'tipo': p[3]['tipo'], 'op1': p[3], 'operador': None, 'comando_tipo': 'variavel'}
        else:
            valor = p[3]
        p[0] = { 'tipo': 'variavel', 'valor': valor, 'nome': None, 'comando_tipo': 'print'}

# FINAL DOS COMANDOS

# FUNÇÕES AUXILIARES

# Declaração vazia = PRONTO
def p_vazio(p):
    'vazio :'
    pass

# Função para mostrar o erro = PRONTO
def p_error(p):
    print("Erro de sintaxe token:", p, "linha: ", p.lineno)


parser = yacc.yacc()