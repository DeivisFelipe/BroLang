# Esse arquivo tem as funções que interpretam o código	

# Clone as variáveis
variaveis = {}

# Retorna as variáveis
def getVariaveis():
    return variaveis

# Seta as variáveis
def setVariaveis(variaveis_yacc):
    global variaveis
    variaveis = variaveis_yacc

# Printa variáveis
def printaVariaveis():
    for variavel in variaveis:
        print(variavel, variaveis[variavel])

# Executa conjunto de comandos
def executaComandos(comandos):
    comando = comandos
    if comando == None:
        return
    printaComando(comando[0])
    avaliaComando(comando[0])
    repetir = True if comando[1] != None else False
    while repetir:
        comando = comando[1]
        printaComando(comando[0])
        avaliaComando(comando[0])
        repetir = True if comando[1] != None else False

# Avalia a comando
def avaliaComando(expressao):
    global variaveis
    if(expressao['comando_tipo'] == 'binaria'):
        if expressao['operador'] == "+":
            return avaliaComando(expressao['op1']) + avaliaComando(expressao['op2'])
        elif expressao['operador'] == "-":
            return avaliaComando(expressao['op1']) - avaliaComando(expressao['op2'])
        elif expressao['operador'] == "*":
            return avaliaComando(expressao['op1']) * avaliaComando(expressao['op2'])
        elif expressao['operador'] == "/":
            return avaliaComando(expressao['op1']) / avaliaComando(expressao['op2'])
        elif expressao['operador'] == ">":
            return 1 if avaliaComando(expressao['op1']) > avaliaComando(expressao['op2']) else 0
        elif expressao['operador'] == "<":
            return 1 if avaliaComando(expressao['op1']) < avaliaComando(expressao['op2']) else 0
        elif expressao['operador'] == "==":
            return 1 if avaliaComando(expressao['op1']) == avaliaComando(expressao['op2']) else 0
        elif expressao['operador'] == ">=":
            return 1 if avaliaComando(expressao['op1']) >= avaliaComando(expressao['op2']) else 0
        elif expressao['operador'] == "<=":
            return 1 if avaliaComando(expressao['op1']) <= avaliaComando(expressao['op2']) else 0
        elif expressao['operador'] == "!=":
            return 1 if avaliaComando(expressao['op1']) != avaliaComando(expressao['op2']) else 0
        elif expressao['operador'] == "&&":
            return 1 if avaliaComando(expressao['op1']) and avaliaComando(expressao['op2']) else 0
        elif expressao['operador'] == "||":
            return 1 if avaliaComando(expressao['op1']) or avaliaComando(expressao['op2']) else 0
    elif(expressao['comando_tipo'] == 'unaria'):
        if expressao['operador'] == "!":
            return 1 if not avaliaComando(expressao['op1']) else 0
    elif expressao['comando_tipo'] == 'variavel':
        return variaveis[expressao['op1']['nome']]['valor']
    elif expressao['comando_tipo'] == 'negacao':
        return -avaliaComando(expressao['op1'])
    elif expressao['comando_tipo'] == 'atribuicao':
        variaveis[expressao['nome']]['valor'] = avaliaComando(expressao['valor'])
    elif expressao['comando_tipo'] == 'print':
        print("")
        print(">> ", end="")
        if expressao['tipo'] == 'char':
            print(avaliaComando(expressao['valor'])[1:-1])
        elif expressao['tipo'] == 'numero':
            print(avaliaComando(expressao['valor']))
        elif expressao['tipo'] == 'variavel':
            print(avaliaComando(expressao['valor']))
    elif expressao['comando_tipo'] == 'entrada':
        # Se foi, seta o valor da variável
        print("")
        print(">> ", end="")
        valor = input()
        # Verifica se o valor é um número ou uma string
        if valor.isnumeric():
            # Verifica se tem ponto, se tiver, é um float
            valor = int(valor)
        # Se não for, é uma string
        else:
            # Verifica se o valor é um float
            try:
                valor = float(valor)
            except:
                valor = '"' + valor + '"'
        variaveis[expressao['nome']] = { 'tipo': expressao['valor']['tipo'], 'valor': valor, 'nome': expressao['nome']}
    elif expressao['comando_tipo'] == 'se':
        if avaliaComando(expressao['valor']):
            comando = expressao['comando']
        elif expressao['senao'] != None:
            comando = expressao['senao']
        else:
            return
        executaComandos(comando)
    elif expressao['comando_tipo'] == 'enquanto':
        while avaliaComando(expressao['valor']):
            comando = expressao['comando']
            if comando == None:
                break
            executaComandos(comando)
    elif expressao['comando_tipo'] == 'constante':
        return expressao['op1']
    
# Printa a comando
def printaComando(expressao):
    if(expressao['comando_tipo'] == 'binaria'):
        print("( ", end=" ")
        printaComando(expressao['op1'])
        print(expressao['operador'], end=" ")
        printaComando(expressao['op2'])
        print(" )", end=" ")
    elif(expressao['comando_tipo'] == 'unaria'):
        print("( " + expressao['operador'], end=" ")
        printaComando(expressao['op1'])
        print(" )", end=" ")
    elif expressao['comando_tipo'] == 'variavel':
        print("( " + expressao['op1']['nome'], end="")
        print(" )", end=" ")
    elif expressao['comando_tipo'] == 'negacao':
        print("( " + expressao['operador'], end=" ")
        printaComando(expressao['op1'])
        print(" )", end=" ")
    elif expressao['comando_tipo'] == 'atribuicao':
        print("( " + expressao['nome'] + " = ", end=" ")
        printaComando(expressao['valor'])
        print(" )")
    elif expressao['comando_tipo'] == 'print':
        print("print ", end=" ")
        printaComando(expressao['valor'])
    elif expressao['comando_tipo'] == 'entrada':
        print("entrada ", end=" ")
        printaComando(expressao['valor'])
    elif expressao['comando_tipo'] == 'se':
        pass
    elif expressao['comando_tipo'] == 'enquanto':
        pass
    elif expressao['comando_tipo'] == 'constante':
        print(expressao['op1'], end=" ")

# Função muda tipo
def mudaTipo(tipo):
    if tipo == 'int':
        tipo = 'inteiro'
    if tipo == 'float':
        tipo = 'real'
    if tipo == 'str':
        tipo = 'char'
    return tipo
        