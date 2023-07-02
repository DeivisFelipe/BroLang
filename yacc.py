# Esse código contem o sintático e o semântico

# Importa o yacc
import ply.yacc as yacc

# Tokens
from lex import tokens

# Verifica se teve inicio do programa
inicio = False
mostrou_erro = False
tab = 1

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

# Declaração inicial
start = 'programa'

def p_programa(p):
    "programa : NULO PRINCIPAL '(' ')' '{' codigo '}'"
    p[0] = "int main() {\n" + p[6] + "\n}"

# Código dentro da função principal
def p_codigo(p):
    "codigo : dec_variavel comando"
    p[0] = p[1] + p[2]

# Declaração de variáveis, estrutura básica: tipo nome_variavel; tipo nome_variavel; ...
def p_dec_variavel(p):
    '''dec_variavel : salva_variavel ';' dec_variavel
                    | vazio'''
    if len(p) > 2:
        p[0] = "\t" + p[1] + p[2] + "\n" + p[3]
    else:
        p[0] = ""

# Salva as variáveis na tabela de símbolos
def p_salva_variavel(p):
    '''salva_variavel : tipo lista_nomes'''
    p[0] = p[1] + " " + p[2]
    # Salva as variáveis
    for nome in p[2].split(", "):
        # Verifica se a variável já foi declarada
        if nome in variaveis:
            print("Erro: Variavel", nome, "ja declarada, linha: ", p.lineno(1))
            exit(1)
        # Se não foi, salva
        variaveis[nome] = (p[1], 0)

# Lista de nomes
def p_lista_nomes(p):
    "lista_nomes : NAME lista_n"
    p[0] = str(p[1]) + str(p[2])

# Continuação da lista de nomes
def p_lista_n(p):
    '''lista_n : ',' NAME lista_n
               | vazio'''
    if len(p) > 2:
        p[0] = ", " + str(p[2]) + str(p[3])
    else:
        p[0] = ""

# Erro na declaração de variável
def p_salva_variavel_erro(p):
    "dec_variavel : tipo error ';'"
    print("Deve vir uma varivel depois do tipo:", p[1], "\nToken recebido:", p[2], "linha: ", p.lineno(2))
    mostrou_error = True
    exit(1)
    
# Tipos de variáveis
def p_tipo(p):
    ''' tipo : INTEIRO 
             | REAL 
             | CHAR '''
    if p[1] == 'inteiro':
        p[0] = "int"
    elif p[1] == 'real':
        p[0] = "float"
    elif p[1] == 'char':
        p[0] = "char"

# Comandos
def p_comando(p):
    ''' comando : comando_se comando
                | comando_enquanto comando
                | comando_atribuicao comando
                | comando_entrada comando
                | comando_saida comando
                | vazio
    '''
    global tab
    tabs = '\t' * (tab)
    if(len(p) > 2):
        if (p[2] == ""):
            p[0] = tabs + str(p[1])
        else:
            p[0] = tabs + str(p[1]) + "\n" + str(p[2])
    else:
        p[0] = ""

def p_comando_se(p):
    "comando_se : aumenta_tab SE '(' expressao ')' '{' comando '}' diminui_tab senao"
    global tab
    tabs = '\t' * (tab)
    p[0] = "if(" + str(p[4]['valor']) + ") {\n" + str(p[7]) + "\n" + tabs + "}" + str(p[10])

def p_senao(p):
    ''' senao : SENAO '{' comando '}'
              | vazio '''
    if len(p) > 2:
        p[0] = "else {\n" + str(p[3]) + "\n}"
    else:
        p[0] = ""

def p_comando_enquanto(p):
    "comando_enquanto : aumenta_tab  ENQUANTO '(' expressao ')' '{' comando '}' diminui_tab"
    global tab
    tabs = '\t' * (tab)
    p[0] = "while(" + str(p[4]['valor']) + ") {\n" + str(p[7]) + "\n" + tabs + "}"

# Atribuição de variável
def p_comando_atribuicao(p):
    "comando_atribuicao : name '=' expressao ';'"
    p[0] = str(p[1]['nome']) + " = " + str(p[3]['valor']) + ";"

    tipo = type(p[3]).__name__
    if (isinstance(p[3], dict)):
        tipo = p[3]['tipo']

    if tipo == 'str':
        tipo = 'char'

    # Verifica se o tipo da variável é compatível com o valor atribuído
    if p[1]['tipo'] != tipo:
        print("Erro: Tipo incompativel: esperado:", p[1]['tipo'], ", recebido:", tipo, "linha: ", p.lineno(1))
        exit(1)
    # Se for compatível, seta o valor da variável
    variaveis[p[1]['nome']] = (p[1]['tipo'], p[3]['valor'])

def p_comando_entrada(p):
    "comando_entrada : LER '(' NAME ')' ';'"
    # Verifica se a variável já foi declarada
    if p[3] not in variaveis:
        print("Erro: Variavel", p[3], "nao declarada, linha: ", p.lineno(3))
        exit(1)
    # Verifica se o tipo da variável é compatível com o valor atribuído
    if variaveis[p[3]][0] == 'int':
        p[0] = "scanf(\"%d\", &" + str(p[3]) + ");"
    elif variaveis[p[3]][0] == 'float':
        p[0] = "scanf(\"%f\", &" + str(p[3]) + ");"
    elif variaveis[p[3]][0] == 'char':
        p[0] = "scanf(\"%s\", &" + str(p[3]) + ");"
    else :
        print("Erro: Tipo incompativel: ", p)
        #exit(1)

def p_comando_saida(p):
    '''comando_saida : ESCREVER '(' CHAR ')' ';'
                     | ESCREVER '(' expressao ')' ';' 
                     | ESCREVER '(' NAME ')' ';' '''
    if p[3] == 'CHAR':
        p[0] = "printf(\"%s\", " + str(p[3]) + ");"
    else:
        p[0] = "printf(\"%d\", " + str(p[3]) + ");"


# Expressões
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
                  | INTEIRO
                  | REAL
                  | CHAR
                  | name '''
    if(len(p) > 2):
        if(p[1] == '('):
            p[0] = { 'tipo': p[2]['tipo'], 'valor': '(' + str(p[2]['valor']) + ')'}
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
                p[0] = { 'tipo': tipo1, 'valor': str(p[1]['valor']) + " " + str(p[2]) + " " + str(p[3]['valor']) }
            # as duas expressoes são de tipos diferentes
            else:
                print("Erro: Tipos incompativeis: " + tipo1 + " " + str(p[2]) + " " + tipo2)
                exit(1)
    else:
        # Verifica se o p[1] é um dicionário
        if (isinstance(p[1], dict)):
            p[0] = p[1]
        else:
            p[0] = { 'tipo': type(p[1]).__name__, 'valor': p[1] }

# Expressão com nome
def p_name(p):
    "name : NAME"
    if p[1] not in variaveis:
        print("Erro: Variavel", p[1], "nao declarada")
        exit(1)
    p[0] = { 'tipo': variaveis[p[1]][0], 'valor': variaveis[p[1]][1], 'nome': p[1] }

def p_expressao_negativa(p):
    "expressao : '-' expressao %prec UMINUS"
    p[0] = -p[2]

# Aumenta o tab
def p_aumenta_tab(p):
    "aumenta_tab :"
    global tab
    tab += 1

# Diminui o tab
def p_diminui_tab(p):
    "diminui_tab :"
    global tab
    tab -= 1


# Declaração vazia
def p_vazio(p):
    'vazio :'
    pass

def p_error(p):
    if(not mostrou_erro):
        print("Erro de sintaxe token:", p, "linha: ", p.lineno)


parser = yacc.yacc()