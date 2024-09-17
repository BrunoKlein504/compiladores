from ap1_final import Analisador_Lexico, leia_arquivo, main

class Analisador_Sintatico:
    def __init__(self):
        self.lexico = Analisador_Lexico(leia_arquivo())
        self.buf = self.lexico.buffer
        self.i = self.lexico.i

    def consome(self):
        lookahead = self.lexico.proximo_atomo()
    
    def programa():
        ...

    def bloco():
        ...

    def decla_de_var():
        ...

    def declaracao():
        ...

    def lista_de_identi():
        ...

    def tipo():
        ...

    def comando_composto():
        ...

    def comando():
        ...

    def atribuicao():
        ...

    def comando_if():
        ...

    def comando_while():
        ...
    
    def comando_entrada():
        ...

    def comando_saida():
        ...

    def expressao():
        ...
    
    def expressao_simples():
        ...

    def operador_adicao():
        ...

    def operador_relacional():
        ...

    def operador_multiplicacao():
        ...

    def termo():
        ...
    
    def fator():
        ...

analisador_sint = Analisador_Sintatico()