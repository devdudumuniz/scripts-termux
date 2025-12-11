# TODO - Lista de Tarefas e Melhorias

Este arquivo rastreia tarefas, bugs e melhorias planejadas para o DM Pentest Framework. É um ótimo lugar para começar se você quer contribuir para o projeto.

## 🐛 Bugs

- [ ] **UI**: Corrigir quebra de layout da tabela em telas muito pequenas.
- [ ] **Export**: A exportação para CSV de resultados com múltiplas linhas não está formatando corretamente.
- [ ] **Network**: O ARP Sniffer não está salvando o arquivo de captura `.pcap` corretamente em alguns dispositivos.

## ✨ Melhorias de Curto Prazo

- [ ] **Core**: Implementar um sistema de cache para consultas OSINT repetidas (ex: cache de DNS).
- [ ] **UI**: Adicionar um menu de "Favoritos" para acesso rápido às ferramentas mais usadas.
- [ ] **OSINT**: Adicionar busca por nome de usuário em redes sociais (ex: com a ferramenta `sherlock`).
- [ ] **Web**: Melhorar o Web Enumerator para testar diferentes extensões de arquivo (ex: `.php`, `.bak`, `.config`).
- [ ] **Docs**: Adicionar mais exemplos práticos na pasta `examples/`.

## 🚀 Novas Funcionalidades (Médio Prazo)

- [ ] **Módulo de Exploração**: Integrar com a base de dados do Exploit-DB via `searchsploit`.
- [ ] **Módulo de Automação**: Desenvolver um construtor de workflows visual na TUI, permitindo encadear a execução de múltiplas ferramentas.
- [ ] **Módulo de Relatórios**: Criar um gerador de relatórios em PDF a partir dos dados coletados em JSON/CSV.
- [ ] **Testes**: Aumentar a cobertura de testes unitários para os módulos do `core/`.

## 🗺️ Visão de Longo Prazo (ver ROADMAP.md)

- [ ] **Integração com Shodan**: Criar um novo módulo para interagir com a API do Shodan.
- [ ] **Suporte a Hardware Externo**: Desenvolver funcionalidades específicas para uso com hardware conectado via OTG.
- [ ] **Interface Gráfica**: Explorar a possibilidade de uma interface gráfica (GUI) web para o framework.

## Como Pegar uma Tarefa

1.  Comente na Issue correspondente à tarefa (ou crie uma nova se não existir).
2.  Faça um fork do projeto e crie uma nova branch para sua feature/correção.
3.  Desenvolva a solução.
4.  Abra um Pull Request referenciando a Issue.

Obrigado por ajudar a tornar o DM Pentest Framework melhor!
