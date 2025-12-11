#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DM Termux Pentest - Network Utilities
Utilitários para operações de rede
"""

import socket
import subprocess
import re
import ipaddress
from typing import List, Dict, Any, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

class NetworkUtils:
    """Utilitários para operações de rede"""
    
    def __init__(self, max_threads: int = 10, timeout: int = 5):
        self.max_threads = max_threads
        self.timeout = timeout
    
    def is_valid_ip(self, ip: str) -> bool:
        """Verifica se é um IP válido"""
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
    
    def is_valid_cidr(self, cidr: str) -> bool:
        """Verifica se é uma notação CIDR válida"""
        try:
            ipaddress.ip_network(cidr, strict=False)
            return True
        except ValueError:
            return False
    
    def expand_cidr(self, cidr: str) -> List[str]:
        """Expande notação CIDR em lista de IPs"""
        try:
            network = ipaddress.ip_network(cidr, strict=False)
            return [str(ip) for ip in network.hosts()]
        except ValueError:
            return []
    
    def expand_range(self, ip_range: str) -> List[str]:
        """
        Expande range de IPs (ex: 192.168.1.1-50)
        """
        ips = []
        
        # Padrão: 192.168.1.1-50
        match = re.match(r'(\d+\.\d+\.\d+\.)(\d+)-(\d+)', ip_range)
        if match:
            prefix = match.group(1)
            start = int(match.group(2))
            end = int(match.group(3))
            
            for i in range(start, end + 1):
                ips.append(f"{prefix}{i}")
        
        return ips
    
    def ping(self, host: str, count: int = 1) -> bool:
        """
        Executa ping em um host
        
        Args:
            host: IP ou hostname
            count: Número de pacotes
            
        Returns:
            True se host está ativo
        """
        try:
            # Comando ping (compatível com Android/Termux)
            cmd = ['ping', '-c', str(count), '-W', str(self.timeout), host]
            result = subprocess.run(cmd, capture_output=True, timeout=self.timeout + 2)
            return result.returncode == 0
        except Exception:
            return False
    
    def ping_sweep(self, targets: List[str], 
                   progress_callback=None) -> List[Dict[str, Any]]:
        """
        Realiza ping sweep em múltiplos alvos
        
        Args:
            targets: Lista de IPs/hosts
            progress_callback: Função callback para progresso
            
        Returns:
            Lista de hosts ativos
        """
        active_hosts = []
        total = len(targets)
        completed = 0
        
        def ping_host(host):
            result = {
                'host': host,
                'status': 'down',
                'reachable': False
            }
            
            if self.ping(host):
                result['status'] = 'up'
                result['reachable'] = True
            
            return result
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = {executor.submit(ping_host, host): host for host in targets}
            
            for future in as_completed(futures):
                completed += 1
                result = future.result()
                
                if result['reachable']:
                    active_hosts.append(result)
                
                if progress_callback:
                    progress_callback(completed, total)
        
        return active_hosts
    
    def check_port(self, host: str, port: int) -> bool:
        """
        Verifica se uma porta está aberta
        
        Args:
            host: IP ou hostname
            port: Número da porta
            
        Returns:
            True se porta está aberta
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except Exception:
            return False
    
    def scan_ports(self, host: str, ports: List[int],
                  progress_callback=None) -> List[Dict[str, Any]]:
        """
        Escaneia portas em um host
        
        Args:
            host: IP ou hostname
            ports: Lista de portas a escanear
            progress_callback: Função callback para progresso
            
        Returns:
            Lista de portas abertas com informações
        """
        open_ports = []
        total = len(ports)
        completed = 0
        
        def scan_port(port):
            result = {
                'port': port,
                'state': 'closed',
                'service': self._get_service_name(port)
            }
            
            if self.check_port(host, port):
                result['state'] = 'open'
                # Tentar obter banner
                banner = self.grab_banner(host, port)
                if banner:
                    result['banner'] = banner
            
            return result
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = {executor.submit(scan_port, port): port for port in ports}
            
            for future in as_completed(futures):
                completed += 1
                result = future.result()
                
                if result['state'] == 'open':
                    open_ports.append(result)
                
                if progress_callback:
                    progress_callback(completed, total)
        
        return open_ports
    
    def grab_banner(self, host: str, port: int, timeout: int = 3) -> Optional[str]:
        """
        Tenta capturar banner de um serviço
        
        Args:
            host: IP ou hostname
            port: Porta do serviço
            timeout: Timeout em segundos
            
        Returns:
            Banner capturado ou None
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((host, port))
            
            # Tentar receber banner
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            sock.close()
            
            return banner if banner else None
        except Exception:
            return None
    
    def _get_service_name(self, port: int) -> str:
        """Retorna nome do serviço comum para a porta"""
        common_ports = {
            21: 'FTP',
            22: 'SSH',
            23: 'Telnet',
            25: 'SMTP',
            53: 'DNS',
            80: 'HTTP',
            110: 'POP3',
            143: 'IMAP',
            443: 'HTTPS',
            445: 'SMB',
            554: 'RTSP',
            3306: 'MySQL',
            3389: 'RDP',
            5432: 'PostgreSQL',
            5900: 'VNC',
            8000: 'HTTP-Alt',
            8080: 'HTTP-Proxy',
            8443: 'HTTPS-Alt',
            8888: 'HTTP-Alt'
        }
        
        return common_ports.get(port, 'Unknown')
    
    def get_local_ip(self) -> Optional[str]:
        """Retorna IP local da máquina"""
        try:
            # Criar socket UDP (não precisa conectar de verdade)
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            return None
    
    def get_network_range(self) -> Optional[str]:
        """Retorna range da rede local em notação CIDR"""
        local_ip = self.get_local_ip()
        if not local_ip:
            return None
        
        # Assumir /24 para redes locais comuns
        parts = local_ip.split('.')
        network = f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
        
        return network
    
    def resolve_hostname(self, hostname: str) -> Optional[str]:
        """Resolve hostname para IP"""
        try:
            return socket.gethostbyname(hostname)
        except Exception:
            return None
    
    def reverse_dns(self, ip: str) -> Optional[str]:
        """Resolve IP para hostname (reverse DNS)"""
        try:
            return socket.gethostbyaddr(ip)[0]
        except Exception:
            return None


# Instância global
_network_utils_instance = None

def get_network_utils(max_threads: int = 10, timeout: int = 5) -> NetworkUtils:
    """Retorna instância global do NetworkUtils"""
    global _network_utils_instance
    if _network_utils_instance is None:
        _network_utils_instance = NetworkUtils(max_threads, timeout)
    return _network_utils_instance
