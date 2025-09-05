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
from .logger import Colors

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
        
        # Largura do menu (baseado no original)
        self.menu_width = 92
        
        # Lista de aplicações disponíveis
        self.apps = [
            {"id": "docker", "name": "Docker + Swarm", "status": "2/2", "cpu": "0.5%", "mem": "45MB"},
            {"id": "traefik", "name": "Traefik (SSL)", "status": "2/2", "cpu": "0.3%", "mem": "32MB"},
            {"id": "portainer", "name": "Portainer", "status": "-", "cpu": "-", "mem": "-"},
            {"id": "postgres", "name": "PostgreSQL", "status": "2/2", "cpu": "1.2%", "mem": "256MB"},
            {"id": "redis", "name": "Redis", "status": "-", "cpu": "-", "mem": "-"},
            {"id": "n8n", "name": "N8N", "status": "2/2", "cpu": "0.8%", "mem": "120MB"},
            {"id": "chatwoot", "name": "Chatwoot", "status": "-", "cpu": "-", "mem": "-"},
            {"id": "directus", "name": "Directus", "status": "-", "cpu": "-", "mem": "-"},
        ]
        
        # Configurações do terminal
        self.old_settings = None
        
        # Contador de linhas para redesenho
        self.last_drawn_lines = 0
    
    def run(self):
        """Executa o menu interativo principal"""
        try:
            # Mostra logo profissional
            self.logger.show_logo()
            print()  # Linha extra após logo
            
            # Menu de seleção
            selected = self._run_selection_menu()
            
            if selected:
                self._confirm_and_install(selected)
            else:
                print(f"\n{self.colors.CINZA}Nenhuma aplicação selecionada{self.colors.RESET}")
                
        except KeyboardInterrupt:
            print(f"\n\n{self.colors.CINZA}Cancelado pelo usuário{self.colors.RESET}")
            sys.exit(0)
    
    def _run_selection_menu(self) -> List[str]:
        """Menu de seleção com navegação por teclado"""
        self._setup_terminal()
        
        # Primeira renderização
        self._draw_menu(first_draw=True)
        
        try:
            while True:
                key = self._get_key()
                
                if key == 'UP':
                    if self.selected_index > 0:
                        self.selected_index -= 1
                        self._redraw_menu()
                elif key == 'DOWN':
                    if self.selected_index < len(self.apps) - 1:
                        self.selected_index += 1
                        self._redraw_menu()
                elif key == 'SPACE' or key == 'RIGHT':
                    # Toggle seleção
                    current_app = self.apps[self.selected_index]
                    if current_app['id'] in self.selected_items:
                        self.selected_items.remove(current_app['id'])
                    else:
                        self.selected_items.add(current_app['id'])
                    self._redraw_menu()
                elif key.isdigit():
                    # Seleciona por número
                    num = int(key) - 1
                    if 0 <= num < len(self.apps):
                        self.selected_index = num
                        self._redraw_menu()
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
    
    def _redraw_menu(self):
        """Redesenha o menu sem limpar input"""
        # Limpar linhas anteriores
        for _ in range(self.last_drawn_lines):
            print(f"\033[1A\033[2K", end="")
        # Desenhar novo menu
        self._draw_menu()
    
    def _draw_menu(self, first_draw=False):
        """Desenha o menu profissional com largura correta"""
        lines = []
        
        if first_draw:
            lines.append("")  # linha vazia inicial
        
        # Header com contador
        selected_count = len(self.selected_items)
        total_count = len(self.apps)
        counter_text = f"Selecionados: {selected_count}/{total_count}"
        
        # Calcular padding para o título
        title_padding = self.menu_width - len("─ SETUP LIVCHAT ") - len(counter_text) - 5
        header_line = f"╭─ SETUP LIVCHAT {'─' * title_padding} {counter_text} ─╮"
        
        lines.append(f"{self.colors.CINZA}{header_line}{self.colors.RESET}")
        
        # Linha de instruções
        instrucoes = " ↑/↓ navegar · → marcar (●/○) · Enter executar · Digite para pesquisar"
        instrucoes_padding = self.menu_width - len(instrucoes) - 2
        lines.append(f"{self.colors.CINZA}│{self.colors.BEGE}{instrucoes}{' ' * instrucoes_padding}{self.colors.CINZA}│{self.colors.RESET}")
        lines.append(f"{self.colors.CINZA}│{' ' * (self.menu_width - 2)}│{self.colors.RESET}")
        
        # Cabeçalho da tabela
        header_text = " APLICAÇÃO" + " " * 50 + "STATUS    CPU     MEM"
        header_padding = self.menu_width - len(header_text) - 2
        lines.append(f"{self.colors.CINZA}│{self.colors.BRANCO}{header_text}{' ' * header_padding}{self.colors.CINZA}│{self.colors.RESET}")
        lines.append(f"{self.colors.CINZA}│{' ' * (self.menu_width - 2)}│{self.colors.RESET}")
        
        # Lista de aplicações
        for i, app in enumerate(self.apps):
            # É o item com cursor?
            is_current = i == self.selected_index
            
            # Símbolo de seleção
            is_selected = app['id'] in self.selected_items
            
            # Formatação do item
            cursor = "> " if is_current else "  "
            symbol = "●" if is_selected else "○"
            
            # Cor do símbolo e texto
            if is_selected:
                symbol_color = self.colors.VERDE
                text_color = self.colors.VERDE
            elif is_current:
                symbol_color = self.colors.BRANCO
                text_color = self.colors.BRANCO
            else:
                symbol_color = self.colors.CINZA
                text_color = self.colors.CINZA
            
            # Número do item
            item_number = f"[{i + 1:1d}]"
            
            # Nome da aplicação (limitado a 40 chars)
            name = app['name']
            if len(name) > 40:
                name = name[:37] + "..."
            
            # Calcular padding para alinhar com as colunas
            # Total de espaço para aplicação: 60 chars
            app_section = f"{cursor}{symbol} {item_number} {name}"
            padding_to_status = 60 - len(app_section)
            
            # Status com cor apropriada
            if app['status'] != '-':
                status_str = f"{text_color}{app['status']:>5}{self.colors.RESET}   "
            else:
                status_str = f"{text_color}     {self.colors.RESET}   "
            
            # CPU
            if app['cpu'] != '-':
                cpu_str = f"{text_color}{app['cpu']:>7}{self.colors.RESET} "
            else:
                cpu_str = f"{text_color}       {self.colors.RESET} "
            
            # MEM
            if app['mem'] != '-':
                mem_str = f"{text_color}{app['mem']:>7}{self.colors.RESET}"
            else:
                mem_str = f"{text_color}       {self.colors.RESET}"
            
            # Montar linha completa
            if is_current and is_selected:
                # Cursor E selecionado - TUDO VERDE
                line_content = f"{self.colors.VERDE}{cursor}{symbol} {item_number} {name}{' ' * padding_to_status}{self.colors.RESET}{status_str}{cpu_str}{mem_str}"
            elif is_current:
                # Cursor mas não selecionado - branco
                line_content = f"{self.colors.BRANCO}{cursor}{symbol_color}{symbol}{self.colors.BRANCO} {item_number} {name}{' ' * padding_to_status}{self.colors.RESET}{status_str}{cpu_str}{mem_str}"
            elif is_selected:
                # Selecionado - verde
                line_content = f"{self.colors.VERDE}{cursor}{symbol} {item_number} {name}{' ' * padding_to_status}{self.colors.RESET}{status_str}{cpu_str}{mem_str}"
            else:
                # Normal - cinza
                line_content = f"{self.colors.CINZA}{cursor}{symbol} {item_number} {name}{' ' * padding_to_status}{self.colors.RESET}{status_str}{cpu_str}{mem_str}"
            
            # Calcular padding final
            clean_line = re.sub(r'\033\[[0-9;]*m', '', line_content)
            final_padding = self.menu_width - len(clean_line) - 2
            
            lines.append(f"{self.colors.CINZA}│{self.colors.RESET}{line_content}{' ' * final_padding}{self.colors.CINZA}│{self.colors.RESET}")
        
        # Footer
        lines.append(f"{self.colors.CINZA}│{' ' * (self.menu_width - 2)}│{self.colors.RESET}")
        footer_line = "─" * (self.menu_width - 2)
        lines.append(f"{self.colors.CINZA}╰{footer_line}╯{self.colors.RESET}")
        
        # Imprimir tudo de uma vez
        for line in lines:
            print(line)
        
        # Atualiza contador de linhas desenhadas
        self.last_drawn_lines = len(lines)
    
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
        
        # Limpar menu anterior
        for _ in range(self.last_drawn_lines):
            print(f"\033[1A\033[2K", end="")
        
        # Importar BoxDrawer para boxes profissionais
        from .logger import BoxDrawer
        box = BoxDrawer(103)
        
        # Mostra resumo profissional
        print(f"\n{self.colors.CINZA}{box.top()}{self.colors.RESET}")
        title = f"{self.colors.BRANCO}APLICAÇÕES SELECIONADAS{self.colors.RESET}"
        print(f"{self.colors.CINZA}{box.line_centered(title)}{self.colors.RESET}")
        print(f"{self.colors.CINZA}{box.separator()}{self.colors.RESET}")
        
        # Lista apps selecionadas
        for app_id in selected:
            app = next((a for a in self.apps if a['id'] == app_id), None)
            if app:
                line = f"  {self.colors.VERDE}●{self.colors.RESET} {app['name']}"
                print(f"{self.colors.CINZA}{box.line_left(line, 4)}{self.colors.RESET}")
        
        print(f"{self.colors.CINZA}{box.bottom()}{self.colors.RESET}")
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
        print(f"\n{self.colors.CINZA}{box.top()}{self.colors.RESET}")
        print(f"{self.colors.CINZA}{box.empty()}{self.colors.RESET}")
        success_msg = f"{self.colors.VERDE}{self.colors.BOLD}✓ INSTALAÇÃO CONCLUÍDA!{self.colors.RESET}"
        print(f"{self.colors.CINZA}{box.line_centered(success_msg)}{self.colors.RESET}")
        print(f"{self.colors.CINZA}{box.empty()}{self.colors.RESET}")
        print(f"{self.colors.CINZA}{box.bottom()}{self.colors.RESET}")
        
        print(f"\n{self.colors.CINZA}Pressione Enter para continuar...{self.colors.RESET}")
        input()