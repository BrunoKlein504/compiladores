# Projeto de Compiladores

Este projeto de compiladores é dividido em várias partes que trabalham juntas para analisar e compilar código-fonte. A seguir, descrevemos a estrutura do projeto e suas funcionalidades principais.

## Estrutura do Projeto

- **main.py**: Este é o arquivo principal que inicia a execução do compilador. Para executar o projeto, basta rodar este arquivo.

- **analisador_lexico.py**: Este arquivo contém a lógica para o analisador léxico, responsável por ler e analisar o código-fonte. Ele identifica tokens e classifica os elementos do código.

- **analisador_sintatico.py**: Este arquivo contém a lógica para o analisador sintático, que analisa a estrutura dos tokens gerados pelo analisador léxico e verifica se eles seguem as regras gramaticais da linguagem.

- **AnalisadorExceptions.py**: Este módulo é responsável pelas classes de exceções personalizadas que ajudam a tratar erros de maneira mais informativa e específica durante a análise do código.

- **Arquivos de Texto**:
  - `program01.txt`: Um dos arquivos de texto que será lido pelo analisador léxico.
  - `program02.txt`: Outro arquivo de texto que será lido pelo analisador léxico.
  - `pascal_example.pas`: Um arquivo Pascal que também será lido pelo analisador léxico.

## Execução

Para executar o projeto, siga os passos abaixo:

1. Certifique-se de que você tem o Python instalado em seu sistema.
2. Clone o repositório ou baixe os arquivos do projeto.
3. Navegue até o diretório do projeto usando o terminal ou Git Bash.
4. Execute o arquivo principal com o seguinte comando:

   ```bash
   python main.py
