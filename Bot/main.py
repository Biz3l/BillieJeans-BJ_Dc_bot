import discord
from discord import app_commands
from decouple import config
from flask import Flask
from discord.ext import commands
import re
import datetime
import os
import asyncio
from Bot.utilities.botCommands import botcommands
from api.api import keepAlive
import sqlite3
import requests
from Bot.cogs.fun import Fun
from Bot.cogs.utilities import Utilities

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) ##Path base para o arquivo bot.py :)
db = "dc_bot.db" #HACK: Necessáro arrumar esse placeholder de database.

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

keepAlive() #Manter o bot de pé #HACK: PLACEHOLDER PARA O BACKEND.

#Configurar Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=f"{prefix}", help_command=None, intents=intents)



@bot.event
async def on_ready():
  
  #HACK: DEPOIS MUDAR PARA UM SETUP HOOK. #INICIO
  await bot.add_cog(Fun(bot)) 
  await bot.add_cog(Utilities(bot)) 
  #FIM

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


bot_version = 0.5 #Versão do bot #HACK: ADICIONAR EM INFO DO BOT.

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
async def add_coins(ctx, moedas: int): #HACK: PLACEHOLDER PARA ADIÇÃO DE MOEDAS.
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
        await ctx.send(f"**{moedas}** 🪙 moedas adicionadas com sucesso!")
    else:
        await ctx.send("Erro interno!")

bot.run(dc_token)

#TODO: Necessário refator o código para adição das cogs.