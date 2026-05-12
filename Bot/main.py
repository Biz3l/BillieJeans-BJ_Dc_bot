import discord
from discord import app_commands
from decouple import config
from discord.ext import commands
import os
import asyncio
import sqlite3
import requests
from cogs.fun import Fun
from cogs.utilities import Utilities
from cogs.info import Info

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) ##Path base para o arquivo bot.py :)


dc_token = config("DC_TOKEN")
prefix = "!"

#Configurar Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=f"{prefix}", help_command=None, intents=intents)



@bot.event
async def on_ready():
  
  #HACK: DEPOIS MUDAR PARA UM SETUP HOOK. #INICIO
  await bot.add_cog(Fun(bot)) 
  await bot.add_cog(Utilities(bot))
  await bot.add_cog(Info(bot))
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
    

# FIXME: Adicionar fix para comando de check de moedas
# @bot.command()
# async def coins(ctx):


@bot.command()
async def add_coins(ctx, moedas: int): #HACK: PLACEHOLDER PARA ADIÇÃO DE MOEDAS.
    if not moedas or moedas <= 0 or moedas >= 10000:
        await ctx.send(f"Quantidade de moedas inválida!!!")
        return
    
    r = requests.post("http://localhost:8080/pay", json={
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

#TODO: Necessário refatorar o código para adição das cogs.