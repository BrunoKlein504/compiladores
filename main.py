from AnalisadorExceptions import LexicoError, SintaticoError, SemanticoError
from analisador_semantico import Analisador_Sintatico

try:
    sintatico = Analisador_Sintatico()
    sintatico.init_sintatico()

except (SintaticoError, LexicoError, SemanticoError) as e:
    print(e)

else:
    linhas = list(sintatico.lexico.buffer).count('\n') + 1
    print(f'\n{linhas} linhas analisadas. Programa sintaticamente correto.')