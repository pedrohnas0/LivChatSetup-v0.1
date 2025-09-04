# 📋 PLANEJAMENTO-01: Bootstrap e Sistema de Logs

**Data:** 2024  
**Versão:** 2.0  
**Status:** Refinando abordagem

---

## 🎯 **OBJETIVO**

Criar sistema de logs elegante e sóbrio: visual limpo em produção, completo em desenvolvimento.

---

## 💡 **INSIGHT DO ORION**

Analisando o SetupOrion:
- **Não tem modo debug explícito** - sempre roda igual
- **Visual simples**: usa ✓ verde e ✗ vermelho
- **Sem emojis exagerados** - apenas símbolos básicos
- **Foco na elegância** - boxes bem desenhados

---

## 📊 **SISTEMA DE LOGS - ABORDAGEM REFINADA**

### **PRODUÇÃO (padrão) - Interface Elegante**

```bash
./setup.py
```

**Características:**
- Interface visual limpa e animada
- Feedback mínimo mas claro
- Cores sóbrias (sem arco-íris)
- Símbolos simples: ✓ ✗ ◌ ●
- Clear screen entre etapas importantes
- Erros mostrados de forma elegante

**Exemplo visual:**
```
╭─────────────────────────────────────────╮
│         Instalando Traefik...           │
╰─────────────────────────────────────────╯

  ◌ Criando rede Docker
  ◌ Aplicando configurações
  ◌ Iniciando serviços

╭─────────────────────────────────────────╮
│     ✓ Traefik instalado com sucesso     │
│                                         │
│     Acesse: traefik.example.com        │
╰─────────────────────────────────────────╯
```

### **DESENVOLVIMENTO (--dev) - Logs Completos**

```bash
./setup.py --dev
```

**Características:**
- NUNCA limpa tela
- Mostra todos os comandos
- Timestamps e níveis de log
- Stack traces completas
- Output completo para debug

**Exemplo:**
```
[2024-01-01 10:00:00] Starting Traefik installation
[2024-01-01 10:00:01] Running: docker network create livchat
[2024-01-01 10:00:01] Output: network_id_xyz123
[2024-01-01 10:00:01] Return: 0
[2024-01-01 10:00:02] Applying template: traefik.yaml.j2
[2024-01-01 10:00:03] Running: docker stack deploy -c traefik.yaml traefik
[2024-01-01 10:00:05] Success: Traefik installed
```

---

## 🎨 **DESIGN VISUAL - ABORDAGEM SÓBRIA**

### **Paleta de Cores (Minimalista)**

```python
# Apenas o essencial
VERDE = "\033[32m"     # Sucesso
VERMELHO = "\033[91m"  # Erro  
CINZA = "\033[90m"     # Bordas e info secundária
BRANCO = "\033[97m"    # Texto principal
RESET = "\033[0m"      # Reset

# Evitar:
# - Amarelo, laranja, roxo (muito colorido)
# - Emojis complexos
# - Múltiplas cores na mesma linha
```

### **Símbolos (Simples e Elegantes)**

```python
# Usar com moderação
SYMBOLS = {
    'success': '✓',     # Sucesso
    'error': '✗',       # Erro
    'pending': '◌',     # Aguardando
    'active': '●',      # Ativo/Selecionado
    'arrow': '→',       # Indicador
    'info': 'ⓘ',       # Informação (raramente)
}

# Evitar emojis como:
# ❌ 🚀 💡 🔥 🎯 ⚡ 🎉 (muito informal)
```

### **Boxes (Estilo Orion)**

```python
def print_box(message: str, status: str = "info"):
    """Box elegante estilo Orion"""
    width = max(len(message) + 4, 45)
    line = "─" * (width - 2)
    
    print(f"{CINZA}╭{line}╮{RESET}")
    
    if status == "success":
        symbol = f"{VERDE}✓{RESET}"
    elif status == "error":
        symbol = f"{VERMELHO}✗{RESET}"
    else:
        symbol = " "
    
    centered = f"{symbol} {message}".center(width - 2)
    print(f"{CINZA}│{RESET}{centered}{CINZA}│{RESET}")
    print(f"{CINZA}╰{line}╯{RESET}")
```

---

## 🔧 **IMPLEMENTAÇÃO DO LOGGER**

### **core/logger.py - Versão Sóbria**

```python
import os
import sys
from datetime import datetime

class Logger:
    """Logger elegante com dois modos: produção visual e desenvolvimento completo"""
    
    def __init__(self, dev_mode: bool = False):
        """
        Args:
            dev_mode: True para desenvolvimento, False para produção
        """
        self.dev = dev_mode
        self.can_clear = not dev_mode and sys.stdout.isatty()
        
        # Cores mínimas
        self.GREEN = '\033[32m'
        self.RED = '\033[91m'
        self.GRAY = '\033[90m'
        self.WHITE = '\033[97m'
        self.RESET = '\033[0m'
    
    def clear(self):
        """Limpa tela apenas em produção"""
        if self.can_clear:
            os.system('clear' if os.name != 'nt' else 'cls')
    
    def section(self, title: str):
        """Início de nova seção"""
        if self.dev:
            print(f"\n[{self._timestamp()}] === {title.upper()} ===")
        else:
            self.clear()
            self._draw_box(title)
    
    def success(self, message: str):
        """Mensagem de sucesso"""
        if self.dev:
            print(f"[{self._timestamp()}] Success: {message}")
        else:
            print(f"  {self.GREEN}✓{self.RESET} {message}")
    
    def error(self, message: str):
        """Mensagem de erro"""
        if self.dev:
            print(f"[{self._timestamp()}] Error: {message}")
        else:
            self._draw_box(f"✗ {message}", error=True)
    
    def step(self, message: str):
        """Passo em progresso"""
        if self.dev:
            print(f"[{self._timestamp()}] Step: {message}")
        else:
            print(f"  {self.GRAY}◌{self.RESET} {message}")
    
    def info(self, message: str):
        """Informação - só em dev"""
        if self.dev:
            print(f"[{self._timestamp()}] Info: {message}")
    
    def command(self, cmd: str, output: str = None, code: int = None):
        """Log de comando - só em dev"""
        if self.dev:
            print(f"[{self._timestamp()}] Running: {cmd}")
            if output:
                for line in output.split('\n')[:10]:  # Limita linhas
                    if line.strip():
                        print(f"[{self._timestamp()}] Output: {line}")
            if code is not None:
                print(f"[{self._timestamp()}] Return: {code}")
    
    def debug(self, message: str):
        """Debug - só em dev"""
        if self.dev:
            print(f"[{self._timestamp()}] Debug: {message}")
    
    def _timestamp(self) -> str:
        """Timestamp para modo dev"""
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def _draw_box(self, message: str, error: bool = False):
        """Desenha box elegante"""
        width = max(len(message) + 4, 45)
        line = "─" * (width - 2)
        color = self.RED if error else self.GRAY
        
        print(f"\n{color}╭{line}╮{self.RESET}")
        centered = message.center(width - 2)
        print(f"{color}│{self.RESET}{centered}{color}│{self.RESET}")
        print(f"{color}╰{line}╯{self.RESET}\n")
```

---

## 📋 **CENÁRIOS DE USO**

### **Cenário 1: Instalação Normal (Produção)**

```bash
./setup.py
```

**Usuário vê:**
```
╭─────────────────────────────────────────╮
│       Verificando pré-requisitos        │
╰─────────────────────────────────────────╯

  ✓ Docker instalado
  ✓ Portas disponíveis
  ◌ Iniciando instalação...

╭─────────────────────────────────────────╮
│         Instalação concluída            │
│                                         │
│    Acesse: portainer.example.com       │
╰─────────────────────────────────────────╯
```

### **Cenário 2: Erro em Produção (Elegante)**

```bash
./setup.py
```

**Usuário vê:**
```
╭─────────────────────────────────────────╮
│       ✗ Porta 5432 já em uso           │
│                                         │
│   Verifique se PostgreSQL já está      │
│   rodando e tente novamente.           │
╰─────────────────────────────────────────╯
```

### **Cenário 3: Desenvolvimento**

```bash
./setup.py --dev
```

**Desenvolvedor vê tudo:**
```
[2024-01-01 10:00:00] Starting setup.py with args: ['--dev']
[2024-01-01 10:00:00] === CHECKING PREREQUISITES ===
[2024-01-01 10:00:00] Running: docker --version
[2024-01-01 10:00:00] Output: Docker version 24.0.7, build afdd53b
[2024-01-01 10:00:00] Return: 0
[2024-01-01 10:00:00] Success: Docker is installed
```

---

## ✅ **PRINCÍPIOS DE DESIGN**

### **DO's - Fazer:**
- ✓ Usar no máximo 3 cores por tela
- ✓ Preferir símbolos simples (✓ ✗ ◌ ●)
- ✓ Boxes para mensagens importantes
- ✓ Clear screen entre seções principais
- ✓ Mensagens concisas e diretas

### **DON'Ts - Evitar:**
- ✗ Emojis coloridos e chamativos
- ✗ Múltiplas cores na mesma linha
- ✗ Animações exageradas
- ✗ Textos muito longos
- ✗ Debug info em produção

---

## 🎯 **TRATAMENTO DE ERROS**

### **Produção - Mensagem Amigável:**
```python
try:
    # código
except PortInUseError:
    logger.error("Porta já está em uso")
    logger.info("Tente: sudo netstat -tlnp | grep 5432")
```

### **Desenvolvimento - Stack Completa:**
```python
try:
    # código
except Exception as e:
    if logger.dev:
        import traceback
        logger.debug(f"Exception: {e}")
        logger.debug(traceback.format_exc())
    else:
        logger.error("Falha na instalação")
```

---

## 📝 **CHECKLIST FINAL**

### **Implementação:**
- [ ] Logger com 2 modos (prod/dev)
- [ ] Máximo 3 cores (verde, vermelho, cinza)
- [ ] Símbolos simples (✓ ✗ ◌ ●)
- [ ] Boxes para destaque
- [ ] Clear screen inteligente

### **Evitar:**
- [ ] Sem emojis coloridos
- [ ] Sem arco-íris de cores
- [ ] Sem animações desnecessárias
- [ ] Sem debug em produção

### **Testar:**
- [ ] Visual em produção está limpo
- [ ] Erros aparecem claramente
- [ ] Modo dev mostra tudo
- [ ] Performance não afetada

---

**Esta abordagem mantém elegância em produção e funcionalidade em desenvolvimento.**