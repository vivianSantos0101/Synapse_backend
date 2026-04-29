# Synapse Backend - Busca Semantica de Repositorios

## Como Baixar o Projeto Pelo GitHub

Se voce recebeu apenas o link do repositorio, o caminho mais simples e este:

1. Abra a pagina do projeto no GitHub.
2. Clique no botao verde `Code`.
3. Clique em `Download ZIP`.
4. Aguarde o download terminar.
5. Extraia o arquivo ZIP para uma pasta do seu computador.
6. Abra essa pasta na sua IDE para começar a mexer na aplicação.

Se a pasta extraida vier com um nome parecido com `Synapse_backend-main`, esse e o comportamento normal do GitHub ao baixar o ZIP.

## Requisitos Para Rodar

Para executar o projeto localmente, e recomendado ter:

- Python 3 instalado na maquina
- `pip` habilitado
- VS Code ou terminal de sua preferencia
- Conexao com a internet na primeira execucao, porque o modelo de embeddings pode precisar ser baixado

No Windows, normalmente o comando do Python aparece como `py`.
Em alguns ambientes, tambem pode funcionar como `python`.

## Como Instalar as Dependencias

1. Abra um terminal.
2. Entre na pasta `semantic_search`.
3. Instale os pacotes listados em `requirements.txt`, conforme a seguir:

    ### Windows

    ```no powershell ou terminal da IDE:
    cd [caminho da pasta], exemplo: cd c:\Users\SEU_USUARIO\caminho\Synapse_backend-main\semantic_search
    py -m pip install -r requirements.txt
    ```

    ### Linux ou macOS

    ```no bash:
    cd [diretório], exemplo: cd /caminho/para/Synapse_backend-main/semantic_search
    python3 -m pip install -r requirements.txt
    ```

## Como Executar a Aplicacao

O funcionamento mais simples deste projeto usa dois terminais. Consulte como abrir dois terminais na sua IDE. 

### Terminal 1 - Servidor

  Esse terminal fica responsavel por subir a API.

  Na pasta `semantic_search`, execute:

  ### Windows

    ```no powershell ou terminal da IDE
    py -m uvicorn app.main:app --reload
    ```

  ### Linux ou macOS

    ```no bash
    python3 -m uvicorn app.main:app --reload
    ```

  Se tudo der certo, o terminal mostrara uma mensagem semelhante a `Application startup complete`.

## Terminal 2 - Indexacao e Testes

  Esse segundo terminal serve para enviar arquivos Markdown para a API e depois fazer buscas.

  Exemplo com o arquivo `nebula_teste.md`:

  ### Windows

    ```powershell
    py testar_readme.py nebula_teste.md empresa/nebula
    ```

    ### Linux ou macOS

    ```bash
    python3 testar_readme.py nebula_teste.md empresa/nebula
    ```

## Observacoes Importantes

- Na primeira execucao, o projeto pode demorar mais por causa do carregamento do modelo de embeddings.
- O banco local fica salvo na pasta `semantic_search/data/chroma_db`.
- O script de teste nao sobe o servidor. Ele depende do servidor ja estar em execucao.
- O fluxo mais comum e deixar o servidor em um terminal e executar os testes em outro.

## Resumo Rapido

1. Baixar o projeto do GitHub.
2. Extrair os arquivos.
3. Abrir a pasta `semantic_search`.
4. Instalar as dependencias com `pip`.
5. Subir o servidor com `uvicorn` em um terminal.
6. Em outro terminal, rodar `testar_readme.py` com o arquivo desejado.
7. Fazer buscas no terminal e analisar os resultados.
