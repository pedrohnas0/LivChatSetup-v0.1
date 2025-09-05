"""
Sistema de Logs - LivChat Setup v0.1
Implementação baseada no método do projeto original para alinhamento perfeito
"""

import os
import sys
from datetime import datetime

class Colors:
    """Paleta de cores profissional como o projeto original"""
    # Principais
    LARANJA = "\033[38;5;173m"  # ASCII art e destaques
    VERDE = "\033[32m"          # Sucesso
    BRANCO = "\033[97m"         # Texto principal
    BEGE = "\033[93m"           # Informações secundárias
    VERMELHO = "\033[91m"       # Erros
    CINZA = "\033[90m"          # Bordas e decoração
    AZUL = "\033[34m"           # Links e info especial
    
    # Adicionais
    AMARELO = "\033[93m"        # Avisos
    RESET = "\033[0m"           # Reset
    BOLD = "\033[1m"            # Negrito

class BoxDrawer:
    """Sistema de boxes profissional com largura 103 - Método do projeto original"""
    
    def __init__(self, width: int = 103):
        self.width = width
        self.inner_width = width - 2  # 101 para largura total de 103
    
    def top(self) -> str:
        # Exatamente 103 caracteres (1 + 101 + 1)
        return f"╭{'─' * self.inner_width}╮"
    
    def bottom(self) -> str:
        # Exatamente 103 caracteres (1 + 101 + 1)
        return f"╰{'─' * self.inner_width}╯"
    
    def empty(self) -> str:
        # Exatamente 103 caracteres (1 + 101 espaços + 1)
        return f"│{' ' * self.inner_width}│"
    
    def line_centered(self, content: str) -> str:
        """
        Centraliza texto considerando cores ANSI
        Método idêntico ao projeto original
        """
        import re
        
        # Remove códigos ANSI para calcular tamanho real
        clean_content = re.sub(r'\x1b\[[0-9;]*m', '', content)
        content_length = len(clean_content)
        
        # Calcula espaçamento para centralizar
        total_padding = self.inner_width - content_length
        left_padding = total_padding // 2
        right_padding = total_padding - left_padding
        
        # Monta a linha com espaçamento calculado
        return f"│{' ' * left_padding}{content}{' ' * right_padding}│"
    
    def line_left(self, content: str, indent: int = 2) -> str:
        """Alinha texto à esquerda com indentação"""
        import re
        
        clean_content = re.sub(r'\x1b\[[0-9;]*m', '', content)
        content_length = len(clean_content)
        
        # Calcula padding à direita
        right_padding = self.inner_width - indent - content_length
        
        return f"│{' ' * indent}{content}{' ' * right_padding}│"
    
    def separator(self) -> str:
        return f"├{'─' * self.inner_width}┤"

class Progress:
    """Sistema de progresso com contadores"""
    
    def __init__(self, total: int):
        self.current = 0
        self.total = total
        self.colors = Colors()
    
    def step(self, message: str) -> str:
        self.current += 1
        symbol = f"{self.colors.VERDE}✓{self.colors.RESET}"
        counter = f"{self.colors.CINZA}{self.current}/{self.total}{self.colors.RESET}"
        return f"  {symbol} {counter} - {message}"
    
    def error(self, message: str) -> str:
        symbol = f"{self.colors.VERMELHO}✗{self.colors.RESET}"
        counter = f"{self.colors.CINZA}{self.current}/{self.total}{self.colors.RESET}"
        return f"  {symbol} {counter} - {message}"
    
    def pending(self, message: str) -> str:
        self.current += 1
        symbol = f"{self.colors.CINZA}◌{self.colors.RESET}"
        counter = f"{self.colors.CINZA}{self.current}/{self.total}{self.colors.RESET}"
        return f"  {symbol} {counter} - {message}"

class Logger:
    """Logger elegante com dois modos: produção visual e desenvolvimento completo"""
    
    def __init__(self, dev_mode: bool = False):
        """
        Args:
            dev_mode: True para desenvolvimento, False para produção
        """
        self.dev = dev_mode
        self.can_clear = not dev_mode and sys.stdout.isatty()
        self.colors = Colors()
        self.box = BoxDrawer(103)
        self.progress = None
    
    def clear(self):
        """Limpa tela apenas em produção"""
        if self.can_clear:
            os.system('clear' if os.name != 'nt' else 'cls')
    
    def show_logo(self):
        """Logo grande e imponente - Método do projeto original"""
        if not self.dev:
            self.clear()
            
            print(f"{self.colors.CINZA}{self.box.top()}{self.colors.RESET}")
            print(f"{self.colors.CINZA}{self.box.empty()}{self.colors.RESET}")
            print(f"{self.colors.CINZA}{self.box.empty()}{self.colors.RESET}")
            
            # IMPORTANTE: Logo com espaços extras para alinhamento (como no original)
            logo_lines = [
                f"{self.colors.LARANJA}     ██╗     ██╗██╗   ██╗ ██████╗██╗  ██╗ █████╗ ████████╗     {self.colors.RESET}",
                f"{self.colors.LARANJA}     ██║     ██║██║   ██║██╔════╝██║  ██║██╔══██╗╚══██╔══╝     {self.colors.RESET}",
                f"{self.colors.LARANJA}     ██║     ██║██║   ██║██║     ███████║███████║   ██║        {self.colors.RESET}",
                f"{self.colors.LARANJA}     ██║     ██║╚██╗ ██╔╝██║     ██╔══██║██╔══██║   ██║        {self.colors.RESET}",
                f"{self.colors.LARANJA}     ███████╗██║ ╚████╔╝ ╚██████╗██║  ██║██║  ██║   ██║        {self.colors.RESET}",
                f"{self.colors.LARANJA}     ╚══════╝╚═╝  ╚═══╝   ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝        {self.colors.RESET}"
            ]
            
            for line in logo_lines:
                print(f"{self.colors.CINZA}{self.box.line_centered(line)}{self.colors.RESET}")
            
            print(f"{self.colors.CINZA}{self.box.empty()}{self.colors.RESET}")
            print(f"{self.colors.CINZA}{self.box.line_centered(f'{self.colors.BRANCO}Setup Modular v0.1{self.colors.RESET}')}{self.colors.RESET}")
            print(f"{self.colors.CINZA}{self.box.empty()}{self.colors.RESET}")
            print(f"{self.colors.CINZA}{self.box.bottom()}{self.colors.RESET}")
            print()
    
    def section(self, title: str):
        """Início de nova seção"""
        if self.dev:
            print(f"\n[{self._timestamp()}] === {title.upper()} ===")
        else:
            print(f"\n{self.colors.CINZA}{self.box.top()}{self.colors.RESET}")
            print(f"{self.colors.CINZA}{self.box.line_centered(f'{self.colors.BRANCO}{title}{self.colors.RESET}')}{self.colors.RESET}")
            print(f"{self.colors.CINZA}{self.box.bottom()}{self.colors.RESET}\n")
    
    def start_progress(self, total: int):
        """Inicia contador de progresso"""
        if not self.dev:
            self.progress = Progress(total)
    
    def success(self, message: str):
        """Mensagem de sucesso"""
        if self.dev:
            print(f"[{self._timestamp()}] Success: {message}")
        else:
            if self.progress:
                print(self.progress.step(message))
            else:
                print(f"  {self.colors.VERDE}✓{self.colors.RESET} {message}")
    
    def error(self, message: str, hint: str = None):
        """Mensagem de erro"""
        if self.dev:
            print(f"[{self._timestamp()}] Error: {message}")
            if hint:
                print(f"[{self._timestamp()}] Hint: {hint}")
        else:
            if self.progress:
                print(self.progress.error(message))
            else:
                self._draw_error_box(message, hint)
    
    def step(self, message: str):
        """Passo em progresso"""
        if self.dev:
            print(f"[{self._timestamp()}] Step: {message}")
        else:
            if self.progress:
                print(self.progress.pending(message))
            else:
                print(f"  {self.colors.CINZA}◌{self.colors.RESET} {message}")
    
    def info(self, message: str):
        """Informação - só em dev"""
        if self.dev:
            print(f"[{self._timestamp()}] Info: {message}")
    
    def command(self, cmd: str, output: str = None, code: int = None):
        """Log de comando - só em dev"""
        if self.dev:
            print(f"[{self._timestamp()}] Running: {cmd}")
            if output:
                # Limita output para não poluir
                lines = output.strip().split('\n')
                for line in lines[:10]:
                    if line.strip():
                        print(f"[{self._timestamp()}] Output: {line}")
                if len(lines) > 10:
                    print(f"[{self._timestamp()}] Output: ... ({len(lines)-10} linhas omitidas)")
            if code is not None:
                print(f"[{self._timestamp()}] Return: {code}")
    
    def debug(self, message: str):
        """Debug - só em dev"""
        if self.dev:
            print(f"[{self._timestamp()}] Debug: {message}")
    
    def exception(self, e: Exception):
        """Log de exceção"""
        if self.dev:
            import traceback
            print(f"[{self._timestamp()}] Exception: {str(e)}")
            print(traceback.format_exc())
        else:
            self.error(f"Falha: {str(e)}")
    
    def _timestamp(self) -> str:
        """Timestamp para modo dev"""
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def _draw_box(self, message: str, color: str = None):
        """Desenha box elegante para produção"""
        if color is None:
            color = self.colors.CINZA
        
        print(f"\n{color}{self.box.top()}{self.colors.RESET}")
        print(f"{color}{self.box.line_centered(message)}{self.colors.RESET}")
        print(f"{color}{self.box.bottom()}{self.colors.RESET}\n")
    
    def _draw_error_box(self, message: str, hint: str = None):
        """Desenha box de erro elegante"""
        print(f"\n{self.colors.VERMELHO}{self.box.top()}{self.colors.RESET}")
        
        error_msg = f"{self.colors.VERMELHO}✗ {message}{self.colors.RESET}"
        print(f"{self.colors.VERMELHO}{self.box.line_centered(error_msg)}{self.colors.RESET}")
        
        if hint:
            print(f"{self.colors.VERMELHO}{self.box.empty()}{self.colors.RESET}")
            hint_msg = f"{self.colors.BEGE}{hint}{self.colors.RESET}"
            print(f"{self.colors.VERMELHO}{self.box.line_centered(hint_msg)}{self.colors.RESET}")
        
        print(f"{self.colors.VERMELHO}{self.box.bottom()}{self.colors.RESET}\n")
    
    def progress_bar(self, current: int, total: int, message: str = ""):
        """Barra de progresso simples - só em produção"""
        if not self.dev and total > 0:
            percent = int((current / total) * 100)
            bar_length = 30
            filled = int(bar_length * current / total)
            bar = "●" * filled + "◌" * (bar_length - filled)
            
            print(f"\r  {self.colors.CINZA}[{bar}] {percent}%{self.colors.RESET} {message}", end="")
            if current >= total:
                print()  # Nova linha quando completo