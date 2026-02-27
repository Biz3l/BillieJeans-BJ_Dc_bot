import discord
from discord import app_commands
from decouple import config
from flask import Flask
from discord.ext import commands
import re
import datetime
from utilities.enhancer import enhancer
import os
import asyncio
from utilities.botCommands import botcommands
from utilities.ytdownloader import ytdownloader
from api import keepAlive
import sqlite3
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) ##Path base para o arquivo bot.py :)
db = "dc_bot.db"

user_db = sqlite3.connect(db)
cursor = user_db.cursor()
cursor.execute("""
               CREATE TABLE IF NOT EXISTS
               users(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_id INTEGER UNIQUE,
               user TEXT,
               coins INTEGER
               CHECK (coins >= 0)
               )
        """)
user_db.commit()
user_db.close()

dc_token = config("DC_TOKEN")
prefix = "!"
bot_help = botcommands.comandos()

keepAlive() #Manter o bot de pé

#Configurar Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=f"{prefix}", help_command=None, intents=intents)

@bot.event
async def on_ready():
  print(f"Bot {bot.user.name} está pronto!")
  try:
    synced = await bot.tree.sync()
    print(f'Bot syncado com sucesso: {len(synced)}')
  except Exception as e:
      print(f'Erro ao sincronizar: {e}')
      

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply(f"Comando não encontrado! por favor use {prefix}help para ver os comandos!")
    else:
        raise error

@bot.command(name='help')
async def custom_help(ctx):
    embed_help = discord.Embed(
        title="Ajuda do Bot 🤖",
        description=bot_help,
        color=discord.Color.red()
    )
    await ctx.send(embed=embed_help)

@bot.tree.command(name='help', description='Puxa os dados de help do bot')
async def help(interaction: discord.Interaction):
    embed_help = discord.Embed(
        title="Ajuda do Bot 🤖",
        description=bot_help,
        color=discord.Color.red()
    )
    await interaction.response.send_message(embed=embed_help)
    

@bot.command()
async def ping(ctx):
    #PONG
    await ctx.send("Pong :) 🏓")

# Ping porém em slash / :)
@bot.tree.command(name='ping', description='pong!')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! 🏓, {interaction.user.mention}!")
    

@bot.command()                                                                                                  
async def mario(ctx):
    #Credo mano
    await ctx.send("WAAAAAAAAAAAAAH", file=discord.File(os.path.join(BASE_DIR, 'images/MARIO.jpg')))

@bot.tree.command(name="mario", description="É o MARIO 😣")
async def mario_tree(interaction: discord.Interaction):
    await interaction.response.send_message(file=discord.File(os.path.join(BASE_DIR, 'images/MARIO.jpg')))

@bot.command()
async def eleé(ctx, pessoa, *, frase: str):
    if pessoa.lower() == "gabriel" or pessoa.lower() == "biel" or pessoa.lower() == "biz3l":
        await ctx.send(f"{pessoa} é muito macho, não é {frase} não viu")
    else:
        await ctx.send(f"Sim em minha concordância o(a) {pessoa} é {frase}")
        await ctx.send(f"Lembrando, ele gosta de tu hein cuidado")


@bot.command()
# Retorna a foto de perfil do id/usuario colocado no argumento, se não houver nenhum envia a do próprio autor
async def fotodata(ctx, usr: discord.User = None):
    if usr == None:
        fotousr = ctx.author.display_avatar
        await ctx.reply(f"{fotousr}")
        return
    
    try:
        fotousr = usr.display_avatar
        await ctx.send(f"{fotousr}")

    except Exception as e:
        print(f"ERRO: {e}")
    

@bot.command()
# Retorna os dados do usuário no discord
async def usrdata(ctx, usr: discord.User = None):
        if usr is None:
            await ctx.reply("Não estou vendo id algum, por favor me mande para que eu possa te retornar!")
            return
        
        try:
            usr_display = re.sub(r"([^a-zA-Z0-9\s])", r"\\\1", usr.display_name)
            usr_name = re.sub(r"([^a-zA-Z0-9\s])", r"\\\1", usr.name)
            await ctx.send(f"Display name: {usr_display}")
            await ctx.send(f"{usr.display_avatar}")
            await ctx.send(f"Conta criada em: {usr.created_at.strftime('%d/%m/%Y %H:%M:%S')}")
            await ctx.send(f"Usuário: @{usr_name}")
        except Exception as e:
            print(f"ERRO: {e}")

@bot.command()
# Comando pra ver o dia e a hora
async def diaehora(ctx):
    hoje = datetime.datetime.now()
    await ctx.send(f"{hoje.strftime('%A -- %H:%M:%S')}")

### NUMERO DE PROCESSOS DO ENHANCER
Processos = 1
@bot.command()
# Comando de Upscaling
async def upscale(ctx, Processos=Processos):

    if not ctx.message.attachments:
        await ctx.reply('Não encontrei nenhum conteúdo anexado!')
    attachment = ctx.message.attachments[0]
    # Verifica se é Imagem
    if not attachment.content_type or not attachment.content_type.startswith("image/"):
        if not attachment.filename.endswith((".png", ".jpg", ".jpeg", ".webp")):
            await ctx.reply("O conteúdo necessita ser uma imagem! 🖨️")
            return
        
    imagemconvertida = None
    imagememupscale = None
    
    try:
        await ctx.reply("Processando imagem, por favor aguarde. ⏳")

        file_path = os.path.join(BASE_DIR, f"utilities/enhancer/{attachment.filename}")

        await attachment.save(file_path)
        
        loop = asyncio.get_event_loop()

        # Pega o nome da imagem convertida e a converte (Já que no caso cada imagem tem nomes diferentes)
        print("Convertendo imagem")

        imagemconvertida = await loop.run_in_executor(None, enhancer.converterimg, os.path.join(BASE_DIR, f"{file_path}"))

        print("Imagem convertida!")


        os.remove(os.path.join(BASE_DIR, f"{file_path}"))


        # Pega o path inteiro do output da imagem em upscale e já upscala a imagem
        imagememupscale = await loop.run_in_executor(None, enhancer.upscale, os.path.join(BASE_DIR, f'utilities/enhancer/{imagemconvertida}'))
        
        print(f"Processo: {Processos} feito com sucesso!")

        await ctx.reply(f"{ctx.author.mention} Aqui está sua imagem:", file=discord.File(os.path.join(BASE_DIR, f"{imagememupscale}")))

        os.remove(os.path.join(BASE_DIR, f"utilities/enhancer/{imagemconvertida}"))

        os.remove(os.path.join(BASE_DIR, f"{imagememupscale}"))

        Processos += 1

    except Exception as e:
        await ctx.reply('Fiquei doidão e não consegui enviar a imagem 😵')
        print(f'[ERRO UPSCALE]: {e}')
        if imagemconvertida:
            os.remove(os.path.join(BASE_DIR, f"utilities/enhancer/{imagemconvertida}"))
        if imagememupscale:
            os.remove(os.path.join(BASE_DIR, f"{imagememupscale}"))
        print(f'Imagens apagadas com sucesso')

@bot.command()
# Um easter egg do bot (Não vou incluir em help nem em readme, vai ficar escondido, só eu sei que existe)
async def vazio_roxo(ctx):
    async with ctx.typing():
        await ctx.send('Vazio Roxo é a combinação da expansão infinita e da absorção infinita \n — a união dessas duas técnicas cria um espaço onde tudo é apagado. \n É o poder de manipular o espaço até que ele deixe de existir, \n tornando tudo que toca simplesmente inexistente.')
        await ctx.send('🫸🔵🔴🫷')
        await ctx.send('**無量空処**')
        await ctx.send('🤌🟣')
        await ctx.send('https://i.pinimg.com/originals/e8/4e/db/e84edb279472c7ab49e97ec276d4ffda.gif')

@bot.command()
# Comando para download de links mp3 do yt!
async def ytdl(ctx, url = None):
    if url == None:
        await ctx.reply('Não encontrei nenhuma URL especificada! Para entender o comando envie "!help" !')
        return
    
    caminhodownload = None

    await ctx.send(f'PROCESSANDO :) \n**ATENÇÃO**, o arquivo enviado resulte em mais que 8mb, variando do server, há a possibilidade, do arquivo não ser enviado!')
    
    try:
        loop = asyncio.get_event_loop()
        caminhodownload = await loop.run_in_executor(None, ytdownloader.ytdownloader, f"{url}")

        if caminhodownload == None:
            await ctx.send('ERRO: Arquivo não encontrado, possivelmente falha no download')
        
        if os.path.getsize(caminhodownload) > 8 * 1024 * 1024:
            await ctx.send('ERRO: Arquivo grande demais para envio no discord!')
            os.remove(caminhodownload)
            return
        
        await ctx.send(f"{ctx.author.mention} Aqui está seu arquivo baixado:", file=discord.File(os.path.join(BASE_DIR, f"{caminhodownload}")))
        os.remove(caminhodownload)

    except Exception as e:
        await ctx.send(f'Erro ao processar vídeo')
        print(f"Erro Processamento de vídeo: {e}")
        if caminhodownload and os.path.exists(caminhodownload):
            os.remove(caminhodownload)
            return
        return

@bot.tree.command(name="ytdl", description="Faz um download em mp3 do youtube pra você :)")
@app_commands.describe(url="URL do vídeo que queira baixar!!")
async def ytdl_tree(interaction: discord.Interaction, url: str):
    if url == None:
        await interaction.response.send_message("Não encontrei nenhuma url especificada!")
        return
    await interaction.response.defer(thinking=True)

    caminhodownload = None
    try:
        loop = asyncio.get_event_loop()
        caminhodownload = await loop.run_in_executor(None, ytdownloader.ytdownloader, f"{url}")

        if caminhodownload == None:
            await interaction.followup.send('ERRO: Arquivo não encontrado, possivelmente falha no download')
        
        if os.path.getsize(caminhodownload) > 8 * 1024 * 1024:
            await interaction.followup.send('ERRO: Arquivo grande demais para envio no discord!')
            os.remove(caminhodownload)
            return
        
        await interaction.followup.send(f"Aqui está seu arquivo baixado:", file=discord.File(os.path.join(BASE_DIR, f"{caminhodownload}")))
        os.remove(caminhodownload)

    except Exception as e:
        await interaction.followup.send(f'Erro ao processar vídeo')
        print(f"Erro Processamento de vídeo: {e}")
        if caminhodownload and os.path.exists(caminhodownload):
            os.remove(caminhodownload)
            return
        return


bot_version = 0.5 #Versão do bot

@bot.command()
async def version(ctx):
    criador = await bot.fetch_user('239568901204213760')
    await ctx.send(f'Atualmente estou na versão **{bot_version}**, e meu criador {criador.name} tem muito amor a mim!')

@bot.tree.command(name='version', description='Mostra a versão do bot')
async def version_tree(interaction: discord.Interaction):
    criador = await bot.fetch_user('239568901204213760')
    await interaction.response.send_message(f'Atualmente estou na versão **{bot_version}**, e meu criador {criador.name} tem muito amor a mim! <a:BongoCatMany:1476209882582745111>')


@bot.command()
async def coins(ctx):
    con = sqlite3.connect(db)
    cur = con.cursor()

    # Cria o usuário se não existir
    cur.execute(
        "INSERT OR IGNORE INTO users (user_id, user, coins) VALUES (?, ?, ?)",
        (ctx.author.id, ctx.author.name, 0,)
    )
    con.commit()

    # Pega as moedas
    cur.execute("SELECT coins FROM users WHERE user_id = ?", (ctx.author.id,))
    coins = cur.fetchone()[0]

    if coins == 1:
        await ctx.send(f"Você tem **{coins}** 🪙 moeda! <a:BongoCat:1476210219045490709>")
    else:
        await ctx.send(f"Você tem **{coins}** 🪙 moedas! <a:BongoCat:1476210219045490709>")

    con.close()


@bot.command()
async def add_coins(ctx, moedas: int):
    if not moedas or moedas <= 0 or moedas >= 10000:
        await ctx.send(f"Quantidade de moedas inválida!!!")
        return
    
    r = requests.post("http://localhost:8080/pay", json={
        "SECRET": f"{config('SECRET_KEY')}",
        "user": ctx.author.name,
        "user_id": ctx.author.id,
        "coins": moedas,
    })

    print(r.json()["SUCESSO"])

    if r.status_code == 200:
        await ctx.send(f"{moedas} moedas adicionadas com sucesso!")
    else:
        await ctx.send("Erro interno!")

bot.run(dc_token)