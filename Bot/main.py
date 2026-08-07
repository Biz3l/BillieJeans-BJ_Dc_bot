import discord
from decouple import config
from discord.ext import commands
import os


from Bot.services.Upscaler.instance import upscale_queue_services
from database.connection import database, metadata, engine
from database.models import users
from Bot.services.DatabaseServices import database_bot_services
from Bot.config.config import Config

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) ##Path base para o arquivo bot.py :)

JSON_CONFIG = Config()
BOT_CONFIG = JSON_CONFIG.read_config()

dc_token = config("DC_TOKEN")

# Carrega o prefix
if BOT_CONFIG.get("prefix"):
    prefix = BOT_CONFIG.get("prefix")
else:
    JSON_CONFIG.write_config("prefix", "!")
    prefix = "!"


#Configurar Bot
database_services = database_bot_services()

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix=f"{prefix}", help_command=None, intents=intents)
    
    async def setup_hook(self):
        print("Rodando setup hook")

        for filename in os.listdir("./Bot/cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"Bot.cogs.{filename[:-3]}")

        await database.connect()
        metadata.create_all(engine)
        synced = await self.tree.sync()
        
        print("Tree Syncada com sucesso")
        print(f"Quantidade de comandos tree disponíveis: {len(synced)}")

        await upscale_queue_services.start()
        print("Queue de upscaling iniciado com suceso!")
        

    async def on_ready(self):
        print(f"Bot {self.user.name} está pronto!")

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.reply(f"Comando não encontrado! por favor use {prefix}help para ver os comandos!")
        else:
            raise error
        

bot = Bot()

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
        return
    
    if moedas <= 0 or moedas >= 10000:
        await ctx.send(f"Quantidade de moedas inválida!!!")
        return
     
    #FIXME: ADICIONAR POSTGRESQL // POR ENQUANTO ESTÁ EM SQLITE
    if BOT_CONFIG.get("bot_admin"):
        if ctx.author.id in BOT_CONFIG.get("bot_admin"):
            await database_services.add_coins_to_user(ctx, moedas)
            return
    
    await ctx.send("Nã nã nã, você não tem esses privilégios 👀")
    return

bot.run(dc_token)