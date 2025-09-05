#!/usr/bin/env python3
"""
LivChat Setup v0.1 - Entry Point
Sistema modular para deploy automatizado de aplicações Docker
"""

import os
import sys
import json
from pathlib import Path

# Adiciona diretório core ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_root():
    """Verifica se está executando como root"""
    if os.geteuid() != 0:
        print("\033[91m✗ Este script precisa ser executado como root\033[0m")
        print("\033[90mUse: sudo python3 setup.py\033[0m")
        sys.exit(1)

def detect_mode():
    """Detecta se está rodando local ou remoto"""
    # Por enquanto sempre local, remoto será implementado depois
    return "local"

def load_config():
    """Carrega ou cria configuração inicial"""
    config_path = Path("config.json")
    
    if config_path.exists():
        with open(config_path, 'r') as f:
            return json.load(f)
    else:
        # Config inicial
        config = {
            "version": "0.1",
            "global": {
                "domain": "",
                "admin_email": "",
                "docker_network": "livchat_network"
            },
            "applications": {}
        }
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        return config

def main():
    """Função principal"""
    try:
        # Importa módulos após verificações
        from core.cli import CLIParser
        from core.logger import Logger
        from core.menu import InteractiveMenu
        
        # Parse argumentos
        parser = CLIParser()
        args = parser.parse_args()
        
        # Configura logger
        logger = Logger(dev_mode=args.dev)
        
        # Verifica root
        check_root()
        
        # Carrega config
        config = load_config()
        
        # Detecta modo
        mode = detect_mode()
        
        # Se não passou comando específico, mostra menu
        if args.command is None:
            logger.clear()
            menu = InteractiveMenu(logger, config, mode)
            menu.run()
        else:
            # Executa comando específico (implementar depois)
            if args.command == "install":
                logger.info(f"Instalando {args.app}")
                # TODO: Implementar instalação direta
            elif args.command == "list":
                logger.info("Listando aplicações disponíveis")
                # TODO: Implementar listagem
            elif args.command == "status":
                logger.info("Verificando status dos serviços")
                # TODO: Implementar status
            else:
                logger.error(f"Comando desconhecido: {args.command}")
                sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n\033[90m\nInstalação cancelada pelo usuário\033[0m")
        sys.exit(0)
    except ImportError as e:
        print(f"\033[91m✗ Erro ao importar módulo: {e}\033[0m")
        print("\033[90mExecute: bash install.sh\033[0m")
        sys.exit(1)
    except Exception as e:
        if '--dev' in sys.argv:
            import traceback
            print(f"\033[91m[ERROR] {e}\033[0m")
            traceback.print_exc()
        else:
            print(f"\033[91m✗ Erro: {e}\033[0m")
        sys.exit(1)

if __name__ == "__main__":
    main()