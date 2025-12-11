# Core do Sistema

Esta pasta contém o código-fonte principal que alimenta o DM Pentest Framework. É o cérebro por trás da interface, do carregamento de módulos e das funcionalidades centrais.

## Estrutura

-   `tui/`: Contém o código para a interface de usuário em modo texto (TUI), construída com a biblioteca Rich.
-   `utils/`: Módulos de utilidades usados em todo o framework, como logging, exportação de dados e funções de rede.
-   `plugins/`: O sistema de carregamento de plugins. Cada subpasta aqui representa um módulo que integra as ferramentas da pasta `tools/` com a TUI.

## Fluxo de Execução

1.  O script principal na raiz do projeto inicia o `tui/main.py`.
2.  A TUI utiliza o `plugins/loader.py` para descobrir e carregar todos os módulos de plugin disponíveis.
3.  Cada plugin define os metadados de um módulo (nome, descrição, ferramentas) e aponta para os scripts correspondentes na pasta `tools/`.
4.  Quando um usuário seleciona uma ferramenta na TUI, o plugin correspondente é acionado, que por sua vez executa o script da ferramenta e captura sua saída.
