#!/data/data/com.termux/files/usr/bin/bash
# -*- coding: utf-8 -*-
#
# LAN Enumeration com privilégios ROOT
# Enumeração completa da rede local com nmap privilegiado
#
# PRÉ-REQUISITOS:
#   - Root access
#   - nmap instalado
#
# USO:
#   ./lan_enum_root.sh [network_cidr]
#

set -e

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configurações
NETWORK="${1:-192.168.1.0/24}"
OUTPUT_DIR="../output"
LOG_DIR="../logs"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Criar diretórios
mkdir -p "$OUTPUT_DIR/json" "$OUTPUT_DIR/csv" "$LOG_DIR"

# Arquivo de log
LOGFILE="$LOG_DIR/lan_enum_root_${TIMESTAMP}.log"

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

# Verificar nmap
check_nmap() {
    if ! command -v nmap &> /dev/null; then
        log_error "nmap não instalado. Execute: pkg install nmap"
        exit 1
    fi
    log_success "nmap encontrado"
}

# Auto-detectar rede se não fornecida
detect_network() {
    if [ "$NETWORK" == "auto" ]; then
        log "Auto-detectando rede local..."
        
        # Obter IP local
        LOCAL_IP=$(ip route get 8.8.8.8 | awk '{print $7; exit}')
        
        if [ -z "$LOCAL_IP" ]; then
            log_error "Não foi possível detectar IP local"
            exit 1
        fi
        
        # Assumir /24
        NETWORK=$(echo "$LOCAL_IP" | cut -d. -f1-3).0/24
        log_success "Rede detectada: $NETWORK"
    fi
}

# Scan rápido de hosts ativos
quick_scan() {
    log "Executando scan rápido de hosts ativos..."
    
    QUICK_OUTPUT="$OUTPUT_DIR/lan_quick_${TIMESTAMP}.xml"
    
    su -c "nmap -sn -PE -PA21,23,80,443,3389 --privileged -oX $QUICK_OUTPUT $NETWORK" 2>&1 | tee -a "$LOGFILE"
    
    log_success "Scan rápido concluído"
}

# Scan completo com detecção de OS e serviços
full_scan() {
    log "Executando scan completo (OS detection, versões de serviços)..."
    
    FULL_OUTPUT="$OUTPUT_DIR/lan_full_${TIMESTAMP}.xml"
    
    # Scan completo com privilégios
    su -c "nmap -sS -sV -O -A --privileged -T4 -oX $FULL_OUTPUT $NETWORK" 2>&1 | tee -a "$LOGFILE"
    
    log_success "Scan completo concluído"
}

# Processar resultados XML do nmap
process_results() {
    log "Processando resultados..."
    
    FULL_OUTPUT="$OUTPUT_DIR/lan_full_${TIMESTAMP}.xml"
    
    if [ ! -f "$FULL_OUTPUT" ]; then
        log_error "Arquivo de resultado não encontrado"
        return 1
    fi
    
    # Processar XML com Python
    python3 << EOF
import xml.etree.ElementTree as ET
import json
import csv
from datetime import datetime

hosts = []
xml_file = "$FULL_OUTPUT"

try:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    for host in root.findall('host'):
        # Status
        status = host.find('status')
        if status is None or status.get('state') != 'up':
            continue
        
        host_data = {
            'timestamp': datetime.now().isoformat(),
            'state': 'up'
        }
        
        # Endereços
        addresses = host.findall('address')
        for addr in addresses:
            addr_type = addr.get('addrtype')
            if addr_type == 'ipv4':
                host_data['ip'] = addr.get('addr')
            elif addr_type == 'mac':
                host_data['mac'] = addr.get('addr')
                host_data['vendor'] = addr.get('vendor', 'Unknown')
        
        # Hostnames
        hostnames = host.find('hostnames')
        if hostnames is not None:
            hostname_list = [hn.get('name') for hn in hostnames.findall('hostname')]
            host_data['hostnames'] = ', '.join(hostname_list) if hostname_list else 'N/A'
        else:
            host_data['hostnames'] = 'N/A'
        
        # OS Detection
        os_elem = host.find('os')
        if os_elem is not None:
            osmatch = os_elem.find('osmatch')
            if osmatch is not None:
                host_data['os'] = osmatch.get('name', 'Unknown')
                host_data['os_accuracy'] = osmatch.get('accuracy', '0')
            else:
                host_data['os'] = 'Unknown'
                host_data['os_accuracy'] = '0'
        else:
            host_data['os'] = 'Unknown'
            host_data['os_accuracy'] = '0'
        
        # Portas abertas
        ports_elem = host.find('ports')
        open_ports = []
        
        if ports_elem is not None:
            for port in ports_elem.findall('port'):
                state = port.find('state')
                if state is not None and state.get('state') == 'open':
                    port_id = port.get('portid')
                    protocol = port.get('protocol')
                    
                    service = port.find('service')
                    if service is not None:
                        service_name = service.get('name', 'unknown')
                        service_version = service.get('version', '')
                        product = service.get('product', '')
                    else:
                        service_name = 'unknown'
                        service_version = ''
                        product = ''
                    
                    open_ports.append({
                        'port': port_id,
                        'protocol': protocol,
                        'service': service_name,
                        'product': product,
                        'version': service_version
                    })
        
        host_data['open_ports_count'] = len(open_ports)
        host_data['open_ports'] = ', '.join([f"{p['port']}/{p['protocol']}" for p in open_ports])
        host_data['services'] = ', '.join([p['service'] for p in open_ports])
        
        hosts.append(host_data)
    
    # Salvar JSON
    json_output = "$OUTPUT_DIR/json/lan_enum_${TIMESTAMP}.json"
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump({
            'scan_timestamp': datetime.now().isoformat(),
            'network': '$NETWORK',
            'total_hosts': len(hosts),
            'hosts': hosts
        }, f, indent=2, ensure_ascii=False)
    
    # Salvar CSV
    csv_output = "$OUTPUT_DIR/csv/lan_enum_${TIMESTAMP}.csv"
    if hosts:
        with open(csv_output, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['ip', 'mac', 'vendor', 'hostnames', 'os', 'os_accuracy', 
                         'open_ports_count', 'open_ports', 'services', 'state', 'timestamp']
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(hosts)
    
    print(f"Encontrados {len(hosts)} hosts ativos")
    print(f"JSON: {json_output}")
    print(f"CSV: {csv_output}")
    
except Exception as e:
    print(f"Erro ao processar: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
EOF
    
    log_success "Resultados processados e exportados"
}

# Main
main() {
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}  LAN Enumeration ROOT - DM Pentest${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    
    check_root
    check_nmap
    detect_network
    
    log "Alvo: $NETWORK"
    
    quick_scan
    full_scan
    process_results
    
    echo ""
    log_success "Enumeração LAN ROOT concluída com sucesso!"
}

main
