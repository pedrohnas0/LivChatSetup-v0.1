"""
CLI Parser - LivChat Setup v0.1
Parser de argumentos da linha de comando
"""

import argparse
import sys

class CLIParser:
    """Parser de linha de comando para o LivChat Setup"""
    
    def __init__(self):
        self.parser = self._create_parser()
    
    def _create_parser(self):
        """Cria o parser principal com subcomandos"""
        parser = argparse.ArgumentParser(
            prog='setup.py',
            description='LivChat Setup v0.1 - Sistema modular para deploy de aplicações Docker',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Exemplos:
  python3 setup.py                    # Menu interativo
  python3 setup.py --dev               # Modo desenvolvimento
  python3 setup.py install n8n        # Instala N8N diretamente
  python3 setup.py install n8n --instance dev  # Instala N8N dev
  python3 setup.py list                # Lista aplicações disponíveis
  python3 setup.py status              # Status dos serviços
            """
        )
        
        # Argumentos globais
        parser.add_argument(
            '--dev',
            action='store_true',
            help='Modo desenvolvimento com logs completos'
        )
        
        parser.add_argument(
            '--version',
            action='version',
            version='%(prog)s v0.1-beta'
        )
        
        # Subcomandos
        subparsers = parser.add_subparsers(dest='command', help='Comandos disponíveis')
        
        # Comando install
        install_parser = subparsers.add_parser(
            'install',
            help='Instala uma aplicação'
        )
        install_parser.add_argument(
            'app',
            help='Nome da aplicação para instalar'
        )
        install_parser.add_argument(
            '--instance',
            default='default',
            help='Nome da instância (para multi-instância)'
        )
        
        # Comando list
        list_parser = subparsers.add_parser(
            'list',
            help='Lista aplicações disponíveis'
        )
        list_parser.add_argument(
            '--installed',
            action='store_true',
            help='Mostra apenas aplicações instaladas'
        )
        
        # Comando status
        status_parser = subparsers.add_parser(
            'status',
            help='Mostra status dos serviços'
        )
        status_parser.add_argument(
            '--app',
            help='Status de uma aplicação específica'
        )
        
        # Comando add-server (para modo remoto futuro)
        server_parser = subparsers.add_parser(
            'add-server',
            help='Adiciona servidor remoto (futuro)'
        )
        
        # Comando use (para modo remoto futuro)
        use_parser = subparsers.add_parser(
            'use',
            help='Seleciona servidor para usar (futuro)'
        )
        use_parser.add_argument(
            'server',
            help='Nome ou ID do servidor'
        )
        
        return parser
    
    def parse_args(self):
        """Parse dos argumentos da linha de comando"""
        args = self.parser.parse_args()
        
        # Se não passou nenhum comando e não é --version, assume menu interativo
        if args.command is None and '--version' not in sys.argv:
            args.menu = True
        else:
            args.menu = False
        
        return args
    
    def print_help(self):
        """Imprime ajuda"""
        self.parser.print_help()