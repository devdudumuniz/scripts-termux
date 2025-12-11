#!/data/data/com.termux/files/usr/bin/bash
# -*- coding: utf-8 -*-
#
# ARP Sniffer com privilégios ROOT
# Captura e analisa tráfego ARP na rede
#
# PRÉ-REQUISITOS:
#   - Root access
#   - tcpdump instalado
#
# USO:
#   ./arp_sniffer_root.sh [interface] [duration]
#

set -e

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configurações
INTERFACE="${1:-wlan0}"
DURATION="${2:-60}"
OUTPUT_DIR="../output"
LOG_DIR="../logs"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Criar diretórios
mkdir -p "$OUTPUT_DIR/json" "$OUTPUT_DIR/csv" "$LOG_DIR"

# Arquivo de log
LOGFILE="$LOG_DIR/arp_sniffer_${TIMESTAMP}.log"
PCAP_FILE="$OUTPUT_DIR/arp_capture_${TIMESTAMP}.pcap"

# Função de log
log() {
    echo -e "${CYAN}[$(date +'%H:%M:%S')]${NC} $1" | tee -a "$LOGFILE"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOGFILE"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1" | tee -a "$LOGFILE"
}

# Verificar root
check_root() {
    if [ "$EUID" -ne 0 ] && ! su -c "exit" 2>/dev/null; then
        log_error "Este script requer privilégios ROOT"
        exit 1
    fi
    log_success "Privilégios ROOT confirmados"
}

# Verificar tcpdump
check_tcpdump() {
    if ! command -v tcpdump &> /dev/null; then
        log_error "tcpdump não instalado. Execute: pkg install tcpdump"
        exit 1
    fi
    log_success "tcpdump encontrado"
}

# Capturar tráfego ARP
capture_arp() {
    log "Capturando tráfego ARP em $INTERFACE por ${DURATION} segundos..."
    
    # Capturar apenas pacotes ARP
    timeout "$DURATION" su -c "tcpdump -i $INTERFACE -w $PCAP_FILE arp" 2>&1 | tee -a "$LOGFILE" || true
    
    log_success "Captura concluída"
}

# Analisar captura
analyze_capture() {
    log "Analisando captura ARP..."
    
    if [ ! -f "$PCAP_FILE" ]; then
        log_error "Arquivo de captura não encontrado"
        return 1
    fi
    
    # Ler PCAP e extrair informações ARP
    su -c "tcpdump -r $PCAP_FILE -n -e" > "$OUTPUT_DIR/arp_raw_${TIMESTAMP}.txt" 2>&1
    
    # Processar com Python
    python3 << EOF
import re
import json
import csv
from datetime import datetime
from collections import defaultdict

arp_packets = []
arp_table = defaultdict(set)
raw_file = "$OUTPUT_DIR/arp_raw_${TIMESTAMP}.txt"

try:
    with open(raw_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            # Padrão: timestamp MAC1 > MAC2, ethertype ARP (28), Request who-has IP1 tell IP2
            # ou: timestamp MAC1 > MAC2, ethertype ARP (28), Reply IP1 is-at MAC1
            
            if 'ARP' not in line:
                continue
            
            packet = {
                'timestamp': datetime.now().isoformat(),
                'raw': line.strip()
            }
            
            # Extrair tipo (Request/Reply)
            if 'Request' in line:
                packet['type'] = 'Request'
                # who-has IP1 tell IP2
                match = re.search(r'who-has (\S+) tell (\S+)', line)
                if match:
                    packet['target_ip'] = match.group(1)
                    packet['sender_ip'] = match.group(2)
            elif 'Reply' in line:
                packet['type'] = 'Reply'
                # IP is-at MAC
                match = re.search(r'(\S+) is-at (\S+)', line)
                if match:
                    packet['sender_ip'] = match.group(1)
                    packet['sender_mac'] = match.group(2)
                    
                    # Adicionar à tabela ARP
                    arp_table[packet['sender_ip']].add(packet['sender_mac'])
            
            # Extrair MACs do cabeçalho ethernet
            mac_match = re.search(r'(\S+) > (\S+),', line)
            if mac_match:
                packet['src_mac'] = mac_match.group(1)
                packet['dst_mac'] = mac_match.group(2)
            
            arp_packets.append(packet)
    
    # Detectar possíveis ARP spoofing (múltiplos MACs para mesmo IP)
    spoofing_alerts = []
    for ip, macs in arp_table.items():
        if len(macs) > 1:
            spoofing_alerts.append({
                'ip': ip,
                'macs': list(macs),
                'alert': 'Múltiplos MACs para mesmo IP - possível ARP spoofing'
            })
    
    # Criar tabela ARP limpa
    arp_table_clean = [
        {'ip': ip, 'mac': ', '.join(macs)}
        for ip, macs in arp_table.items()
    ]
    
    # Salvar JSON
    json_output = "$OUTPUT_DIR/json/arp_analysis_${TIMESTAMP}.json"
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump({
            'capture_timestamp': datetime.now().isoformat(),
            'interface': '$INTERFACE',
            'duration_seconds': $DURATION,
            'total_packets': len(arp_packets),
            'arp_table': arp_table_clean,
            'spoofing_alerts': spoofing_alerts,
            'packets': arp_packets[:100]  # Limitar a 100 primeiros para não ficar muito grande
        }, f, indent=2, ensure_ascii=False)
    
    # Salvar CSV da tabela ARP
    csv_output = "$OUTPUT_DIR/csv/arp_table_${TIMESTAMP}.csv"
    if arp_table_clean:
        with open(csv_output, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['ip', 'mac'])
            writer.writeheader()
            writer.writerows(arp_table_clean)
    
    # Salvar alertas de spoofing
    if spoofing_alerts:
        csv_alerts = "$OUTPUT_DIR/csv/arp_spoofing_alerts_${TIMESTAMP}.csv"
        with open(csv_alerts, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['ip', 'macs', 'alert'])
            writer.writeheader()
            for alert in spoofing_alerts:
                alert['macs'] = ', '.join(alert['macs'])
                writer.writerow(alert)
        print(f"ALERTAS DE SPOOFING: {csv_alerts}")
    
    print(f"Total de pacotes ARP: {len(arp_packets)}")
    print(f"Entradas na tabela ARP: {len(arp_table_clean)}")
    print(f"Alertas de spoofing: {len(spoofing_alerts)}")
    print(f"JSON: {json_output}")
    print(f"CSV: {csv_output}")
    
except Exception as e:
    print(f"Erro ao processar: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
EOF
    
    log_success "Análise concluída"
}

# Cleanup
cleanup() {
    log "Limpando arquivos temporários..."
    rm -f "$OUTPUT_DIR/arp_raw_${TIMESTAMP}.txt" 2>/dev/null || true
}

# Trap para cleanup
trap cleanup EXIT

# Main
main() {
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}  ARP Sniffer ROOT - DM Pentest${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    
    check_root
    check_tcpdump
    capture_arp
    analyze_capture
    
    echo ""
    log_success "ARP Sniffer ROOT concluído com sucesso!"
    log "Arquivo PCAP salvo em: $PCAP_FILE"
}

main
