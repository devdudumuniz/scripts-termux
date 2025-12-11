# Ferramentas do Framework

Esta pasta contém todos os scripts, binários e ferramentas de linha de comando que formam a espinha dorsal do DM Pentest Framework. As ferramentas são organizadas em subpastas que correspondem aos módulos da TUI.

## Organização

-   `osint/`: Ferramentas de Open Source Intelligence.
-   `network/`: Ferramentas de análise e varredura de rede.
-   `web/`: Ferramentas para testes em aplicações web.
-   `exploit/`: Ferramentas e scripts de exploração.
-   `forensic/`: Utilitários para análise forense.
-   `automation/`: Scripts para automação de tarefas.

## Como Adicionar uma Nova Ferramenta

1.  **Escolha a Categoria**: Coloque seu script na subpasta apropriada (ex: `network/`).
2.  **Padrão de Script**: Certifique-se de que seu script seja executável (`chmod +x`) e siga as boas práticas de scripting (tratamento de erros, parâmetros, etc.).
3.  **Integre com o Core**: Para que a ferramenta apareça na TUI, você precisará criar um módulo de plugin correspondente em `core/plugins/`. Consulte a documentação em `core/plugins/README.md` para mais detalhes.
