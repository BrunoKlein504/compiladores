# from ap1_final import Analisador_Lexico, leia_arquivo, main
import ap1_final as AL

# Usarei While em casos de cadeias a*
# Usarei if aninhado em casos de cadeias b| ε 

class Analisador_Sintatico:
    def __init__(self):
        self.lexico = AL.Analisador_Lexico(AL.leia_arquivo())
        self.lookahead = self.lexico.proximo_atomo()

    def init_sintatico(self):
       self.programa()
       self.consome()


    # def consome(self, atomo):
    #     if atomo != self.lookahead.tipo:
    #         raise Exception(f'Linha: {self.lookahead.linha} - Atomo: {AL.atomo_msg[self.lookahead.tipo]} \tLexema: {self.lookahead.lexema}')
    #     elif atomo != AL.EOS:
    #         self.lookahead = self.lexico.proximo_atomo()

    def consome(self, atomo=None):
        if atomo is not None and atomo != self.lookahead.tipo:
            raise Exception(f'Linha: {self.lookahead.linha} - Atomo: {AL.atomo_msg[self.lookahead.tipo]} \tLexema: {self.lookahead.lexema}')
        elif self.lookahead.tipo != AL.EOS:
            self.lookahead = self.lexico.proximo_atomo()



    
    def programa(self):
        # <programa> ::= program identificador [( <lista de identificadores> )] ; <bloco>.
        if self.lookahead.tipo == AL.PROGRAM:
            self.consome(AL.PROGRAM)
            self.consome(AL.IDENTIFICADOR)

            if self.lookahead.tipo == AL.ABRE_PARENT:
                self.consome(AL.ABRE_PARENT)
                self.lista_de_identi()
                self.consome(AL.FECHA_PARENT)
            
            self.consome(AL.PONTO_VIRGUL)
            self.bloco()
            self.consome(AL.PONTO)
        


    def bloco(self):
        #<bloco> ::= [<declarações de variáveis>] <comando composto>
        if self.lookahead.tipo == AL.VAR:
            self.decla_de_var()
        # self.decla_de_var()
        self.comando_composto()

    # def decla_de_var(self):
    #     #<declarações de variáveis> ::= var <declaração> {; <declaração> };
    #     if self.lookahead.tipo == AL.VAR:
    #         self.consome(AL.VAR)
    #         self.declaracao()
    #         while self.lookahead.tipo == AL.VIRGULA:
    #             self.consome(AL.VIRGULA)
    #             self.declaracao()
    #         self.consome(AL.PONTO_VIRGUL)

    def decla_de_var(self):
    # <declarações de variáveis> ::= var <declaração> { ; <declaração> };
        if self.lookahead.tipo == AL.VAR:
            self.consome(AL.VAR)
            self.declaracao()
            while self.lookahead.tipo == AL.PONTO_VIRGUL:
                self.consome(AL.PONTO_VIRGUL)
                self.declaracao()
            self.consome(AL.PONTO_VIRGUL)

    def declaracao(self):
        #<declaração> ::= <lista de identificadores> : <tipo>
        self.lista_de_identi()
        self.consome(AL.DOIS_PONTOS)
        self.tipo()

    def lista_de_identi(self):
        #<lista de identificadores> ::= identificador { , identificador }
        self.consome(AL.IDENTIFICADOR)
        while self.lookahead.tipo == AL.VIRGULA:
            self.consome(AL.VIRGULA)
            self.consome(AL.IDENTIFICADOR)



    def tipo(self):
        #<tipo> ::= integer | boolean
        if self.lookahead.tipo == AL.INTEGER:
            self.consome(AL.INTEGER)
        
        elif self.lookahead.tipo == AL.BOOLEAN:
            self.consome(AL.BOOLEAN)

    # def comando_composto(self):
    #     #<comando composto> ::= begin <comando> { ; <comando> } end
    #     if self.lookahead.tipo == AL.BEGIN:
    #         self.consome(AL.BEGIN)
    #         self.comando()

    #     while self.lookahead.tipo == AL.PONTO_VIRGUL:
    #         self.consome(AL.PONTO_VIRGUL)
    #         self.comando()

    #     self.consome(AL.END)

    def comando_composto(self):
    # <comando composto> ::= begin <comando> { ; <comando> } end
        if self.lookahead.tipo == AL.BEGIN:
            self.consome(AL.BEGIN)
            self.comando()

        while self.lookahead.tipo == AL.PONTO_VIRGUL:
            self.consome(AL.PONTO_VIRGUL)
            self.comando()

        self.consome(AL.END)


    def comando(self):

        # <comando> ::=

        #     <atribuicao> |
        #     <comando de entrada> |
        #     <comando de saída> |
        #     <comando if> |
        #     <comando while> |
        #     <comando composto>

        if self.lookahead.tipo == AL.IDENTIFICADOR:
            self.atribuicao()
        
        elif self.lookahead.tipo == AL.IF:
            self.comando_if()
        
        elif self.lookahead.tipo == AL.WHILE:
            self.comando_while()

        elif self.lookahead.tipo == AL.READ:
            self.comando_entrada()
        
        elif self.lookahead.tipo == AL.WRITE:
            self.comando_saida()
        
        elif self.lookahead.tipo == AL.BEGIN:
            self.comando_composto()

        

    def atribuicao(self):
        #<atribuição> ::= identificador := <expressao> ;
        self.consome(AL.IDENTIFICADOR)
        self.consome(AL.ATRIB)
        self.expressao()
        self.consome(AL.PONTO_VIRGUL)


    def comando_if(self):
#         <comando if> ::= if <expressao> then <comando>
#                   [else <comando>]
        self.consome(AL.IF)
        self.expressao()
        self.consome(AL.THEN)
        self.comando()

        if self.lookahead.tipo == AL.ELSE:
            self.consome(AL.ELSE)
            self.comando()

    def comando_while(self):
        #<comando while> ::= while <expressao> do <comando>
        self.consome(AL.WHILE)
        self.expressao()
        self.consome(AL.DO)
        self.comando()

    
    def comando_entrada(self):
        #<comando de entrada> ::= read ( <lista de identificadores> )
        self.consome(AL.READ)
        self.consome(AL.ABRE_PARENT)
        self.lista_de_identi()
        self.consome(AL.FECHA_PARENT)


    def comando_saida(self):
        # <comando de saida> ::= write ( <expressao> { , <expressao> } )
        self.consome(AL.WRITE)
        self.consome(AL.ABRE_PARENT)
        self.expressao()
        
        while self.lookahead.tipo == AL.VIRGULA:
            self.consome(AL.VIRGULA)
            self.expressao()

        self.consome(AL.FECHA_PARENT)

    def expressao(self):
        # <expressao> ::= <expressao simples> [<operador relacional> <expressao simples>]
        self.expressao_simples()

        # <operador relacional> ::= < | <= | = | <> | > | >=
        if self.lookahead.tipo == AL.RELOP:
            self.consome(AL.RELOP)
            self.expressao_simples()



    
    def expressao_simples(self):
        #<expressao simples> ::= [+ | −] <termo> { <operador de adição> <termo> }
        if self.lookahead.tipo == AL.ADDOP:
            self.consome(AL.ADDOP)
        
        self.termo()

        while self.lookahead.tipo == AL.ADDOP:
            self.consome(AL.ADDOP)
            self.termo()

    # def operador_adicao(self):
    #     ...

    # def operador_relacional(self):
    #     ...

    # def operador_multiplicacao(self):
    #     ...

    def termo(self):
        # <termo> ::= <fator> { <operador de multiplicação> <fator> }
        self.fator()

        while self.lookahead.tipo == AL.MULOP:
            self.consome(AL.MULOP)
            self.fator()
    
    def fator(self):
        # <fator> ::=

        #         identificador |
        #         numero |
        #         ( <expressao> ) |
        #         true |
        #         false |
        #         not <fator>

        if self.lookahead.tipo == AL.IDENTIFICADOR:
            self.consome(AL.IDENTIFICADOR)
        elif self.lookahead.tipo == AL.NUM:
            self.consome(AL.NUM)
        elif self.lookahead.tipo == AL.ABRE_PARENT:
            self.consome(AL.ABRE_PARENT)
            self.expressao()
            self.consome(AL.FECHA_PARENT)
        elif self.lookahead.tipo == AL.TRUE:
            self.consome(AL.TRUE)
        elif self.lookahead.tipo == AL.FALSE:
            self.consome(AL.FALSE)
        elif self.lookahead.tipo == AL.NOT:
            self.consome(AL.NOT)
            self.fator()

# analisador_sint = Analisador_Sintatico()

# atomo = AL.Atomo(AL.EOS, 0, 0, 0, 0)
# print(analisador_sint.buf)

# try:
#     sintatico = Analisador_Sintatico()  # Cria a instância do analisador sintático
#     sintatico.init_sintatico()  # Inicia a análise sintática do programa


#     while sintatico.lookahead.tipo != AL.EOS:  # Continua até o fim do arquivo
#         atomo = sintatico.lookahead
#         print(f"Linha: {atomo.linha} - Atomo: {AL.atomo_msg[atomo.tipo]} \tLexema: {atomo.lexema}")
#         sintatico.consome(atomo.tipo)  # Consome o token atual e avança para o próximo


#     print(f"Linha: {sintatico.lookahead.linha} - Atomo: {AL.atomo_msg[sintatico.lookahead.tipo]}")

# except Exception as e:
#     print(f"Erro: {e}")

try:
    sintatico = Analisador_Sintatico()
    sintatico.init_sintatico()  

    atomo = sintatico.lookahead
    print(f"Linha: {atomo.linha} - Atomo: {AL.atomo_msg[atomo.tipo]} \tLexema: {atomo.lexema}")

except Exception as e:
    print(f"Erro: {e}")
