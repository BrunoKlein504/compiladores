atomo_EOS = 0
IDENTIFICADOR = 1
OP_SOMA = 2
OP_MULT = 3

i = 0
buf = ''
lookahead = 0

def proximo_char():
    global i
    c = buf[i]
    i += 1
    return c

# mini analisador lexico
def proximo_atomo():
    c = proximo_char()
    if c == '\0':
        return atomo_EOS
    elif c == 'a' or c == 'b':
        return IDENTIFICADOR
    elif c == '+':
        return OP_SOMA
    elif c == '*':
        return OP_MULT
# E ::= a | b | +EE | *EE
def E():
    if lookahead == OP_SOMA:
        consome(OP_SOMA)
        E()
        E()
    elif lookahead == OP_MULT:
        consome(OP_MULT)
        E()
        E()
    elif lookahead == IDENTIFICADOR:
        consome(IDENTIFICADOR)
    else:
        print('Erro lexico!!')
        exit(1)

def consome(atomo):
    global lookahead
    if (atomo != lookahead):
        print('Erro sintático!')
    elif (atomo != atomo_EOS):
        lookahead = proximo_atomo()


def sintatico():
    global lookahead
    lookahead = proximo_atomo()
    E()
    consome(atomo_EOS)
    print('Expressão processada com sucesso!')

def main():
    global buf
    buf = input()
    buf = buf + '\0'
    sintatico()

main()