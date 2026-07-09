# BillieJeans-BJ_Dc_bot

Bot para Discord desenvolvido em Python com `discord.py`, criado para aprendizado, automações e utilitários diversos.

## 💡 Funcionalidades

### Comandos Principais
- 🎨 **Upscaling de Imagens** - Melhora a qualidade de imagens usando RealESRGAN
- 🎵 **Download de Áudio** - Converte vídeos do YouTube para MP3
- 📊 **Comandos de Informação** - Versão, hora/data, perfil e ajuda
- 🪙 **Sistema de Moedas** - Consulta e criação automática de perfil no banco
- 🎮 **Comandos Divertidos** - Interações e jogos
- 🛠️ **Utilidades Gerais** - Comandos auxiliares e suporte

### Estrutura do Projeto
- `Bot/cogs/` - Comandos organizados por categoria
- `Bot/services/` - Regras de negócio e acesso ao banco
- `Bot/error/` - Sistema de tratamento de erros
- `Bot/utilities/` - Ferramentas (enhancer, ytdownloader)
- `api/` - API auxiliar
- `database/` - Gerenciamento de dados
- `Docs/` - Documentação

## 🚀 Tecnologias usadas

- **Python 3.10** == **Bot**
- **Python 3.19** == **Backend**
- **discord.py 2.6.4** - API Discord
- **RealESRGAN** - Upscaling de imagens
- **yt-dlp** - Download de vídeos YouTube
- **GFPGAN** - Restauração de rosto em imagens

## 📦 Como usar

1. Clone o repositório  
   ```bash
   git clone https://github.com/Biz3l/BillieJeans-BJ_Dc_bot.git
   cd BillieJeans-BJ_Dc_bot
   ```

2. Crie um ambiente virtual  
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate  # Windows
   ```

3. Instale dependências  
   ```bash
   pip install -r Bot/requirements.txt
   ```

4. Configure suas credenciais  
   - Adicione seu token do Discord em uma variável de ambiente `DC_TOKEN`

5. Execute o bot  
   ```bash
   python -m Bot.main
   ```

## 🗄️ Banco de Dados

- O bot usa SQLite para persistir usuários e moedas
- A tabela de usuários é criada automaticamente no startup
- O perfil é criado automaticamente quando o usuário usa comandos que dependem de dados persistentes

## 🧠 Sobre o Projeto

Esse projeto foi criado com o objetivo de praticar:
- Integração com APIs (Discord, YouTube, etc)
- Programação assíncrona em Python
- Arquitetura de bots Discord
- Processamento de imagens
- Automações em servidores Discord

O bot continua em desenvolvimento e recebe melhorias e novos comandos regularmente.

---
