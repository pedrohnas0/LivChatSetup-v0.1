#!/bin/bash

################################################################################
#                         LIVCHAT SETUP v0.1 - Bootstrap                      #
################################################################################

# Cores sóbrias
VERDE="\033[32m"
VERMELHO="\033[91m"
CINZA="\033[90m"
BRANCO="\033[97m"
RESET="\033[0m"

# Verifica se é root
if [ "$(id -u)" -ne 0 ]; then
    echo -e "${VERMELHO}✗ Este script precisa ser executado como root${RESET}"
    echo -e "${CINZA}Use: sudo bash install.sh${RESET}"
    exit 1
fi

# Detecta modo dev
DEV_MODE=false
if [ "$1" == "--dev" ]; then
    DEV_MODE=true
    echo -e "${CINZA}[$(date '+%Y-%m-%d %H:%M:%S')] Modo desenvolvimento ativado${RESET}"
fi

# Função para limpar tela (só em produção)
clear_screen() {
    if [ "$DEV_MODE" = false ]; then
        clear
    fi
}

# Função para exibir box
print_box() {
    local message="$1"
    local width=45
    local line=$(printf '─%.0s' $(seq 1 $((width-2))))
    
    echo -e "\n${CINZA}╭${line}╮${RESET}"
    printf "${CINZA}│${RESET} %-$((width-2))s ${CINZA}│${RESET}\n" "$message"
    echo -e "${CINZA}╰${line}╯${RESET}\n"
}

# Função para executar comando
run_command() {
    local cmd="$1"
    local description="$2"
    
    if [ "$DEV_MODE" = true ]; then
        echo -e "${CINZA}[$(date '+%Y-%m-%d %H:%M:%S')] Running: $cmd${RESET}"
    fi
    
    if eval "$cmd" > /dev/null 2>&1; then
        echo -e "  ${VERDE}✓${RESET} $description"
        return 0
    else
        echo -e "  ${VERMELHO}✗${RESET} $description"
        return 1
    fi
}

# Início
clear_screen
print_box "  LivChat Setup v0.1 - Bootstrap  "

echo -e "${CINZA}Preparando sistema...${RESET}\n"

# Atualiza sistema
run_command "apt update" "Atualizando lista de pacotes"

# Instala dependências básicas
echo -e "\n${CINZA}Instalando dependências...${RESET}\n"

# Python e pip
run_command "apt install -y python3" "Python 3"
run_command "apt install -y python3-pip" "Python pip"
run_command "apt install -y python3-venv" "Python venv"

# Ferramentas essenciais
run_command "apt install -y git" "Git"
run_command "apt install -y curl" "Curl"
run_command "apt install -y wget" "Wget"

# Ferramentas auxiliares
run_command "apt install -y jq" "JQ (parser JSON)"
run_command "apt install -y apache2-utils" "Apache Utils (htpasswd)"
run_command "apt install -y unzip" "Unzip"

# Verifica se já está no diretório correto
if [ -f "setup.py" ]; then
    echo -e "\n${CINZA}Detectado diretório do projeto${RESET}"
else
    # Se for instalação remota, clona o repositório
    echo -e "\n${CINZA}Baixando projeto...${RESET}\n"
    
    if [ -d "LivChatSetup-v0.1" ]; then
        run_command "rm -rf LivChatSetup-v0.1" "Removendo versão anterior"
    fi
    
    run_command "git clone https://github.com/pedrohnas0/LivChatSetup-v0.1.git" "Clonando repositório"
    
    if [ -d "LivChatSetup-v0.1" ]; then
        cd LivChatSetup-v0.1
    else
        echo -e "${VERMELHO}✗ Erro ao clonar repositório${RESET}"
        exit 1
    fi
fi

# Instala dependências Python
echo -e "\n${CINZA}Configurando Python...${RESET}\n"

if [ -f "requirements.txt" ]; then
    run_command "pip3 install -r requirements.txt" "Instalando dependências Python"
else
    # Instala dependências mínimas
    run_command "pip3 install jinja2" "Jinja2 (templates)"
    run_command "pip3 install paramiko" "Paramiko (SSH)"
fi

# Finaliza
print_box "     Instalação concluída!      "

echo -e "${CINZA}Execute o setup com:${RESET}"
echo -e "${BRANCO}  python3 setup.py${RESET}          ${CINZA}# Modo produção${RESET}"
echo -e "${BRANCO}  python3 setup.py --dev${RESET}     ${CINZA}# Modo desenvolvimento${RESET}"
echo ""

# Se não estiver em modo dev, executa o setup automaticamente
if [ "$DEV_MODE" = false ]; then
    echo -e "${CINZA}Iniciando setup automaticamente...${RESET}"
    sleep 2
    python3 setup.py
else
    echo -e "${CINZA}[$(date '+%Y-%m-%d %H:%M:%S')] Bootstrap concluído${RESET}"
fi