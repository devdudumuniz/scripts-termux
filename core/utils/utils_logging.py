#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DM Termux Pentest - Logging Utilities
Módulo centralizado para gerenciamento de logs
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

class PentestLogger:
    """Gerenciador centralizado de logs para o framework"""
    
    def __init__(self, config_path: str = "config/settings.json"):
        self.config = self._load_config(config_path)
        self.log_dir = Path(self.config.get("logging", {}).get("log_dir", "logs/"))
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Configurar logging
        self._setup_logging()
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Carrega configurações do arquivo JSON"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {
                "logging": {
                    "enabled": True,
                    "level": "INFO",
                    "verbose": False,
                    "log_to_file": True
                }
            }
    
    def _setup_logging(self):
        """Configura o sistema de logging"""
        log_config = self.config.get("logging", {})
        level = getattr(logging, log_config.get("level", "INFO"))
        
        # Formato do log
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # Configurar handlers
        handlers = []
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(log_format))
        handlers.append(console_handler)
        
        # File handler
        if log_config.get("log_to_file", True):
            log_file = self.log_dir / f"pentest_{datetime.now().strftime('%Y%m%d')}.log"
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(logging.Formatter(log_format))
            handlers.append(file_handler)
        
        # Configurar logger raiz
        logging.basicConfig(
            level=level,
            format=log_format,
            handlers=handlers
        )
        
        self.logger = logging.getLogger("DMPentest")
    
    def log_execution(self, tool_name: str, parameters: Dict[str, Any], 
                     results: Optional[Dict[str, Any]] = None, 
                     status: str = "success", error: Optional[str] = None):
        """
        Registra a execução de uma ferramenta
        
        Args:
            tool_name: Nome da ferramenta executada
            parameters: Parâmetros utilizados
            results: Resultados obtidos (opcional)
            status: Status da execução (success, error, warning)
            error: Mensagem de erro (se houver)
        """
        timestamp = datetime.now().isoformat()
        
        log_entry = {
            "timestamp": timestamp,
            "tool": tool_name,
            "parameters": parameters,
            "status": status,
            "results_summary": self._summarize_results(results) if results else None,
            "error": error
        }
        
        # Log em arquivo JSON estruturado
        json_log_file = self.log_dir / f"executions_{datetime.now().strftime('%Y%m%d')}.json"
        
        try:
            # Carregar logs existentes
            if json_log_file.exists():
                with open(json_log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            else:
                logs = []
            
            # Adicionar novo log
            logs.append(log_entry)
            
            # Salvar
            with open(json_log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
        
        except Exception as e:
            self.logger.error(f"Erro ao salvar log JSON: {e}")
        
        # Log no sistema de logging padrão
        if status == "success":
            self.logger.info(f"Executado: {tool_name} - {parameters}")
        elif status == "error":
            self.logger.error(f"Erro em {tool_name}: {error}")
        else:
            self.logger.warning(f"Aviso em {tool_name}: {error}")
    
    def _summarize_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um resumo dos resultados para logging"""
        summary = {}
        
        if isinstance(results, dict):
            # Contar itens principais
            for key, value in results.items():
                if isinstance(value, list):
                    summary[f"{key}_count"] = len(value)
                elif isinstance(value, dict):
                    summary[f"{key}_keys"] = list(value.keys())
                else:
                    summary[key] = value
        
        return summary
    
    def info(self, message: str):
        """Log de informação"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log de aviso"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log de erro"""
        self.logger.error(message)
    
    def debug(self, message: str):
        """Log de debug"""
        self.logger.debug(message)
    
    def get_recent_logs(self, limit: int = 50) -> list:
        """Retorna os logs mais recentes"""
        json_log_file = self.log_dir / f"executions_{datetime.now().strftime('%Y%m%d')}.json"
        
        try:
            if json_log_file.exists():
                with open(json_log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
                    return logs[-limit:] if len(logs) > limit else logs
        except Exception as e:
            self.logger.error(f"Erro ao carregar logs recentes: {e}")
        
        return []


# Instância global do logger
_logger_instance = None

def get_logger() -> PentestLogger:
    """Retorna a instância global do logger"""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = PentestLogger()
    return _logger_instance
