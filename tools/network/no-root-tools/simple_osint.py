#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple OSINT - Coleta de informações públicas
Ferramenta básica de OSINT usando APIs públicas

PRÉ-REQUISITOS:
    - Python 3.x
    - Conexão com internet

USO:
    ./simple_osint.py <tipo> <alvo>
    
    Tipos:
        ip      - Informações sobre IP
        domain  - Informações sobre domínio
        email   - Validação de email (formato)
        phone   - Formato de telefone
"""

import sys
import json
import csv
import socket
import re
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

# Cores
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'

class OSINTTool:
    """Ferramenta básica de OSINT"""
    
    def __init__(self):
        self.output_dir = Path('../output')
        self.json_dir = self.output_dir / 'json'
        self.csv_dir = self.output_dir / 'csv'
        
        self.json_dir.mkdir(parents=True, exist_ok=True)
        self.csv_dir.mkdir(parents=True, exist_ok=True)
    
    def ip_lookup(self, ip):
        """Lookup de informações sobre IP"""
        print(f"{Colors.CYAN}[*]{Colors.NC} Coletando informações sobre IP: {ip}\n")
        
        info = {
            'ip': ip,
            'timestamp': datetime.now().isoformat()
        }
        
        # Reverse DNS
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            info['hostname'] = hostname
            print(f"{Colors.GREEN}[+]{Colors.NC} Hostname: {hostname}")
        except:
            info['hostname'] = 'N/A'
            print(f"{Colors.YELLOW}[!]{Colors.NC} Hostname: N/A")
        
        # GeoIP usando API pública (ip-api.com)
        try:
            url = f"http://ip-api.com/json/{ip}"
            with urllib.request.urlopen(url, timeout=10) as response:
                geo_data = json.loads(response.read().decode())
                
                if geo_data.get('status') == 'success':
                    info['country'] = geo_data.get('country', 'Unknown')
                    info['region'] = geo_data.get('regionName', 'Unknown')
                    info['city'] = geo_data.get('city', 'Unknown')
                    info['isp'] = geo_data.get('isp', 'Unknown')
                    info['org'] = geo_data.get('org', 'Unknown')
                    info['as'] = geo_data.get('as', 'Unknown')
                    info['lat'] = geo_data.get('lat', 0)
                    info['lon'] = geo_data.get('lon', 0)
                    
                    print(f"{Colors.GREEN}[+]{Colors.NC} País: {info['country']}")
                    print(f"{Colors.GREEN}[+]{Colors.NC} Região: {info['region']}")
                    print(f"{Colors.GREEN}[+]{Colors.NC} Cidade: {info['city']}")
                    print(f"{Colors.GREEN}[+]{Colors.NC} ISP: {info['isp']}")
                    print(f"{Colors.GREEN}[+]{Colors.NC} Organização: {info['org']}")
                    print(f"{Colors.GREEN}[+]{Colors.NC} AS: {info['as']}")
        except Exception as e:
            print(f"{Colors.RED}[!]{Colors.NC} Erro ao obter GeoIP: {e}")
        
        return info
    
    def domain_lookup(self, domain):
        """Lookup de informações sobre domínio"""
        print(f"{Colors.CYAN}[*]{Colors.NC} Coletando informações sobre domínio: {domain}\n")
        
        info = {
            'domain': domain,
            'timestamp': datetime.now().isoformat()
        }
        
        # Resolver DNS
        try:
            ip = socket.gethostbyname(domain)
            info['ip'] = ip
            print(f"{Colors.GREEN}[+]{Colors.NC} IP: {ip}")
        except:
            info['ip'] = 'N/A'
            print(f"{Colors.YELLOW}[!]{Colors.NC} IP: N/A (não resolvido)")
        
        # Tentar obter informações do servidor web
        try:
            url = f"http://{domain}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            with urllib.request.urlopen(req, timeout=10) as response:
                headers = dict(response.headers)
                
                info['server'] = headers.get('Server', 'Unknown')
                info['powered_by'] = headers.get('X-Powered-By', 'Unknown')
                
                print(f"{Colors.GREEN}[+]{Colors.NC} Server: {info['server']}")
                print(f"{Colors.GREEN}[+]{Colors.NC} Powered-By: {info['powered_by']}")
        except Exception as e:
            print(f"{Colors.YELLOW}[!]{Colors.NC} Não foi possível acessar servidor web")
        
        # Verificar portas comuns
        common_ports = [21, 22, 25, 80, 443, 3306, 3389, 8080]
        open_ports = []
        
        print(f"\n{Colors.CYAN}[*]{Colors.NC} Verificando portas comuns...")
        
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((domain, port))
                sock.close()
                
                if result == 0:
                    open_ports.append(port)
                    print(f"{Colors.GREEN}[+]{Colors.NC} Porta {port} aberta")
            except:
                pass
        
        info['open_ports'] = open_ports
        
        return info
    
    def email_check(self, email):
        """Verifica formato de email"""
        print(f"{Colors.CYAN}[*]{Colors.NC} Verificando email: {email}\n")
        
        info = {
            'email': email,
            'timestamp': datetime.now().isoformat()
        }
        
        # Validar formato
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        is_valid = re.match(email_regex, email) is not None
        
        info['valid_format'] = is_valid
        
        if is_valid:
            print(f"{Colors.GREEN}[+]{Colors.NC} Formato válido")
            
            # Extrair domínio
            domain = email.split('@')[1]
            info['domain'] = domain
            print(f"{Colors.GREEN}[+]{Colors.NC} Domínio: {domain}")
            
            # Verificar MX records
            try:
                import subprocess
                result = subprocess.run(
                    ['nslookup', '-type=mx', domain],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if 'mail exchanger' in result.stdout.lower():
                    info['has_mx'] = True
                    print(f"{Colors.GREEN}[+]{Colors.NC} MX records encontrados")
                else:
                    info['has_mx'] = False
                    print(f"{Colors.YELLOW}[!]{Colors.NC} MX records não encontrados")
            except:
                info['has_mx'] = 'Unknown'
        else:
            print(f"{Colors.RED}[!]{Colors.NC} Formato inválido")
        
        return info
    
    def phone_check(self, phone):
        """Verifica formato de telefone"""
        print(f"{Colors.CYAN}[*]{Colors.NC} Analisando telefone: {phone}\n")
        
        info = {
            'phone': phone,
            'timestamp': datetime.now().isoformat()
        }
        
        # Remover caracteres não numéricos
        digits = re.sub(r'\D', '', phone)
        info['digits'] = digits
        info['digit_count'] = len(digits)
        
        print(f"{Colors.GREEN}[+]{Colors.NC} Dígitos: {digits}")
        print(f"{Colors.GREEN}[+]{Colors.NC} Total de dígitos: {len(digits)}")
        
        # Identificar país (básico)
        if len(digits) == 11 and digits.startswith('55'):
            info['country'] = 'Brasil'
            info['type'] = 'Celular' if digits[4] == '9' else 'Fixo'
        elif len(digits) == 10:
            info['country'] = 'Brasil (sem código país)'
            info['type'] = 'Celular' if digits[2] == '9' else 'Fixo'
        else:
            info['country'] = 'Unknown'
            info['type'] = 'Unknown'
        
        print(f"{Colors.GREEN}[+]{Colors.NC} País: {info['country']}")
        print(f"{Colors.GREEN}[+]{Colors.NC} Tipo: {info['type']}")
        
        return info
    
    def export_results(self, data, prefix):
        """Exporta resultados"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # JSON
        json_file = self.json_dir / f"{prefix}_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # CSV
        csv_file = self.csv_dir / f"{prefix}_{timestamp}.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            writer.writeheader()
            writer.writerow(data)
        
        return str(json_file), str(csv_file)

def main():
    if len(sys.argv) < 3:
        print(f"{Colors.RED}Uso:{Colors.NC} {sys.argv[0]} <tipo> <alvo>")
        print(f"\nTipos disponíveis:")
        print(f"  ip      - Informações sobre IP")
        print(f"  domain  - Informações sobre domínio")
        print(f"  email   - Validação de email")
        print(f"  phone   - Análise de telefone")
        sys.exit(1)
    
    osint_type = sys.argv[1].lower()
    target = sys.argv[2]
    
    # Banner
    print(f"{Colors.CYAN}{'='*60}{Colors.NC}")
    print(f"{Colors.YELLOW}  Simple OSINT - DM Pentest{Colors.NC}")
    print(f"{Colors.CYAN}{'='*60}{Colors.NC}\n")
    
    tool = OSINTTool()
    
    # Executar lookup apropriado
    if osint_type == 'ip':
        data = tool.ip_lookup(target)
        prefix = f"osint_ip_{target.replace('.', '_')}"
    elif osint_type == 'domain':
        data = tool.domain_lookup(target)
        prefix = f"osint_domain_{target.replace('.', '_')}"
    elif osint_type == 'email':
        data = tool.email_check(target)
        prefix = f"osint_email_{target.replace('@', '_at_').replace('.', '_')}"
    elif osint_type == 'phone':
        data = tool.phone_check(target)
        prefix = f"osint_phone"
    else:
        print(f"{Colors.RED}[!]{Colors.NC} Tipo inválido: {osint_type}")
        sys.exit(1)
    
    # Exportar
    json_file, csv_file = tool.export_results(data, prefix)
    
    print(f"\n{Colors.CYAN}{'='*60}{Colors.NC}")
    print(f"{Colors.GREEN}[✓]{Colors.NC} Coleta concluída")
    print(f"\n{Colors.CYAN}[*]{Colors.NC} Resultados exportados:")
    print(f"    JSON: {json_file}")
    print(f"    CSV: {csv_file}")
    print(f"{Colors.CYAN}{'='*60}{Colors.NC}\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!]{Colors.NC} Interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.NC} {e}")
        sys.exit(1)
