#!/bin/bash

################################################################################
#                         LIVCHAT SETUP v0.1 - Bootstrap                      #
################################################################################

# Paleta de cores profissional (igual ao original)
laranja="\e[38;5;173m"      # Cor laranja suave para texto
verde="\e[32m"              # Verde para sucesso
branco="\e[97m"             # Branco brilhante para destaques
bege="\e[93m"               # Bege para informações
vermelho="\e[91m"           # Vermelho para erros
cinza="\e[90m"              # Cinza para bordas
azul="\e[34m"               # Azul
reset="\e[0m"               # Reset das cores
bold="\e[1m"                # Negrito

# ============= FUNÇÕES DE BOX DO PROJETO ORIGINAL =============

box_line_centered() {
    local content="$1"
    local total_width=101  # Largura interna total da caixa (103 - 2 bordas)
    
    # Remove códigos de cor para calcular tamanho real do texto
    local clean_content=$(printf "%b" "$content" | sed 's/\x1b\[[0-9;]*m//g')
    local content_length=${#clean_content}
    
    # Calcula espaçamento para centralizar perfeitamente
    local total_padding=$((total_width - content_length))
    local left_padding=$((total_padding / 2))
    local right_padding=$((total_padding - left_padding))
    
    # Monta a linha com espaçamento calculado e processa as cores
    printf "${cinza}│${reset}"
    printf "%*s" $left_padding ""
    printf "%b" "$content"
    printf "%*s" $right_padding ""
    printf "${cinza}│${reset}\n"
}

box_line() {
    local content="$1"
    local clean_content=$(printf "%b" "$content" | sed 's/\x1b\[[0-9;]*m//g')
    local content_length=${#clean_content}
    local right_padding=$((99 - content_length))  # 99 = 101 - 2 espaços (início e fim)
    
    printf "${cinza}│${reset} "
    printf "%b" "$content"
    printf "%*s" $right_padding ""
    printf " ${cinza}│${reset}\n"
}

box_top() {
    echo -e "${cinza}╭─────────────────────────────────────────────────────────────────────────────────────────────────────╮${reset}"
}

box_empty() {
    echo -e "${cinza}│                                                                                                     │${reset}"
}

box_bottom() {
    echo -e "${cinza}╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯${reset}"
}

# ============= FUNÇÕES ESPECÍFICAS =============

print_logo() {
    clear
    echo ""
    box_top
    box_empty
    box_empty
    # IMPORTANTE: Os logos têm espaços extras para ajudar no alinhamento!
    box_line_centered "${laranja}     ██╗     ██╗██╗   ██╗ ██████╗██╗  ██╗ █████╗ ████████╗     ${reset}"
    box_line_centered "${laranja}     ██║     ██║██║   ██║██╔════╝██║  ██║██╔══██╗╚══██╔══╝     ${reset}"
    box_line_centered "${laranja}     ██║     ██║██║   ██║██║     ███████║███████║   ██║        ${reset}"
    box_line_centered "${laranja}     ██║     ██║╚██╗ ██╔╝██║     ██╔══██║██╔══██║   ██║        ${reset}"
    box_line_centered "${laranja}     ███████╗██║ ╚████╔╝ ╚██████╗██║  ██║██║  ██║   ██║        ${reset}"
    box_line_centered "${laranja}     ╚══════╝╚═╝  ╚═══╝   ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝        ${reset}"
    box_empty
    box_line_centered "${branco}${bold}Setup v0.1 - Bootstrap${reset}"
    box_empty
    box_bottom
    echo ""
}

print_status_box() {
    echo ""
    box_top
    box_line " ${branco}${bold}INICIANDO INSTALAÇÃO${reset}"
    box_bottom
    echo ""
}

print_success_box() {
    echo ""
    box_top
    box_empty
    box_line_centered "${verde}${bold}✓ INSTALAÇÃO CONCLUÍDA!${reset}"
    box_empty
    box_bottom
    echo ""
}

# Contador de progresso
PROGRESS_CURRENT=0
PROGRESS_TOTAL=15

# Função para executar comando com progresso
run_command() {
    local cmd="$1"
    local description="$2"
    
    PROGRESS_CURRENT=$((PROGRESS_CURRENT + 1))
    
    if [ "$DEV_MODE" = true ]; then
        echo -e "${cinza}$(date '+%Y-%m-%d %H:%M:%S') ${bege}[command]${cinza} > ${reset}$cmd"
    fi
    
    if eval "$cmd" > /dev/null 2>&1; then
        echo -e "  ${verde}✓${reset} ${cinza}$PROGRESS_CURRENT/$PROGRESS_TOTAL${reset} - $description"
        return 0
    else
        echo -e "  ${vermelho}✗${reset} ${cinza}$PROGRESS_CURRENT/$PROGRESS_TOTAL${reset} - $description"
        return 1
    fi
}

# Verifica se é root
if [ "$(id -u)" -ne 0 ]; then
    echo -e "${vermelho}✗ Este script precisa ser executado como root${reset}"
    echo -e "${cinza}Use: sudo bash install.sh${reset}"
    exit 1
fi

# Detecta modo dev
DEV_MODE=false
if [ "$1" == "--dev" ]; then
    DEV_MODE=true
    echo -e "${cinza}$(date '+%Y-%m-%d %H:%M:%S') ${azul}[info]${cinza} > ${reset}Modo desenvolvimento ativado"
fi

# ============= INÍCIO DA INSTALAÇÃO =============

print_logo
print_status_box

echo -e "${bege}Preparando sistema para instalação...${reset}\n"

# Atualiza sistema
run_command "apt update" "Atualizando lista de pacotes"

# Instala dependências básicas
echo -e "\n${cinza}Instalando dependências...${reset}\n"

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
    echo -e "\n${cinza}Detectado diretório do projeto${reset}"
else
    # Se for instalação remota, clona o repositório
    echo -e "\n${cinza}Baixando projeto...${reset}\n"
    
    if [ -d "LivChatSetup-v0.1" ]; then
        run_command "rm -rf LivChatSetup-v0.1" "Removendo versão anterior"
    fi
    
    run_command "git clone https://github.com/pedrohnas0/LivChatSetup-v0.1.git" "Clonando repositório"
    
    if [ -d "LivChatSetup-v0.1" ]; then
        cd LivChatSetup-v0.1
    else
        echo -e "${vermelho}✗ Erro ao clonar repositório${reset}"
        exit 1
    fi
fi

# Instala dependências Python
echo -e "\n${cinza}Configurando Python...${reset}\n"

if [ -f "requirements.txt" ]; then
    run_command "pip3 install -r requirements.txt" "Instalando dependências Python"
else
    # Instala dependências mínimas
    run_command "pip3 install jinja2" "Jinja2 (templates)"
    run_command "pip3 install paramiko" "Paramiko (SSH)"
fi

# Finalização
print_success_box

echo -e "${bege}Execute o setup com:${reset}"
echo -e "\n  ${branco}${bold}python3 setup.py${reset}          ${cinza}# Modo produção com interface elegante${reset}"
echo -e "  ${branco}${bold}python3 setup.py --dev${reset}     ${cinza}# Modo desenvolvimento com logs completos${reset}"
echo ""

# Se não estiver em modo dev, executa o setup automaticamente
if [ "$DEV_MODE" = false ]; then
    echo -e "${cinza}Iniciando setup automaticamente...${reset}"
    sleep 2
    python3 setup.py
else
    echo -e "${cinza}$(date '+%Y-%m-%d %H:%M:%S') ${verde}[success]${cinza} > ${reset}Bootstrap concluído"
fi