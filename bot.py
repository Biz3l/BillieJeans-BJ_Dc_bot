import discord
from decouple import config
from flask import Flask
from discord.ext import commands
import re
import datetime
from utilities.enhancer import enhancer
import os
from PIL import Image
import asyncio
from utilities.botCommands import botcommands
from time import sleep
dc_token = config("DC_TOKEN")
prefix = "!"
bot_help = botcommands.comandos()


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
        await ctx.send(f"Comando não encontrado! por favor use {prefix}help para ver os comandos!")
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

@bot.command()
async def ping(ctx):
    #PONG
    await ctx.send("Pong :) 🏓")


@bot.tree.command(name='ping', description='pong!')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! 🏓, {interaction.user.mention}!")
    

@bot.command()                                                                                                  
async def mario(ctx):
    #Credo mano
    await ctx.send("https://pm1.aminoapps.com/6868/9bd680702e657d438cafd346a0304ded76b4ea3ar1-720-661v2_hq.jpg")

@bot.command()
async def eleé(ctx, pessoa, *, frase: str):
    if pessoa.lower() == "gabriel" or pessoa.lower() == "biel" or pessoa.lower() == "biz3l":
        await ctx.send(f"{pessoa} é muito macho, não é {frase} não viu")
    else:
        await ctx.send(f"Sim em minha concordância o(a) {pessoa} é {frase}")
        await ctx.send(f"Lembrando, ele gosta de tu hein cuidado")


@bot.command()
# Retorna a foto de perfil de quem enviou a mensagem
async def minhafoto(ctx):
    fotousr = ctx.author.display_avatar
    await ctx.send(f"{fotousr}")

@bot.command()
# Retorna os dados do usuário no discord
async def usrdata(ctx, idusr: int):
        usr = await bot.fetch_user(idusr)
        usr_display = re.sub(r"([^a-zA-Z0-9\s])", r"\\\1", usr.display_name)
        usr_name = re.sub(r"([^a-zA-Z0-9\s])", r"\\\1", usr.name)
        await ctx.send(f"Display name: {usr_display}")
        await ctx.send(f"{usr.display_avatar}")
        await ctx.send(f"Conta criada em: {usr.created_at.strftime('%d/%m/%Y %H:%M:%S')}")
        await ctx.send(f"Usuário: @{usr_name}")

@bot.command()
# Comando pra ver o dia e a hora
async def diaehora(ctx):
    hoje = datetime.datetime.now()
    await ctx.send(f"{hoje.strftime('%A -- %H:%M:%S')}")

@bot.command()
# Comando de Upscaling
async def upscale(ctx):
    if not ctx.message.attachments:
        await ctx.send('Não encontrei nenhum conteúdo anexado!')
    attachment = ctx.message.attachments[0]
    # Verifica se é Imagem
    if not attachment.content_type or not attachment.content_type.startswith("image/"):
        if not attachment.filename.endswith((".png", ".jpg", ".jpeg", ".webp")):
            await ctx.send("O conteúdo necessita ser uma imagem! 🖨️")
            return
    try:
        await ctx.send("Processando imagem, por favor aguarde. ⏳")

        file_path = f"utilities/enhancer/{attachment.filename}"

        await attachment.save(file_path)
        
        loop = asyncio.get_event_loop()

        # pega o nome da imagem convertida (Já que no caso cada imagem tem nomes diferentes)
        imagemconvertida = await loop.run_in_executor(None, enhancer.converterimg, f"{file_path}")

        os.remove(f"{file_path}")

        imagememupscale = await loop.run_in_executor(None, enhancer.upscale, f'utilities/enhancer/{imagemconvertida}')
        
        await ctx.send("Aqui está sua imagem:", file=discord.File(f"{imagememupscale}"))

        os.remove(f"utilities/enhancer/{imagemconvertida}")

        os.remove(f"{imagememupscale}")

    except Exception as e:
        await ctx.send('Fiquei doidão e não consegui enviar a imagem 😵')
        print(f'[ERRO UPSCALE]: {e}')

@bot.command()
# Um easter egg do bot (Não vou incluir em help nem em readme, vai ficar escondido, só eu sei que existe)
async def vazio_roxo(ctx):
    async with ctx.typing():
        await ctx.send('Vazio Roxo é a combinação da expansão infinita e da absorção infinita \n — a união dessas duas técnicas cria um espaço onde tudo é apagado. \n É o poder de manipular o espaço até que ele deixe de existir, \n tornando tudo que toca simplesmente inexistente.')
        await ctx.send('🫸🔵🔴🫷')
        await ctx.send('**無量空処**')
        await ctx.send('🤌🟣')
        await ctx.send('https://i.pinimg.com/originals/e8/4e/db/e84edb279472c7ab49e97ec276d4ffda.gif')

bot.run(dc_token)