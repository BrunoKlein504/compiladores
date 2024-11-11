# from ap1_final import Analisador_Lexico, leia_arquivo, main
import analisador_lexico as AL
from AnalisadorExceptions import SintaticoError, LexicoError, SemanticoError


# Usarei While em casos de cadeias a*
# Usarei if aninhado em casos de cadeias b| ε 
#TODO
#    Fazer uma função printar_compilaçao()

table_symbols = []

class Analisador_Sintatico:
    def __init__(self):
        self.lexico = AL.AnalisadorLexico(AL.leia_arquivo())
        self.lookahead = self.lexico.proximo_atomo()

        global arithmetic_relations_MULT
        arithmetic_relations_MULT = ''

        global arithmetic_relations_ADD
        arithmetic_relations_ADD = ''

        global instructions_relations
        instructions_relations = ''



        global L
        L = 1



    def init_sintatico(self):
       self.programa()

    def consome(self, atomo):
        if atomo != self.lookahead.tipo:
            raise SintaticoError(f'Esperado [{AL.atomo_msg[atomo]} ] encontrado [{AL.atomo_msg[self.lookahead.tipo]} ] na linha {self.lookahead.linha}')
        
        elif self.lookahead.tipo != AL.EOS:
            # if self.lookahead.valor: # Usando truthy caso o valor decimal seja maior que zero
            #     print(f'Linha: {self.lookahead.linha}- Atomo: {AL.atomo_msg[self.lookahead.tipo]:<25}Lexema: {self.lookahead.lexema:<15}valor: {self.lookahead.valor}')
            # else:
            #     print(f'Linha: {self.lookahead.linha}- Atomo: {AL.atomo_msg[self.lookahead.tipo]:<25}Lexema: {self.lookahead.lexema}')
            self.lookahead = self.lexico.proximo_atomo()



    
    def programa(self):
    # <programa> ::= program identificador [( <lista de identificadores> )] ; <bloco>.
        print("INPP")
        self.consome(AL.PROGRAM)
        self.consome(AL.IDENTIFICADOR)

        if self.lookahead.tipo == AL.ABRE_PARENT:
            self.consome(AL.ABRE_PARENT)
            self.lista_de_identi()
            self.consome(AL.FECHA_PARENT)

        self.consome(AL.PONTO_VIRGUL)
        self.bloco()
        print("PARA")
        self.consome(AL.PONTO)


    def bloco(self):
        #<bloco> ::= [<declarações de variáveis>] <comando composto>
        if self.lookahead.tipo == AL.VAR:
            self.decla_de_var()
        
        self.comando_composto()

    def decla_de_var(self):
    # <declarações de variáveis> ::= var <declaração> { ; <declaração> };
        self.consome(AL.VAR)
        self.declaracao()

        while self.lookahead.tipo == AL.PONTO_VIRGUL:
            self.consome(AL.PONTO_VIRGUL)
            if self.lookahead.tipo != AL.BEGIN:
                self.declaracao()
        print(f"AMEM {len(table_symbols)}")


    def declaracao(self):
        #<declaração> ::= <lista de identificadores> : <tipo>
        self.lista_de_identi(declaracao_bool=True)
        self.consome(AL.DOIS_PONTOS)
        self.tipo()

    def lista_de_identi(self, declaracao_bool=False, funcEntrada_bool=False):
        #<lista de identificadores> ::= identificador { , identificador }

        if declaracao_bool:
            table_symbols.append(self.lookahead.lexema)

            if table_symbols.count(self.lookahead.lexema) > 1:
                raise SemanticoError(f"Var <{self.lookahead.lexema}> Já Declarado, Mude o Identificador!")
        
            self.consome(AL.IDENTIFICADOR)
            while self.lookahead.tipo == AL.VIRGULA:
                self.consome(AL.VIRGULA)
                table_symbols.append(self.lookahead.lexema) # Adicionando identificadores
                if table_symbols.count(self.lookahead.lexema) > 1:
                    raise SemanticoError(f"Var <{self.lookahead.lexema}> Já Declarado, Mude o Identificador!")
                self.consome(AL.IDENTIFICADOR)

        elif funcEntrada_bool:

            if self.lookahead.lexema not in table_symbols:
                raise SemanticoError(f"<{self.lookahead.lexema}> Não Foi Declarada!")
            
            print(f"ARMZ {table_symbols.index(self.lookahead.lexema)}")
            self.consome(AL.IDENTIFICADOR)

            while self.lookahead.tipo == AL.VIRGULA:
                self.consome(AL.VIRGULA)
                print("LEIT")
                if self.lookahead.lexema not in table_symbols:
                    raise SemanticoError(f"<{self.lookahead.lexema}> Não Foi Declarada!")
                
                print(f"ARMZ {table_symbols.index(self.lookahead.lexema)}")
                self.consome(AL.IDENTIFICADOR)


    def tipo(self):
        #<tipo> ::= integer | boolean

        if self.lookahead.tipo == AL.INTEGER:
            self.consome(AL.INTEGER)
        
        elif self.lookahead.tipo == AL.BOOLEAN:
            self.consome(AL.BOOLEAN)

    def comando_composto(self):
    # <comando composto> ::= begin <comando> { ; <comando> } end
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
        #<atribuição> ::= identificador := <expressao>

        if self.lookahead.lexema not in table_symbols:
            raise SemanticoError(f"<{self.lookahead.lexema}> Não Foi Declarada!")
        
        endereco = self.lookahead.lexema

        self.consome(AL.IDENTIFICADOR)
        self.consome(AL.ATRIB)
        self.expressao()

        if arithmetic_relations_MULT:
            print(arithmetic_relations_MULT)
        
        if arithmetic_relations_ADD:
            print(arithmetic_relations_ADD)

        print(f"ARMZ {table_symbols.index(endereco)}")

                # if self.lookahead.tipo == AL.PONTO_VIRGUL:
                #     self.consome(AL.PONTO_VIRGUL)

    def comando_if(self):
#         <comando if> ::= if <expressao> then <comando>
#                   [else <comando>]

        global L
        provisory_L = L

        self.consome(AL.IF)
        self.expressao()

        print(f"DSVF L{L}")
        L += 1
        self.consome(AL.THEN)
        self.comando()
        print(f"DSVS L{L}")
        if self.lookahead.tipo == AL.ELSE:
            print(f"L{provisory_L}: NADA")
            self.consome(AL.ELSE)
            self.comando()
        print(f"L{L}: NADA")

    def comando_while(self):
        #<comando while> ::= while <expressao> do <comando>
        global L
        provisory_L = L

        print(f"L{L}: NADA")
        #FAZER UMA VAR nova
        L += 1



        self.consome(AL.WHILE)
        self.expressao()
        self.consome(AL.DO)

        print(f"DSVF L{L}")

        self.comando()

        print(f"DSVS L{provisory_L}")
        print(f"L{L}: NADA")
    
    def comando_entrada(self):
        #<comando de entrada> ::= read ( <lista de identificadores> )
        print("LEIT")

        self.consome(AL.READ)
        self.consome(AL.ABRE_PARENT)
        self.lista_de_identi(funcEntrada_bool=True)
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
        print("IMPR")

    def expressao(self):
        # <expressao> ::= <expressao simples> [<operador relacional> <expressao simples>]

        self.expressao_simples()

        if arithmetic_relations_MULT:
            print(arithmetic_relations_MULT)
        
        if arithmetic_relations_ADD:
            print(arithmetic_relations_ADD)

        if self.lookahead.tipo == AL.RELOP:
            self.operador_relacional()
            self.expressao_simples()

            if instructions_relations:
                print(instructions_relations)



    
    def expressao_simples(self):
        #<expressao simples> ::= [+ | −] <termo> { <operador de adição> <termo> }
        global arithmetic_relations_ADD

        if self.lookahead.operador == AL.SOMA:
            self.consome(AL.ADDOP)

        elif self.lookahead.operador == AL.SUBT:
            self.consome(AL.ADDOP)
        
        self.termo()


        while self.lookahead.tipo == AL.ADDOP:
            self.operador_adicao()
            self.termo()
            if arithmetic_relations_ADD:
                print(arithmetic_relations_ADD)
                arithmetic_relations_ADD = ''

    def operador_adicao(self):
        # <operador de adição> ::= + | − | or
        global arithmetic_relations_ADD


        if self.lookahead.operador == AL.SOMA:
            arithmetic_relations_ADD = "SOMA"

            self.consome(AL.ADDOP)
        
        elif self.lookahead.operador == AL.SUBT:
            arithmetic_relations_ADD = "SUBT"

            self.consome(AL.ADDOP)
        
        elif self.lookahead.tipo == AL.OR:
            self.consome(AL.OR)

    def operador_relacional(self):
        # <operador relacional> ::= < | <= | = | <> | > | >=
        global instructions_relations

        if self.lookahead.tipo == AL.RELOP:
            # FAZER CADA RELOP
            if self.lookahead.lexema == ">=":
                instructions_relations = "CMAG"

            elif self.lookahead.lexema == "<=":
                instructions_relations = "CMEG"
            
            elif self.lookahead.lexema == "=":
                instructions_relations = "CMIG"
            
            elif self.lookahead.lexema == "<>":
                instructions_relations = "CMDG"
            
            elif self.lookahead.lexema == "<":
                instructions_relations = "CMME"
            
            elif self.lookahead.lexema == ">":
                instructions_relations = "CMMA"

            self.consome(AL.RELOP)

    def operador_multiplicacao(self):
        # <operador de multiplicação> ::= ∗ | / | div | mod | and
        global arithmetic_relations_MULT

        if self.lookahead.operador == AL.MULT:
            
            arithmetic_relations_MULT = "MULT"

            self.consome(AL.MULOP)
        
        elif self.lookahead.operador == AL.DIVI:

            arithmetic_relations_MULT = "DIVI"

            self.consome(AL.MULOP)
        
        elif self.lookahead.tipo == AL.MULOP:
            self.consome(AL.MULOP)

    def termo(self):
        # <termo> ::= <fator> { <operador de multiplicação> <fator> }
        self.fator()
        global arithmetic_relations_MULT

        while self.lookahead.tipo == AL.MULOP:
            self.operador_multiplicacao()
            self.fator()
            if arithmetic_relations_MULT:
                print(arithmetic_relations_MULT)
                arithmetic_relations_MULT = ""
    
    def fator(self):
        # <fator> ::=

        #         identificador |
        #         numero |
        #         ( <expressao> ) |
        #         true |
        #         false |
        #         not <fator>


        if self.lookahead.tipo == AL.IDENTIFICADOR:

            if self.lookahead.lexema not in table_symbols:
                raise SemanticoError(f"<{self.lookahead.lexema}> Não Foi Declarada!")
            
            print(f"CRVL {table_symbols.index(self.lookahead.lexema)}")

            self.consome(AL.IDENTIFICADOR)
        
        elif self.lookahead.tipo == AL.NUM:
            
            print(f"CRCT {self.lookahead.lexema}")

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


if  __name__ == '__main__':
    try:
        sintatico = Analisador_Sintatico()
        sintatico.init_sintatico()

    except (SintaticoError, LexicoError) as e:
        print(e)

#     else:
#         linhas = list(sintatico.lexico.buffer).count('\n') + 1
#         print(f'\n{linhas} linhas analisadas. Programa sintaticamente correto.')