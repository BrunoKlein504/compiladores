from AnalisadorExceptions import LexicoError, SintaticoError
from analisador_sinatico_v3 import Analisador_Sintatico

try:
    sintatico = Analisador_Sintatico()
    sintatico.init_sintatico()

except (SintaticoError, LexicoError) as e:
    print(e)

else:
    linhas = list(sintatico.lexico.buffer).count('\n') + 1
    print(f'\n{linhas} linhas analisadas. Programa sintaticamente correto.')