# Configuração do Framework

Esta pasta contém os arquivos de configuração que permitem personalizar o comportamento e a aparência do DM Pentest Framework.

## Arquivos

- `settings.json`: Contém as configurações globais do framework.
  - `performance`: Ajustes de performance, como o número máximo de threads para tarefas paralelas.
  - `logging`: Configurações de nível de log (DEBUG, INFO, WARNING, ERROR).
  - `plugins`: Permite habilitar ou desabilitar módulos de plugins específicos.

- `themes.json`: Define os esquemas de cores para a interface TUI. O framework vem com temas `dark` e `light` por padrão, mas você pode criar e adicionar seus próprios temas aqui.

## Como Editar

Você pode editar esses arquivos diretamente com um editor de texto. As alterações serão aplicadas na próxima vez que o framework for iniciado. Uma interface para editar as configurações mais comuns também está disponível diretamente na TUI, no menu de configurações.
