# 🚀 LivChat Setup v0.1

**Sistema modular para deploy automatizado de aplicações Docker**

*Baseado no projeto [SetupOrion](https://github.com/oriondesign2015/SetupOrion) do Willian - Orion Design*

---

## ⚡ **Instalação**

```bash
# Execução rápida
bash <(curl -sSL setup.livchat.ai)

# Instalação manual
git clone https://github.com/pedrohnas0/LivChatSetup-v0.1.git
cd LivChatSetup-v0.1
sudo python3 setup.py
```

## 🆕 **Novidades v0.1**

- **Multi-instância**: Instale várias versões da mesma app (n8n_dev, n8n_prod)
- **Modo Remoto**: Gerencie múltiplas VPS do seu PC
- **Logs Melhorados**: 3 níveis (produção, verbose, debug)

## 📦 **Aplicações Disponíveis**

### Infraestrutura
- Docker + Swarm
- Traefik (SSL automático)
- Portainer

### Bancos de Dados  
- PostgreSQL
- Redis
- MinIO

### Aplicações
- N8N - Automação
- Chatwoot - Suporte
- Directus - CMS
- Evolution API - WhatsApp
- E mais...

## 💻 **Uso Básico**

### Menu Interativo
```bash
./setup.py
# Use ↑↓ para navegar
# → para selecionar
# Enter para instalar
```

### Multi-instância
```bash
./setup.py install n8n --instance dev
./setup.py install n8n --instance prod
```

### Modo Remoto
```bash
./setup.py add-server
./setup.py use servidor1
./setup.py install traefik
```

## 🔧 **Requisitos**

- Debian 12 ou Ubuntu 20+
- Acesso root
- 2GB RAM mínimo
- Python 3.9+

---

### 💝 Agradecimentos

**Willian - [Orion Design](https://oriondesign.art.br/)**

Projeto original: [SetupOrion](https://github.com/oriondesign2015/SetupOrion)