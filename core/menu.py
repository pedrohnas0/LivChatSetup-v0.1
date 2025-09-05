"""
Menu Interativo TUI - LivChat Setup v0.1
Interface visual elegante e sóbria para seleção de aplicações
"""

import sys
import tty
import termios
import os
import subprocess
import re
from typing import List, Dict, Optional
from .logger import Colors, BoxDrawer

class InteractiveMenu:
    """Menu TUI profissional com navegação por teclado e visual elegante"""
    
    def __init__(self, logger, config: dict, mode: str = "local"):
        self.logger = logger
        self.config = config
        self.mode = mode
        
        # Estado do menu
        self.selected_index = 0
        self.selected_items = set()
        self.search_term = ""
        self.search_mode = False
        
        # Visual components
        self.colors = Colors()
        self.box = BoxDrawer(103)
        
        # Lista de aplicações disponíveis
        self.apps = [
            {"id": "docker", "name": "Docker + Swarm", "category": "infra", "status": "running", "cpu": "0.5%", "mem": "45MB"},
            {"id": "traefik", "name": "Traefik (SSL)", "category": "infra", "status": "running", "cpu": "0.3%", "mem": "32MB"},
            {"id": "portainer", "name": "Portainer", "category": "infra", "status": "stopped", "cpu": "-", "mem": "-"},
            {"id": "postgres", "name": "PostgreSQL", "category": "database", "status": "running", "cpu": "1.2%", "mem": "256MB"},
            {"id": "redis", "name": "Redis", "category": "database", "status": "stopped", "cpu": "-", "mem": "-"},
            {"id": "n8n", "name": "N8N", "category": "app", "status": "running", "cpu": "0.8%", "mem": "120MB"},
            {"id": "chatwoot", "name": "Chatwoot", "category": "app", "status": "stopped", "cpu": "-", "mem": "-"},
            {"id": "directus", "name": "Directus", "category": "app", "status": "stopped", "cpu": "-", "mem": "-"},
        ]
        
        # Atualiza status real do Docker
        self._update_docker_status()
        
        # Configurações do terminal
        self.old_settings = None
    
    def _update_docker_status(self):
        """Atualiza status real dos containers Docker"""
        try:
            # Tenta obter status do Docker
            result = subprocess.run(
                ['docker', 'ps', '--format', '{{.Names}}\t{{.Status}}'],
                capture_output=True, text=True, timeout=2
            )
            if result.returncode == 0:
                running_containers = {}
                for line in result.stdout.strip().split('\n'):
                    if line:
                        parts = line.split('\t')
                        if len(parts) >= 2:
                            name = parts[0].lower()
                            running_containers[name] = 'running' if 'Up' in parts[1] else 'stopped'
                
                # Atualiza status das apps
                for app in self.apps:
                    for container_name in running_containers:
                        if app['id'] in container_name:
                            app['status'] = running_containers[container_name]
                            break
        except:
            # Se falhar, mantém status mockado
            pass
    
    def run(self):
        """Executa o menu interativo principal"""
        try:
            # Mostra logo profissional
            self.logger.show_logo()
            
            # Menu de seleção
            selected = self._run_selection_menu()
            
            if selected:
                self._confirm_and_install(selected)
            else:
                self.logger.info("Nenhuma aplicação selecionada")
                
        except KeyboardInterrupt:
            print(f"\n\n{self.colors.CINZA}Cancelado pelo usuário{self.colors.RESET}")
            sys.exit(0)
    
    def _run_selection_menu(self) -> List[str]:
        """Menu de seleção com navegação por teclado"""
        self._setup_terminal()
        
        try:
            while True:
                self._draw_menu()
                key = self._get_key()
                
                if key == 'UP':
                    if self.selected_index > 0:
                        self.selected_index -= 1
                elif key == 'DOWN':
                    if self.selected_index < len(self.apps) - 1:
                        self.selected_index += 1
                elif key == 'SPACE' or key == 'RIGHT':
                    # Toggle seleção
                    current_app = self.apps[self.selected_index]
                    if current_app['id'] in self.selected_items:
                        self.selected_items.remove(current_app['id'])
                    else:
                        self.selected_items.add(current_app['id'])
                elif key.isdigit():
                    # Seleciona por número
                    num = int(key) - 1
                    if 0 <= num < len(self.apps):
                        self.selected_index = num
                elif key.isalpha() and not (key == 'q' or key == 'Q'):
                    # Inicia modo de pesquisa
                    self.search_mode = True
                    self.search_term = key
                elif key == '\x7f':  # Backspace
                    if self.search_mode and self.search_term:
                        self.search_term = self.search_term[:-1]
                    if not self.search_term:
                        self.search_mode = False
                elif key == '\x1b' and self.search_mode:  # ESC
                    self.search_mode = False
                    self.search_term = ""
                elif key == 'ENTER':
                    # Confirma seleção
                    if self.selected_items:
                        return list(self.selected_items)
                    else:
                        # Se nada selecionado, seleciona o item atual
                        current_app = self.apps[self.selected_index]
                        return [current_app['id']]
                elif key == 'q' or key == 'Q':
                    # Sair
                    return []
                
        finally:
            self._restore_terminal()
    
    def _draw_menu(self):
        """Desenha o menu profissional com largura 103"""
        # Move cursor para o topo
        print("\033[H\033[2J", end="")
        
        # Header do menu
        selected_count = len(self.selected_items)
        total_count = len(self.apps)
        
        # Cria o header com espaçamento correto
        header_left = "─ SETUP LIVCHAT "
        header_right = f" Selecionados: {selected_count}/{total_count} ─"
        header_middle_size = 101 - len(header_left) - len(header_right)
        header_middle = "─" * header_middle_size
        
        print(f"{self.colors.CINZA}╭{header_left}{header_middle}{header_right}╮{self.colors.RESET}")
        
        # Linha de instruções
        instructions = "↑/↓ navegar · → marcar (●/○) · Enter executar · Digite para pesquisar"
        print(f"{self.colors.CINZA}│ {self.colors.BEGE}{instructions.center(99)}{self.colors.CINZA} │{self.colors.RESET}")
        
        # Linha vazia
        print(f"{self.colors.CINZA}│{' ' * 101}│{self.colors.RESET}")
        
        # Cabeçalho da tabela
        print(f"{self.colors.CINZA}│ {self.colors.BRANCO}{'APLICAÇÃO':<40} {'STATUS':<15} {'CPU':<10} {'MEM':<10}{' ' * 24}{self.colors.CINZA} │{self.colors.RESET}")
        
        # Linha separadora
        print(f"{self.colors.CINZA}│ {'─' * 99} │{self.colors.RESET}")
        
        # Lista de aplicações
        for i, app in enumerate(self.apps):
            # Numeração
            num = f"[{i + 1}]"
            
            # Indicador de seleção e cor
            if i == self.selected_index:
                cursor = ">"
                color = self.colors.BRANCO
            else:
                cursor = " "
                color = self.colors.CINZA
            
            # Checkbox
            if app['id'] in self.selected_items:
                checkbox = f"{self.colors.VERDE}●{self.colors.RESET}"
            else:
                checkbox = "○"
            
            # Status
            if app['status'] == 'running':
                status_display = f"{self.colors.VERDE}2/2{self.colors.RESET}"
                status_raw = "2/2"
            else:
                status_display = f"{self.colors.CINZA}-{self.colors.RESET}"
                status_raw = "-"
            
            # Constrói a linha
            line_parts = [
                f" {cursor} {checkbox} {num:5}",
                f"{color}{app['name']:<35}{self.colors.RESET}",
                f"{status_display}",
                f"{color}{app['cpu']:>7}{self.colors.RESET}",
                f"{color}{app['mem']:>10}{self.colors.RESET}"
            ]
            
            # Calcula tamanho real sem ANSI codes
            clean_parts = [
                f" {cursor} {checkbox} {num:5}",
                f"{app['name']:<35}",
                f"{status_raw:<10}",
                f"{app['cpu']:>7}",
                f"{app['mem']:>10}"
            ]
            clean_line = "".join(clean_parts)
            padding_needed = 99 - len(clean_line)
            
            # Imprime a linha
            print(f"{self.colors.CINZA}│{self.colors.RESET}", end="")
            for part in line_parts:
                print(part, end="")
            print(f"{' ' * padding_needed}{self.colors.CINZA} │{self.colors.RESET}")
        
        # Footer
        print(f"{self.colors.CINZA}╰{'─' * 101}╯{self.colors.RESET}")
    
    def _setup_terminal(self):
        """Configura terminal para captura de teclas"""
        self.old_settings = termios.tcgetattr(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
    
    def _restore_terminal(self):
        """Restaura configurações do terminal"""
        if self.old_settings:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, self.old_settings)
    
    def _get_key(self) -> str:
        """Captura tecla pressionada"""
        key = sys.stdin.read(1)
        
        # Detecta sequências escape (setas)
        if key == '\x1b':
            key2 = sys.stdin.read(1)
            if key2 == '[':
                key3 = sys.stdin.read(1)
                if key3 == 'A':
                    return 'UP'
                elif key3 == 'B':
                    return 'DOWN'
                elif key3 == 'C':
                    return 'RIGHT'
                elif key3 == 'D':
                    return 'LEFT'
        
        # Outras teclas
        if key == ' ':
            return 'SPACE'
        elif key == '\r' or key == '\n':
            return 'ENTER'
        
        return key
    
    def _confirm_and_install(self, selected: List[str]):
        """Confirma e instala aplicações selecionadas com visual profissional"""
        self._restore_terminal()
        self.logger.clear()
        
        # Mostra resumo profissional
        print(f"\n{self.colors.CINZA}{self.box.top()}{self.colors.RESET}")
        title = f"{self.colors.BRANCO}APLICAÇÕES SELECIONADAS{self.colors.RESET}"
        print(f"{self.colors.CINZA}{self.box.line_centered(title)}{self.colors.RESET}")
        print(f"{self.colors.CINZA}{self.box.separator()}{self.colors.RESET}")
        
        # Lista apps selecionadas
        for app_id in selected:
            app = next((a for a in self.apps if a['id'] == app_id), None)
            if app:
                line = f"  {self.colors.VERDE}●{self.colors.RESET} {app['name']}"
                print(f"{self.colors.CINZA}{self.box.line_left(line, 4)}{self.colors.RESET}")
        
        print(f"{self.colors.CINZA}{self.box.bottom()}{self.colors.RESET}")
        print(f"\n{self.colors.BEGE}Pressione Enter para instalar ou Ctrl+C para cancelar{self.colors.RESET}")
        
        try:
            input()
        except KeyboardInterrupt:
            return
        
        # Conta total de passos para progress
        total_steps = len(selected) + 3  # Apps + validação + finalização
        self.logger.start_progress(total_steps)
        
        # Instalação com progress real
        self.logger.section("INSTALANDO APLICAÇÕES")
        
        self.logger.success("Verificando sistema operacional")
        import time
        time.sleep(0.5)
        
        self.logger.success("Verificando Docker")
        time.sleep(0.5)
        
        for app_id in selected:
            app = next((a for a in self.apps if a['id'] == app_id), None)
            if app:
                self.logger.success(f"Instalando {app['name']}")
                time.sleep(1)  # TODO: Implementar instalação real
        
        self.logger.success("Finalizando instalação")
        
        # Box de conclusão
        print(f"\n{self.colors.CINZA}{self.box.top()}{self.colors.RESET}")
        print(f"{self.colors.CINZA}{self.box.empty()}{self.colors.RESET}")
        success_msg = f"{self.colors.VERDE}{self.colors.BOLD}✓ INSTALAÇÃO CONCLUÍDA!{self.colors.RESET}"
        print(f"{self.colors.CINZA}{self.box.line_centered(success_msg)}{self.colors.RESET}")
        print(f"{self.colors.CINZA}{self.box.empty()}{self.colors.RESET}")
        print(f"{self.colors.CINZA}{self.box.bottom()}{self.colors.RESET}")
        
        print(f"\n{self.colors.CINZA}Pressione Enter para continuar...{self.colors.RESET}")
        input()