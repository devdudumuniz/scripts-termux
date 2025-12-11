#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plugin FORENSIC - Digital Forensics
Módulo de análise forense digital
"""

import sys
import os
import hashlib
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'core'))

from utils_logging import get_logger
from utils_export import get_exporter

def get_module_metadata():
    """Retorna metadados do módulo"""
    return {
        'name': 'FORENSIC',
        'category': 'FORENSIC',
        'description': 'Ferramentas de análise forense digital',
        'version': '1.0.0',
        'author': 'DM',
        'tools': [
            'File Hash Calculator',
            'File Metadata Extractor',
            'String Extractor'
        ]
    }

def run_module(tui_context=None):
    """Executa o módulo FORENSIC"""
    logger = get_logger()
    logger.info("Módulo FORENSIC iniciado")
    
    print("\n" + "="*60)
    print("  FORENSIC Module - DM Pentest")
    print("="*60 + "\n")
    
    print("Ferramentas disponíveis:")
    print("  1) File Hash Calculator")
    print("  2) File Metadata Extractor")
    print("  3) String Extractor")
    print("  0) Voltar")
    
    choice = input("\nEscolha uma opção: ").strip()
    
    if choice == '1':
        filepath = input("Digite o caminho do arquivo: ").strip()
        calculate_hashes(filepath)
    elif choice == '2':
        filepath = input("Digite o caminho do arquivo: ").strip()
        extract_metadata(filepath)
    elif choice == '3':
        filepath = input("Digite o caminho do arquivo: ").strip()
        extract_strings(filepath)
    elif choice == '0':
        return
    else:
        print("Opção inválida!")
    
    return {'status': 'success'}

def calculate_hashes(filepath):
    """Calcula hashes de um arquivo"""
    logger = get_logger()
    
    if not os.path.exists(filepath):
        print(f"[!] Arquivo não encontrado: {filepath}")
        return
    
    print(f"\n[*] Calculando hashes de: {filepath}\n")
    
    try:
        # MD5
        md5_hash = hashlib.md5()
        # SHA1
        sha1_hash = hashlib.sha1()
        # SHA256
        sha256_hash = hashlib.sha256()
        
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                md5_hash.update(chunk)
                sha1_hash.update(chunk)
                sha256_hash.update(chunk)
        
        results = {
            'file': filepath,
            'md5': md5_hash.hexdigest(),
            'sha1': sha1_hash.hexdigest(),
            'sha256': sha256_hash.hexdigest(),
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"MD5:    {results['md5']}")
        print(f"SHA1:   {results['sha1']}")
        print(f"SHA256: {results['sha256']}")
        
        # Exportar
        exporter = get_exporter()
        exported = exporter.export_json(results, 'file_hashes')
        print(f"\n[+] Resultados salvos em: {exported}")
        
        logger.log_execution('File Hash Calculator', {'file': filepath}, results=results, status='success')
        
    except Exception as e:
        print(f"[!] Erro: {e}")
        logger.error(f"Erro ao calcular hashes: {e}")

def extract_metadata(filepath):
    """Extrai metadados de um arquivo"""
    if not os.path.exists(filepath):
        print(f"[!] Arquivo não encontrado: {filepath}")
        return
    
    print(f"\n[*] Extraindo metadados de: {filepath}\n")
    
    try:
        stat_info = os.stat(filepath)
        
        metadata = {
            'file': filepath,
            'size_bytes': stat_info.st_size,
            'created': datetime.fromtimestamp(stat_info.st_ctime).isoformat(),
            'modified': datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
            'accessed': datetime.fromtimestamp(stat_info.st_atime).isoformat(),
            'permissions': oct(stat_info.st_mode)[-3:],
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"Tamanho: {metadata['size_bytes']} bytes")
        print(f"Criado: {metadata['created']}")
        print(f"Modificado: {metadata['modified']}")
        print(f"Acessado: {metadata['accessed']}")
        print(f"Permissões: {metadata['permissions']}")
        
        # Exportar
        exporter = get_exporter()
        exported = exporter.export_json(metadata, 'file_metadata')
        print(f"\n[+] Resultados salvos em: {exported}")
        
    except Exception as e:
        print(f"[!] Erro: {e}")

def extract_strings(filepath, min_length=4):
    """Extrai strings de um arquivo"""
    if not os.path.exists(filepath):
        print(f"[!] Arquivo não encontrado: {filepath}")
        return
    
    print(f"\n[*] Extraindo strings de: {filepath}\n")
    
    try:
        strings = []
        
        with open(filepath, 'rb') as f:
            current_string = b''
            
            while byte := f.read(1):
                if 32 <= byte[0] <= 126:  # Caracteres imprimíveis ASCII
                    current_string += byte
                else:
                    if len(current_string) >= min_length:
                        strings.append(current_string.decode('ascii', errors='ignore'))
                    current_string = b''
        
        print(f"[+] Encontradas {len(strings)} strings (mínimo {min_length} caracteres)")
        print("\nPrimeiras 20 strings:")
        print("-" * 60)
        
        for s in strings[:20]:
            print(s)
        
        print("-" * 60)
        
        # Exportar
        exporter = get_exporter()
        exported = exporter.export_json({
            'file': filepath,
            'total_strings': len(strings),
            'strings': strings[:100],  # Limitar a 100
            'timestamp': datetime.now().isoformat()
        }, 'file_strings')
        
        print(f"\n[+] Resultados salvos em: {exported}")
        
    except Exception as e:
        print(f"[!] Erro: {e}")

if __name__ == '__main__':
    run_module()
