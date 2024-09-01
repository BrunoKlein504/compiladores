from typing import NamedTuple
from typing import Union

import sys

ERRO = 0
IDENTIFICADOR = 1
NUM_INT = 2
NUM_REAL = 3
EOS = 4
RELOP = 5    # operador relacional
ADDOP = 6
MULOP = 7

IF = 8
THEN = 9
ELSE = 10
WHILE = 11
DO  = 12
BEGIN = 13
END = 14


# operadores relacionais
LE = 1000               # menor igual (<=)
NE = 1001               # diferente   (<>)
LT = 1002               # menor que   (<)
GE = 1003               # maior igual (>=)
GT = 1004               # maior que   (>)
EQ = 1005               # igual       (=)

# operador de adição
SOMA = 1006
SUBT = 1007
DIVI = 1008
MULT = 1009



atomo_msg = ['ERRO', 'IDENTIFICADOR', 'NUM_INT', 'NUM_REAL', 'EOS', 'RELOP   ', 
'ADDOP', 'MULOP','IF', 'THEN', 'ELSE', 'WHILE  ', 'DO   ','BEGIN', 'END']

palavras_reservadas = {'if': IF, 'then': THEN, 'else': ELSE, 'while': WHILE, 'do': DO, 
'begin': BEGIN, 'end': END}

class Atomo(NamedTuple):
    tipo : int
    lexema : str
    valor : Union [int, float]
    operador : int          # LE, NE, LT, GE, GT, EQ
    linha : int

class Analisador_Lexico:
    def __init__(self, buffer):
        self.linha = 1
        self.buffer = buffer + '\0'
        self.i = 0
    
    def proximo_char(self):
        c = self.buffer[self.i]
        self.i += 1
        return c

    def retrair(self):
        self.i -= 1

    def proximo_atomo(self):
        atomo = Atomo(ERRO, '', 0, 0, self.linha)
        c = self.proximo_char()
        while c in [' ', '\n', '\t', '\0']:
            if c == '\n':
                self.linha += 1
            if c == '\0':
                return Atomo(EOS, '', 0, 0, self.linha)
            c = self.proximo_char()
        if c.isalpha() or c == '_':
            return self.tratar_identificador(c)
        elif c.isdigit():
            return self.tratar_numeros(c)
        elif c == '<':
            return self.tratar_operador_menor(c)
        elif c == '=':
            return Atomo(RELOP, '=', 0, EQ, self.linha)
        elif c == '+':
            return Atomo(ADDOP, '+', 0, SOMA, self.linha)

        return atomo        

    def tratar_operador_menor(self, c: str):
        lexema = c
        c = self.proximo_char()
        estado = 1
        while True:
            if estado == 1:
                if c == '=':
                    lexema += c
                    estado = 2
                elif c == '>':
                    lexema += c
                    estado = 3
                else:
                    estado = 4
            elif estado == 2:
                return Atomo(RELOP, lexema, 0, LE, self.linha)
            elif estado == 3:
                return Atomo(RELOP, lexema, 0, NE, self.linha)
            elif estado == 4:
                self.retrair()
                return Atomo(RELOP, lexema, 0, LT, self.linha)

            


    def tratar_numeros(self, c: str):
        lexema = c
        c = self.proximo_char()
        estado = 1
        while True:
            if estado == 1:
                if c.isdigit():
                    lexema += c
                    estado = 1
                    c = self.proximo_char()
                elif c == '.':
                    lexema += c
                    estado = 3
                    c = self.proximo_char()                    
                elif c.isalpha():
                    return Atomo(ERRO, '', 0, 0, self.linha)    
                else:
                    estado = 2
            elif estado == 2:
                self.retrair()
                return Atomo(NUM_INT, lexema, int(lexema), 0, self.linha)
            elif estado == 3:
                if c.isdigit():
                    lexema += c
                    estado = 4
                    c = self.proximo_char()
                else:
                    return Atomo(ERRO, '', 0, 0, self.linha)
            elif estado == 4:
                if c.isdigit():
                    lexema += c
                    estado = 4
                    c = self.proximo_char()
                else:
                    estado = 5
            elif estado == 5:
                self.retrair()
                return Atomo(NUM_REAL, lexema, float(lexema), 0, self.linha)


    def tratar_identificador(self, c: str):
        lexema = c
        c = self.proximo_char()
        estado = 1
        while True:
            if estado == 1:
                if c.isalpha() or c.isdigit() or c == '_':
                    lexema += c
                    estado = 1
                    c = self.proximo_char()
                else:
                    estado = 2
            elif estado == 2:
                self.retrair()
                if lexema.lower() in palavras_reservadas:
                    return Atomo(palavras_reservadas[lexema.lower()], lexema, 0,0,self.linha)
                else:
                    return Atomo(IDENTIFICADOR, lexema, 0, 0, self.linha)



def leia_arquivo():
    if len(sys.argv) > 1:
        nome_arq = sys.argv[1]
    else:
        nome_arq = 'teste2.txt'

    arq = open(nome_arq)
    buffer = arq.read()
    arq.close()

    return buffer    


def main():
    buffer = leia_arquivo()
    lex = Analisador_Lexico(buffer)
    atomo = lex.proximo_atomo()
    while (atomo.tipo != EOS and atomo.tipo != ERRO):
        print(f'Linha: {atomo.linha}', end='')
        print(f' - atomo: {atomo_msg[atomo.tipo]}', end='')
        print(f'\t lexema: {atomo.lexema}')
        atomo = lex.proximo_atomo()

    print(f'Linha: {atomo.linha}', end='')
    print(f' - atomo: {atomo_msg[atomo.tipo]}', end='')
    

main()
