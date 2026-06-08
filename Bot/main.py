import discord
from discord import app_commands
from decouple import config
from discord.ext import commands
import os
from Bot.cogs.fun import Fun
from Bot.cogs.utilities import Utilities
from Bot.cogs.info import Info
from database.connection import database, metadata, engine
from database.models import users
from Bot.services.database_services import database_bot_services

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) ##Path base para o arquivo bot.py :)


dc_token = config("DC_TOKEN")
prefix = "!"

#Configurar Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=f"{prefix}", help_command=None, intents=intents)
database_services = database_bot_services()

@bot.event
async def on_ready():
  #HACK: DEPOIS MUDAR PARA UM SETUP HOOK. #INICIO
  await database.connect()
  metadata.create_all(engine)
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
    


@bot.command()
async def coins(ctx):
    try:
        query = users.select().where(users.c.discord_id == ctx.author.id)
        result = await database.fetch_one(query)
        if not result:
            await database_services.create_user_if_not_exist(ctx)
            print("Usuário criado com Sucesso")
        user = await database.fetch_one(query)
        await ctx.send(f"Usuário {user['username']} tem **{user['coins']}** 🪙 Moedas!")
        
    except Exception as e:
        await ctx.send("Erro interno!")
        print(e)


@bot.command()
async def add_coins(ctx, moedas: int = None): #HACK: PLACEHOLDER PARA ADIÇÃO DE MOEDAS.
    if not moedas:
        await ctx.send(f"Por favor envie a quantidade de moedas!!!")
    if moedas <= 0 or moedas >= 10000:
        await ctx.send(f"Quantidade de moedas inválida!!!")
        return
     
    #FIXME: ADICIONAR POSTGRESQL // POR ENQUANTO ESTÁ EM SQLITE
    try:
        query = users.select().where(users.c.discord_id == ctx.author.id)
        result = await database.fetch_one(query)
        if not result:
            await database_services.create_user_if_not_exist(ctx)
            print("Usuário criado com Sucesso")
        query_coins = users.update().where(users.c.discord_id == ctx.author.id).values(
            coins = users.c.coins + moedas
        )

        await database.execute(query_coins)

        await ctx.send(f"**{moedas}** 🪙 moedas adicionadas com sucesso!")

    except Exception as e:
        await ctx.send("Erro interno!")
        print(e)

bot.run(dc_token)