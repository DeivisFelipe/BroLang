# Esse código contem o sintático e o semântico

# Importa o yacc
import ply.yacc as yacc

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

    #