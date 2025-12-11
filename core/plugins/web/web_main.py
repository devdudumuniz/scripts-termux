#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plugin WEB - Web Application Testing
Módulo de testes e enumeração web
"""

import os
import sys
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'core'))

from utils_logging import get_logger
from utils_export import get_exporter

def get_module_metadata():
    """Retorna metadados do módulo"""
    return {
        'name': 'WEB',
        'category': 'WEB',
        'description': 'Ferramentas de teste e enumeração de aplicações web',
        'version': '1.0.0',
        'author': 'DM',
        'tools': [
            'Web Enumeration (Directory Bruteforce)',
            'HTTP Headers Analysis',
            'Technology Detection'
        ]
    }

def run_module(tui_context=None):
    """Executa o módulo WEB"""
    logger = get_logger()
    logger.info("Módulo WEB iniciado")
    
    if tui_context is None:
        return run_cli_mode()
    
    return run_tui_mode(tui_context)

def run_cli_mode():
    """Executa em modo linha de comando"""
    print("\n" + "="*60)
    print("  WEB Module - DM Pentest")
    print("="*60 + "\n")
    
    print("Ferramentas disponíveis:")
    print("  1) Web Enumeration (Directory Bruteforce)")
    print("  2) HTTP Headers Analysis")
    print("  0) Voltar")
    
    choice = input("\nEscolha uma opção: ").strip()
    
    if choice == '1':
        url = input("Digite a URL base (ex: http://example.com): ").strip()
        run_web_enum(url)
    elif choice == '2':
        url = input("Digite a URL: ").strip()
        run_headers_analysis(url)
    elif choice == '0':
        return
    else:
        print("Opção inválida!")

def run_tui_mode(tui_context):
    """Executa em modo TUI"""
    return {
        'tools': [
            {
                'name': 'Web Enumeration',
                'action': run_web_enum,
                'params': ['url']
            },
            {
                'name': 'HTTP Headers Analysis',
                'action': run_headers_analysis,
                'params': ['url']
            }
        ]
    }

def run_web_enum(url, wordlist=None):
    """Executa enumeração web"""
    logger = get_logger()
    logger.info(f"Executando Web Enumeration: {url}")
    
    tool_path = Path(__file__).parent.parent.parent / 'no-root-tools' / 'web_enum.sh'
    
    try:
        cmd = ['bash', str(tool_path), url]
        if wordlist:
            cmd.append(wordlist)
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        print(result.stdout)
        
        if result.returncode == 0:
            logger.log_execution('Web Enumeration', {'url': url}, status='success')
            return {'status': 'success', 'output': result.stdout}
        else:
            logger.log_execution('Web Enumeration', {'url': url}, status='error', error=result.stderr)
            return {'status': 'error', 'output': result.stderr}
    
    except Exception as e:
        logger.error(f"Erro ao executar Web Enumeration: {e}")
        return {'status': 'error', 'error': str(e)}

def run_headers_analysis(url):
    """Analisa headers HTTP"""
    logger = get_logger()
    logger.info(f"Analisando headers: {url}")
    
    try:
        import urllib.request
        
        print(f"\n[*] Analisando headers de: {url}\n")
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, timeout=10) as response:
            headers = dict(response.headers)
            
            print("Headers encontrados:")
            print("-" * 60)
            
            for key, value in headers.items():
                print(f"{key}: {value}")
            
            print("-" * 60)
            
            # Análise de segurança
            print("\n[*] Análise de Segurança:")
            
            security_headers = {
                'X-Frame-Options': 'Proteção contra clickjacking',
                'X-Content-Type-Options': 'Proteção contra MIME sniffing',
                'X-XSS-Protection': 'Proteção contra XSS',
                'Strict-Transport-Security': 'HSTS - Força HTTPS',
                'Content-Security-Policy': 'CSP - Política de segurança de conteúdo'
            }
            
            for header, description in security_headers.items():
                if header in headers:
                    print(f"[+] {header}: PRESENTE - {description}")
                else:
                    print(f"[-] {header}: AUSENTE - {description}")
            
            # Detectar tecnologias
            print("\n[*] Tecnologias Detectadas:")
            
            server = headers.get('Server', 'Unknown')
            powered_by = headers.get('X-Powered-By', 'Unknown')
            
            print(f"Server: {server}")
            print(f"Powered-By: {powered_by}")
            
            logger.log_execution('HTTP Headers Analysis', {'url': url}, 
                               results={'headers_count': len(headers)}, status='success')
            
            return {'status': 'success', 'headers': headers}
    
    except Exception as e:
        logger.error(f"Erro ao analisar headers: {e}")
        print(f"[!] Erro: {e}")
        return {'status': 'error', 'error': str(e)}

if __name__ == '__main__':
    run_module()
