# ROADMAP - Visão de Futuro do Projeto

Este documento descreve a visão de longo prazo e as principais direções de desenvolvimento para o DM Pentest Framework. Nosso objetivo é evoluir de uma suíte de ferramentas para uma plataforma de segurança ofensiva completa e adaptável.

## Q1 2026: Expansão e Usabilidade

-   **Internacionalização (i18n)**: Adicionar suporte a múltiplos idiomas na interface TUI, começando com Inglês e Espanhol.
-   **Construtor de Workflows (v1)**: Lançar a primeira versão do construtor de workflows, permitindo que os usuários criem sequências de automação simples (ex: Ping Sweep -> Port Scan -> Web Enum).
-   **Integração com Metasploit**: Criar um wrapper para interagir com o `msfconsole` e `msfvenom`, facilitando a busca de exploits e a geração de payloads.

## Q2 2026: Inteligência e Integração

-   **Integração com Shodan**: Desenvolver um módulo completo para consultar a API do Shodan, permitindo a busca por dispositivos, vulnerabilidades e serviços expostos na internet.
-   **Módulo de Análise de Malware**: Adicionar ferramentas para análise estática de arquivos APK e executáveis, extraindo strings, permissões e possíveis indicadores de comprometimento (IoCs).
-   **Dashboard Web (Beta)**: Iniciar o desenvolvimento de uma interface web opcional para visualização de dados e gerenciamento de alvos, rodando em um servidor local no dispositivo.

## Q3 2026: Foco em Hardware e Redes Sem Fio

-   **Suporte a Hardware Externo via OTG**: Esta é uma das nossas metas mais ambiciosas. O objetivo é permitir que o framework utilize hardware especializado conectado via USB OTG para expandir suas capacidades.
    -   **Antenas Wi-Fi Externas**: Integrar com adaptadores Wi-Fi que suportam modo monitor e injeção de pacotes (ex: Alfa, Panda Wireless). Isso permitirá ataques mais avançados a redes Wi-Fi, como deautenticação, Evil Twin, e captura de handshakes WPA/WPA2 de forma mais eficaz.
    -   **Rádios SDR (Software-Defined Radio)**: Adicionar suporte para dispositivos como HackRF e RTL-SDR, abrindo portas para análise de sinais de rádio, GPS spoofing, e ataques a dispositivos IoT que usam frequências sub-GHz.
    -   **Adaptadores 5G/LTE**: Desenvolver funcionalidades para análise de redes móveis, como wardriving 5G, identificação de estações rádio-base (ERBs) e análise de metadados de tráfego móvel (requer hardware e configurações específicas).

| Hardware            | Objetivo Principal                                      | Exemplo de Ferramenta a Integrar |
| :------------------ | :------------------------------------------------------ | :------------------------------- |
| **Antena Wi-Fi OTG**  | Auditoria avançada de redes Wi-Fi (Modo Monitor)        | Aircrack-ng, Kismet, Wifite      |
| **Rádio SDR OTG**     | Análise de sinais de rádio e segurança de IoT           | GQRX, URH, rtl_433             |
| **Adaptador 5G OTG**  | Análise e mapeamento de redes de telefonia móvel        | Ferramentas customizadas         |

## Q4 2026 e Além: Automação e IA

-   **Pentest Automatizado (Auto-Pentest)**: Desenvolver um módulo que, dado um alvo, executa um workflow de pentest completo de forma autônoma, desde o reconhecimento até a identificação de vulnerabilidades, gerando um relatório final.
-   **Correlação de Dados com IA**: Utilizar modelos de machine learning para correlacionar os dados coletados de diferentes módulos, identificando padrões e priorizando os vetores de ataque mais promissores.
-   **Ecossistema de Plugins da Comunidade**: Criar um repositório central para que a comunidade possa submeter, avaliar e instalar plugins de forma segura e fácil, diretamente da TUI.

Este roadmap é um documento vivo e será atualizado com base no feedback da comunidade e nas novas tendências do cenário de segurança da informação. Se você tem ideias ou quer ajudar a construir o futuro do projeto, junte-se a nós!
