#!/data/data/com.termux/files/usr/bin/bash
# -*- coding: utf-8 -*-
#
# WiFi Scanner com privilégios ROOT
# Utiliza modo monitor e aircrack-ng para captura avançada
#
# PRÉ-REQUISITOS:
#   - Root access
#   - aircrack-ng instalado
#   - Interface wireless compatível com modo monitor
#
# USO:
#   ./wifi_scan_root.sh [interface] [tempo_scan]
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
SCAN_TIME="${2:-30}"
OUTPUT_DIR="../output"
LOG_DIR="../logs"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Criar diretórios
mkdir -p "$OUTPUT_DIR/json" "$OUTPUT_DIR/csv" "$LOG_DIR"

# Arquivo de log
LOGFILE="$LOG_DIR/wifi_scan_root_${TIMESTAMP}.log"

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

# Verificar aircrack-ng
check_aircrack() {
    if ! command -v airmon-ng &> /dev/null; then
        log_error "aircrack-ng não instalado. Execute: pkg install aircrack-ng"
        exit 1
    fi
    log_success "aircrack-ng encontrado"
}

# Habilitar modo monitor
enable_monitor_mode() {
    log "Habilitando modo monitor em $INTERFACE..."
    
    # Matar processos que podem interferir
    su -c "airmon-ng check kill" 2>/dev/null || true
    
    # Habilitar modo monitor
    su -c "airmon-ng start $INTERFACE" 2>&1 | tee -a "$LOGFILE"
    
    # Interface em modo monitor geralmente fica como wlan0mon
    MONITOR_INTERFACE="${INTERFACE}mon"
    
    if su -c "iwconfig $MONITOR_INTERFACE" 2>/dev/null | grep -q "Mode:Monitor"; then
        log_success "Modo monitor habilitado em $MONITOR_INTERFACE"
    else
        log_error "Falha ao habilitar modo monitor"
        exit 1
    fi
}

# Desabilitar modo monitor
disable_monitor_mode() {
    log "Desabilitando modo monitor..."
    su -c "airmon-ng stop $MONITOR_INTERFACE" 2>&1 | tee -a "$LOGFILE"
    log_success "Modo monitor desabilitado"
}

# Escanear redes WiFi
scan_networks() {
    log "Escaneando redes WiFi por ${SCAN_TIME} segundos..."
    
    CAPTURE_FILE="$OUTPUT_DIR/wifi_capture_${TIMESTAMP}"
    
    # Iniciar airodump-ng
    timeout "$SCAN_TIME" su -c "airodump-ng -w $CAPTURE_FILE --output-format csv $MONITOR_INTERFACE" 2>&1 | tee -a "$LOGFILE" || true
    
    log_success "Scan concluído"
}

# Processar resultados
process_results() {
    log "Processando resultados..."
    
    CSV_FILE="${CAPTURE_FILE}-01.csv"
    
    if [ ! -f "$CSV_FILE" ]; then
        log_error "Arquivo de captura não encontrado"
        return 1
    fi
    
    # Processar CSV com Python
    python3 << EOF
import csv
import json
from datetime import datetime

networks = []
csv_file = "$CSV_FILE"

try:
    with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    # Separar seção de APs
    sections = content.split('\n\n')
    if len(sections) < 1:
        print("Nenhuma rede encontrada")
        exit(0)
    
    # Processar APs
    lines = sections[0].strip().split('\n')
    
    # Encontrar header
    header_idx = 0
    for i, line in enumerate(lines):
        if 'BSSID' in line:
            header_idx = i
            break
    
    if header_idx == 0:
        print("Header não encontrado")
        exit(0)
    
    # Processar redes
    for line in lines[header_idx + 1:]:
        if not line.strip():
            continue
            
        parts = [p.strip() for p in line.split(',')]
        
        if len(parts) >= 14:
            network = {
                'bssid': parts[0],
                'channel': parts[3],
                'speed': parts[4],
                'privacy': parts[5],
                'cipher': parts[6],
                'authentication': parts[7],
                'power': parts[8],
                'beacons': parts[9],
                'iv': parts[10],
                'lan_ip': parts[11],
                'id_length': parts[12],
                'essid': parts[13],
                'timestamp': datetime.now().isoformat()
            }
            
            networks.append(network)
    
    # Salvar JSON
    json_output = "$OUTPUT_DIR/json/wifi_scan_${TIMESTAMP}.json"
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump({
            'scan_timestamp': datetime.now().isoformat(),
            'interface': '$MONITOR_INTERFACE',
            'total_networks': len(networks),
            'networks': networks
        }, f, indent=2, ensure_ascii=False)
    
    # Salvar CSV limpo
    csv_output = "$OUTPUT_DIR/csv/wifi_scan_${TIMESTAMP}.csv"
    with open(csv_output, 'w', newline='', encoding='utf-8') as f:
        if networks:
            writer = csv.DictWriter(f, fieldnames=networks[0].keys())
            writer.writeheader()
            writer.writerows(networks)
    
    print(f"Encontradas {len(networks)} redes")
    print(f"JSON: {json_output}")
    print(f"CSV: {csv_output}")
    
except Exception as e:
    print(f"Erro ao processar: {e}")
    exit(1)
EOF
    
    log_success "Resultados processados e exportados"
}

# Cleanup
cleanup() {
    log "Limpando arquivos temporários..."
    rm -f "${CAPTURE_FILE}"*.cap "${CAPTURE_FILE}"*.kismet.* 2>/dev/null || true
    disable_monitor_mode
}

# Trap para cleanup
trap cleanup EXIT

# Main
main() {
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}  WiFi Scanner ROOT - DM Pentest${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    
    check_root
    check_aircrack
    enable_monitor_mode
    scan_networks
    process_results
    
    echo ""
    log_success "Scan WiFi ROOT concluído com sucesso!"
}

main
