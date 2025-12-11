# Exemplo Prático: Scanning Completo de uma Rede Local

Este exemplo demonstra como usar o DM Pentest Framework para realizar um scanning completo de uma rede local, desde a descoberta de hosts até a identificação de serviços e possíveis vulnerabilidades.

## Cenário

Você está conectado à rede Wi-Fi de um cliente (com autorização) e precisa mapear todos os dispositivos ativos, identificar os serviços em execução e gerar um relatório consolidado.

**Rede**: 192.168.1.0/24  
**Objetivo**: Descobrir hosts, portas abertas e serviços.

## Passo 1: Descoberta de Hosts (Ping Sweep)

Primeiro, vamos identificar quais endereços IP estão ativos na rede.

1.  Inicie o framework: `./DM`
2.  No menu principal, selecione `3` (Módulo REDE).
3.  Selecione `1` (Ping Sweep).
4.  Digite a rede: `192.168.1.0/24`
5.  Aguarde a conclusão. O framework irá exibir uma lista de IPs ativos.

**Saída Esperada**:
```
[+] Host ativo: 192.168.1.1
[+] Host ativo: 192.168.1.10
[+] Host ativo: 192.168.1.25
[+] Host ativo: 192.168.1.50
...
[*] Total de hosts ativos: 12
```

Os resultados são salvos automaticamente em `output/json/ping_sweep_192_168_1_0_24_TIMESTAMP.json`.

## Passo 2: Scanning de Portas

Agora, para cada host ativo, vamos escanear as portas abertas. Vamos usar o host `192.168.1.50` como exemplo.

1.  No módulo REDE, selecione `2` (Port Scanner).
2.  Digite o IP alvo: `192.168.1.50`
3.  Escolha o tipo de scan: `common` (portas comuns) ou `full` (todas as portas 1-65535).
4.  Aguarde a conclusão.

**Saída Esperada**:
```
[*] Escaneando 192.168.1.50...

[+] Porta 22 aberta - SSH
[+] Porta 80 aberta - HTTP
[+] Porta 443 aberta - HTTPS

[*] Total de portas abertas: 3
```

## Passo 3: Enumeração Web (se aplicável)

Se o host tem as portas 80 ou 443 abertas, podemos fazer uma enumeração web.

1.  Volte ao menu principal e selecione `2` (Módulo WEB).
2.  Selecione `1` (Web Enumeration).
3.  Digite a URL base: `http://192.168.1.50`
4.  O framework irá procurar por diretórios e arquivos comuns.

**Saída Esperada**:
```
[+] Encontrado: /admin (200)
[+] Encontrado: /login (200)
[+] Encontrado: /backup (403)
...
```

## Passo 4: Geração de Relatório

Após coletar todos os dados, você pode gerar um relatório consolidado.

1.  No menu principal, selecione `6` (Módulo AUTOMATION).
2.  Selecione `3` (Report Generator).
3.  O framework irá consolidar todos os scans realizados e gerar um relatório em JSON.

O relatório consolidado estará em `output/json/consolidated_report_TIMESTAMP.json` e pode ser aberto em qualquer editor de texto ou importado para ferramentas de análise.

## Conclusão

Com esses passos simples, você mapeou completamente uma rede, identificou serviços e gerou um relatório. Este é apenas um exemplo básico; o framework oferece muito mais ferramentas para aprofundar sua análise.
