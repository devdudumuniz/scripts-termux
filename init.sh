#!/data/data/com.termux/files/usr/bin/bash
# -*- coding: utf-8 -*-
#
# DM Termux Pentest - Initialization Script
# Script de inicialização e configuração automática
#

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
show_banner() {
    clear
    echo -e "${GREEN}"
    cat << "EOF"
    ____  __  ________           __       ______                           
   / __ \/  |/  /_  __/__  _____/ /_     /_  __/__  _________ ___  ___  __
  / / / / /|_/ / / / / _ \/ ___/ __ \     / / / _ \/ ___/ __ `__ \/ / / / /
 / /_/ / /  / / / / /  __/ /__/ / / /    / / /  __/ /  / / / / / / /_/ /  
/_____/_/  /_/ /_/  \___/\___/_/ /_/    /_/  \___/_/  /_/ /_/ /_/\__,_/   
                                                                            
    ____             __            __     ______                            
   / __ \___  ____  / /____  _____/ /_   / ____/________ _____ ___  ___ 
  / /_/ / _ \/ __ \/ __/ _ \/ ___/ __/  / /_  / ___/ __ `/ __ `__ \/ _ \
 / ____/  __/ / / / /_/  __(__  ) /_   / __/ / /  / /_/ / / / / / /  __/
/_/    \___/_/ /_/\__/\___/____/\__/  /_/   /_/   \__,_/_/ /_/ /_/\___/ 
                                                                          
EOF
    echo -e "${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}  Framework de Pentest para Termux - v1.0.0${NC}"
    echo -e "${YELLOW}  Desenvolvido por DM${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
    echo ""
}

# Função de log
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Detectar se tem root
detect_root() {
    log_info "Detectando privilégios de root..."
    
    if command -v su &> /dev/null; then
        if su -c "exit" 2>/dev/null; then
            log_success "Root detectado e disponível"
            HAS_ROOT=true
        else
            log_warning "Root não disponível ou negado"
            HAS_ROOT=false
        fi
    else
        log_warning "Comando 'su' não encontrado - sem root"
        HAS_ROOT=false
    fi
}

# Atualizar pacotes
update_packages() {
    log_info "Atualizando repositórios do Termux..."
    
    pkg update -y 2>&1 | grep -v "^Reading" | grep -v "^Building" || true
    
    log_info "Atualizando pacotes instalados..."
    pkg upgrade -y 2>&1 | grep -v "^Reading" | grep -v "^Building" || true
    
    log_success "Pacotes atualizados"
}

# Instalar dependências básicas
install_basic_deps() {
    log_info "Instalando dependências básicas..."
    
    BASIC_PACKAGES=(
        "python"
        "git"
        "curl"
        "wget"
        "nmap"
        "nodejs"
        "termux-api"
    )
    
    for package in "${BASIC_PACKAGES[@]}"; do
        if ! command -v "$package" &> /dev/null; then
            log_info "Instalando $package..."
            pkg install -y "$package" 2>&1 | tail -n 5
        else
            log_success "$package já instalado"
        fi
    done
}

# Instalar ferramentas de pentest
install_pentest_tools() {
    log_info "Instalando ferramentas de pentest..."
    
    PENTEST_PACKAGES=(
        "nmap"
        "hydra"
        "netcat"
        "dnsutils"
        "whois"
    )
    
    for package in "${PENTEST_PACKAGES[@]}"; do
        if ! pkg list-installed 2>/dev/null | grep -q "^$package/"; then
            log_info "Instalando $package..."
            pkg install -y "$package" 2>&1 | tail -n 5 || log_warning "Falha ao instalar $package"
        else
            log_success "$package já instalado"
        fi
    done
}

# Instalar ferramentas root (se disponível)
install_root_tools() {
    if [ "$HAS_ROOT" = true ]; then
        log_info "Instalando ferramentas que requerem root..."
        
        ROOT_PACKAGES=(
            "tsu"
            "aircrack-ng"
            "tcpdump"
        )
        
        for package in "${ROOT_PACKAGES[@]}"; do
            if ! pkg list-installed 2>/dev/null | grep -q "^$package/"; then
                log_info "Instalando $package..."
                pkg install -y "$package" 2>&1 | tail -n 5 || log_warning "Falha ao instalar $package"
            else
                log_success "$package já instalado"
            fi
        done
    else
        log_warning "Pulando instalação de ferramentas root (root não disponível)"
    fi
}

# Configurar ambiente Python
setup_python_env() {
    log_info "Configurando ambiente Python..."
    
    # Instalar pip se necessário
    if ! command -v pip &> /dev/null; then
        log_info "Instalando pip..."
        pkg install -y python-pip
    fi
    
    # Criar diretório venv se não existir
    if [ ! -d "core/venv" ]; then
        log_info "Criando ambiente virtual Python..."
        python -m venv core/venv
    fi
    
    # Ativar venv e instalar dependências
    log_info "Instalando bibliotecas Python..."
    source core/venv/bin/activate
    
    pip install --upgrade pip -q
    pip install rich textual requests beautifulsoup4 -q
    
    deactivate
    
    log_success "Ambiente Python configurado"
}

# Configurar permissões
setup_permissions() {
    log_info "Configurando permissões..."
    
    # Tornar scripts executáveis
    find . -name "*.sh" -type f -exec chmod +x {} \;
    find . -name "*.py" -type f -exec chmod +x {} \;
    
    log_success "Permissões configuradas"
}

# Criar arquivos de configuração se não existirem
setup_config() {
    log_info "Verificando configurações..."
    
    # Atualizar config com detecção de root
    if [ -f "config/settings.json" ]; then
        python3 << EOF
import json
with open('config/settings.json', 'r') as f:
    config = json.load(f)
config['app']['has_root'] = $HAS_ROOT
with open('config/settings.json', 'w') as f:
    json.dump(config, f, indent=2)
EOF
        log_success "Configuração atualizada com status de root"
    fi
}

# Menu de seleção de modo
select_mode() {
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}  Selecione o modo de operação:${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    
    if [ "$HAS_ROOT" = true ]; then
        echo -e "${GREEN}  1)${NC} Modo ROOT (acesso completo)"
        echo -e "${YELLOW}  2)${NC} Modo NO-ROOT (sem privilégios)"
        echo -e "${BLUE}  3)${NC} Modo HÍBRIDO (detectar automaticamente)"
    else
        echo -e "${YELLOW}  1)${NC} Modo NO-ROOT (sem privilégios) ${RED}[ÚNICO DISPONÍVEL]${NC}"
        echo -e "${BLUE}  2)${NC} Modo HÍBRIDO (detectar automaticamente)"
    fi
    
    echo ""
    read -p "$(echo -e ${CYAN}Escolha uma opção:${NC} )" mode_choice
    
    case $mode_choice in
        1)
            if [ "$HAS_ROOT" = true ]; then
                SELECTED_MODE="root"
            else
                SELECTED_MODE="no-root"
            fi
            ;;
        2)
            if [ "$HAS_ROOT" = true ]; then
                SELECTED_MODE="no-root"
            else
                SELECTED_MODE="hybrid"
            fi
            ;;
        3)
            SELECTED_MODE="hybrid"
            ;;
        *)
            log_warning "Opção inválida, usando modo híbrido"
            SELECTED_MODE="hybrid"
            ;;
    esac
    
    log_success "Modo selecionado: $SELECTED_MODE"
}

# Iniciar TUI
start_tui() {
    log_info "Iniciando interface TUI..."
    echo ""
    
    # Ativar venv e executar TUI
    source core/venv/bin/activate
    python core/tui_main.py --mode "$SELECTED_MODE"
    deactivate
}

# Main
main() {
    show_banner
    
    # Detectar root
    detect_root
    
    # Perguntar se quer fazer setup completo
    echo ""
    read -p "$(echo -e ${CYAN}Deseja executar o setup completo? [S/n]:${NC} )" do_setup
    
    if [[ "$do_setup" =~ ^[Ss]$ ]] || [[ -z "$do_setup" ]]; then
        update_packages
        install_basic_deps
        install_pentest_tools
        install_root_tools
        setup_python_env
        setup_permissions
        setup_config
        
        log_success "Setup concluído com sucesso!"
    else
        log_info "Pulando setup, usando configuração existente"
    fi
    
    # Selecionar modo
    select_mode
    
    # Iniciar TUI
    start_tui
}

# Executar
main
