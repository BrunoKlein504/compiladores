# CARACTERES DELIMITADORES:
#   Regex -> (\s|\n|\t|\r)*

# COMENTÀRIOS:
#   Regex para comentário de uma linha -> '(([//]{2})(\s|\S )*\n)'
#   Regex para comentário de múltiplas linhas -> '(\(\*(\S|\s)*\*\))'

# INDENTIFICADORES:
#   Regex para o átomo <letra> -> '([a-zA-Z]|[_])+ == (\w)'
#   Regex para o átomo <digito> -> '(\d)'
#   Regex para o átomo <identificador> -> (<letra>(<letra>|<digito>)*) =='(A-Za-z)|[_]+(\w)*'
#   Não pode ter mais de 20 caracteres "not (len(lexema) <= 20) -> raise(LexemaSizeError)"

# Números:
#   Regex para o átomo <digito> -> (\d)
#   Regex para o átomo <numero> -> (<digito>+) == ('\d+')


"""
Na próxima versão, irei polir este módulo com mais cautela!

#TODO
    Melhorar os tratadores;
    Melhorar o leia_aquivo() deixando menos hard coded (Talvez usando Manager Context);
    Implementar REGEX.
"""

from typing import NamedTuple
import sys
from AnalisadorExceptions import LexicoError
from pathlib import Path

#Átomos Mensagens
ERRO = 0
IDENTIFICADOR = 1
# NUM_INT = 2
NUM = 2
EOS = 4
RELOP = 5    # operador relacional  (< | <= | = | <> | > | >=)
ADDOP = 6    # operador de adição  (+ | - | or -> boolean)
MULOP = 7    # operador de multiplicação  (* | / | div | mod | and -> boolean)

# Palavras Reservadas
IF = 8
THEN = 9
ELSE = 10
WHILE = 11
DO  = 12
BEGIN = 13
END = 14
BOOLEAN = 15
FALSE = 16
TRUE = 17
INTEGER = 18
MOD = 19
DIV = 20
PROGRAM = 21
READ = 22
NOT = 23
VAR = 24
PONTO_VIRGUL = 25
ATRIB = 26
DOIS_PONTOS = 27
WRITE = 28
ABRE_PARENT = 29
FECHA_PARENT = 30
VIRGULA = 31
AND = 32
PONTO = 33
OR = 34


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

#terminal
PV = 1010

atomo_msg = ['ERRO', 'IDENTIFICADOR', 'NUM', 'NUM_REAL', 'EOS', 'RELOP', 
'ADDOP', 'MULOP','IF', 'THEN', 'ELSE', 'WHILE  ', 'DO   ','BEGIN', 'END',
'BOOLEAN', 'FALSE', 'TRUE', 'INTEGER', 'MOD', 'DIV', 'PROGRAM', 'READ', 'NOT', 'VAR', 'PONTO_VIRGUL', 'ATRIB', 
"DOIS_PONTOS", "WRITE", "ABRE_PARENT", "FECHA_PARENT", "VIRGULA", 'AND', 'PONTO', 'OR']

palavras_reservadas = {'if': IF, 'then': THEN, 'else': ELSE, 'while': WHILE, 'do': DO, 
'begin': BEGIN, 'end': END, 'boolean': BOOLEAN, 'false': FALSE,
 'true': TRUE, 'integer': INTEGER, 'mod': MOD,
   'div': DIV, 'program': PROGRAM, 'read': READ, 'not': NOT, 'var': VAR,'write': WRITE,
     "abre_parenteses":ABRE_PARENT, "fecha_parenteses": FECHA_PARENT,'and': AND,'or': OR}



class Atomo(NamedTuple):
    tipo : int
    lexema : str
    valor : int
    operador : int          # LE, NE, LT, GE, GT, EQ
    linha : int

class AnalisadorLexico:
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
        while c in [' ', '\n', '\t', '\0', '\r']:
            if c == '\n':
                self.linha += 1
            if c == '\0':
                return Atomo(EOS, '', 0, 0, self.linha)
            c = self.proximo_char()
        if c.isalpha() or c == '_' or c == '(' or c == ')' or c == ',' or c == ';' or c == '.':
            return self.tratar_identificador(c)
        elif c.isdigit():
            return self.tratar_numeros(c)
        elif c == ':':
            return self.tratar_atribuicao(c)
        elif c == '<':
            return self.tratar_operador_menor(c)
        elif c == '>':
            return self.tratar_operador_maior(c)
        elif c == '=': # ADICIONAR OS RESTANTES VALORES
            return Atomo(RELOP, '=', 0, EQ, self.linha)
        elif c == '+':
            return Atomo(ADDOP, '+', 0, SOMA, self.linha)
        elif c == '-':
            return Atomo(ADDOP, '-', 0, SUBT, self.linha)
        elif c == '*':
            return Atomo(MULOP, '*', 0, MULT, self.linha)
        elif c == '/':
            return Atomo(MULOP, '/', 0, DIVI, self.linha)

        return atomo
    
    def tratar_atribuicao(self, c: str):
        lexema = c
        c = self.proximo_char()
        if c == '=':
            lexema += c
            return Atomo(ATRIB, lexema, 0, 0, self.linha)
        elif c == " ":
            return Atomo(DOIS_PONTOS, lexema, 0, 0, self.linha)
        return Atomo(ERRO, '', 0, 0, self.linha)

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
            

    def tratar_operador_maior(self, c:str):
        #GE Greater or Equal
        #GT Greater Than
        lexema = c
        estado = 1
        c = self.proximo_char()
        while True:
            if estado == 1:
                if c == "=":
                    lexema += c
                    estado = 2
                else:
                    estado = 3

            elif estado == 2:
                return Atomo(RELOP, lexema, 0, GE, self.linha)
            
            elif estado == 3:
                self.retrair()
                return Atomo(RELOP, lexema, 0, GE, self.linha)

            


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

                elif c.isalpha():
                    return Atomo(ERRO, '', 0, 0, self.linha)    
                else:
                    estado = 2
            elif estado == 2:
                self.retrair()
                return Atomo(NUM, lexema, int(lexema), 0, self.linha)

    def tratar_identificador(self, c: str):
        lexema = c
        if c == '(': # Seção de comentários de múltiplas linhas
            c = self.proximo_char()
            if c == '*':
                c = self.proximo_char()
                while c != '*':
                    if c == "\n":
                        self.linha += 1
                    c = self.proximo_char()
                c = self.proximo_char()
                if c == ')':
                    c = self.proximo_char()
                    if c == '\n':
                        self.linha += 1
                    return self.proximo_atomo()
            else:
                c = self.retrair()
                return Atomo(ABRE_PARENT, lexema, 0, 0, self.linha)
        elif c == ')':
            return Atomo(FECHA_PARENT, lexema, 0,0, self.linha)
        elif c == ',':
            return Atomo(VIRGULA, lexema, 0, 0, self.linha)
        elif c == ';':
            return Atomo(PONTO_VIRGUL, lexema, 0, 0, self.linha)
        elif c == '.':
            return Atomo(PONTO, lexema, 0, 0, self.linha)
        elif c == '/': # SEÇÃO DE COMENTÁRIOS
            c = self.proximo_char()
            if c == '/':
                while c != "\n":
                    c = self.proximo_char()
                self.linha += 1
                return self.proximo_atomo()
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
                elif len(lexema) >= 20:
                    raise LexicoError(f'Identificador [{lexema} ] excedeu 20 caractares na linha {self.linha}')
                else:
                    return Atomo(IDENTIFICADOR, lexema, 0, 0, self.linha)



def leia_arquivo():
    if len(sys.argv) > 1:
        nome_arq = sys.argv[1]
    else:
        # path = Path(__file__).parent / 'pascal_example.pas'
        path = Path(__file__).parent / 'pascal2.pas'
        nome_arq = str(path)

    arq = open(nome_arq)
    buffer = arq.read()
    arq.close()

    return buffer    


# def main():
#     try:
#         buffer = leia_arquivo()
#         lex = AnalisadorLexico(buffer)
#         atomo = lex.proximo_atomo()
#         while (atomo.tipo != EOS and atomo.tipo != ERRO):
#             print(f'Linha: {atomo.linha}', end='')
#             print(f' - atomo: {atomo_msg[atomo.tipo]}', end='') # Indexação
#             if atomo.valor > 0:
#                 print(f'\t lexema: {atomo.lexema}', end='')
#                 print(f'    -    valor:{atomo.valor}')
#             else:
#                 print(f'\t lexema: {atomo.lexema}')
#             atomo = lex.proximo_atomo()

#         print(f'Linha: {atomo.linha}', end='')
#         print(f' - atomo: {atomo_msg[atomo.tipo]}', end='')
#     except Exception as e:
#         print(e)
# if __name__ == '__main__':
#     main()
