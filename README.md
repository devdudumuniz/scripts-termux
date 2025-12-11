# DM Termux Pentest Framework

<p align="center">
  <img src="assets/banners/main_banner.png" alt="DM Pentest Framework Banner">
</p>

<p align="center">
    <a href="#-sobre-o-projeto">Sobre</a> •
    <a href="#-estrutura-do-projeto">Estrutura</a> •
    <a href="#ferramentas">Ferramentas</a> •
    <a href="#instalação">Instalação</a> •
    <a href="#como-usar">Como Usar</a> •
    <a href="#roadmap">Roadmap</a> •
    <a href="#como-contribuir">Contribuir</a>
</p>

---

## 🚀 Sobre o Projeto

O **DM Termux Pentest** é um framework de segurança ofensiva e análise de redes, de código aberto, projetado especificamente para o ambiente **Termux** em dispositivos Android. Ele foi construído para ser uma ferramenta poderosa e portátil para profissionais de segurança, pesquisadores e entusiastas, permitindo a execução de uma suíte de pentest completa diretamente de um smartphone, com ou sem privilégios de **ROOT**.

Nossa missão é democratizar o acesso a ferramentas de segurança de qualidade, fornecendo uma plataforma modular, extensível e fácil de usar, que possa crescer com a colaboração da comunidade.

---

## 📂 Estrutura do Projeto

O projeto foi organizado para ser intuitivo e escalável, facilitando a colaboração e o desenvolvimento de novos módulos.

```
DM-pentest-opensource/
├── .github/          # Templates para Issues, PRs e workflows de CI/CD
├── assets/           # Logos, banners e screenshots
├── config/           # Arquivos de configuração do framework
├── core/             # O coração do sistema (TUI, loader, utils)
├── docs/             # Documentação detalhada do projeto
├── examples/         # Exemplos de uso prático das ferramentas
├── logs/             # Logs de execução das ferramentas
├── output/           # Resultados exportados (JSON, CSV)
├── scripts/          # Scripts auxiliares (instalação, build, etc.)
├── tests/            # Testes unitários e de integração
├── tools/            # Scripts e binários das ferramentas de pentest
├── CONTRIBUTING.md   # Guia para contribuidores
├── INSTALL.md        # Guia de instalação detalhado
├── LICENSE           # Licença do projeto (MIT)
├── README.md         # Este arquivo
├── ROADMAP.md        # Visão de futuro e grandes features
└── TODO.md           # Lista de tarefas e melhorias a fazer
```

---

## 🛠️ Ferramentas Disponíveis

O framework organiza as ferramentas em módulos, cada um com um propósito específico.

### Módulo OSINT

Ferramentas para coleta de informações de fontes abertas. Essencial para a fase de reconhecimento.

| Ferramenta         | Descrição                                         |
| :----------------- | :------------------------------------------------ |
| **IP Lookup**      | Coleta informações de geolocalização e ASN de um IP. |
| **Domain Lookup**  | Obtém registros DNS e informações de um domínio.    |
| **Email Validation** | Verifica a validade e os registros MX de um e-mail. |
| **Phone Analysis** | Analisa e extrai informações de um número de telefone. |

### Módulo de Rede

Análise e varredura de redes para identificar ativos e vulnerabilidades.

| Ferramenta          | Descrição                                                              |
| :------------------ | :--------------------------------------------------------------------- |
| **Ping Sweep**      | Descobre hosts ativos em uma determinada faixa de rede.                  |
| **Port Scanner**    | <img src="assets/logos/nmap.png" width=20> **Nmap**: Escaneia portas abertas, serviços e versões em um alvo. |
| **LAN Enumeration** | Enumera dispositivos e serviços em uma rede local.                     |
| **ARP Sniffer**     | Captura tráfego ARP para identificar hosts e possíveis ataques MitM.    |

### Módulo Web

Ferramentas focadas em testes de segurança de aplicações web.

| Ferramenta            | Descrição                                                                   |
| :-------------------- | :-------------------------------------------------------------------------- |
| **Web Enumeration**   | <img src="assets-logos/dirbuster.png" width=20> **DirBuster**: Enumera diretórios e arquivos em um servidor web. |
| **Headers Analysis**  | Analisa os cabeçalhos HTTP em busca de falhas de segurança e tecnologias. |

---

## ⚙️ Instalação

Para instruções detalhadas de instalação, consulte o arquivo [**INSTALL.md**](INSTALL.md).

```bash
# Clone o repositório
git clone https://github.com/SEU_USUARIO/DM-pentest-opensource.git

# Entre na pasta
cd DM-pentest-opensource

# Execute o script de instalação
./install.sh
```

---

## 🕹️ Como Usar

Após a instalação, inicie o framework com o comando principal:

```bash
./DM
```

Isso abrirá a interface TUI, onde você poderá navegar pelos módulos e executar as ferramentas de forma interativa.

Para exemplos de uso mais avançados e casos de uso práticos, consulte a pasta [**examples/**](examples/).

---

## 🗺️ Roadmap

Estamos sempre planejando o futuro! Nossos principais objetivos incluem:

-   **Integração com Shodan**: Adicionar um módulo para consultar a API do Shodan.
-   **Melhorias no Módulo de Exploração**: Integrar com bases de dados de exploits.
-   **Suporte a Hardware Externo**: Adaptações para uso com antenas Wi-Fi e 5G via OTG.

Para uma visão completa, veja nosso [**ROADMAP.md**](ROADMAP.md).

---

## 🤝 Como Contribuir

Este é um projeto feito pela comunidade para a comunidade. Toda contribuição é bem-vinda! Se você quer ajudar, por favor, leia nosso [**CONTRIBUTING.md**](CONTRIBUTING.md) para saber como.

### Tarefas e Melhorias

Procurando por onde começar? Dê uma olhada no nosso [**TODO.md**](TODO.md) para ver a lista de tarefas, bugs a serem corrigidos e melhorias planejadas.

---

## ⚖️ Licença

Este projeto está sob a licença MIT. Veja o arquivo [**LICENSE**](LICENSE) para mais detalhes.
