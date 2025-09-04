import discord
from decouple import config
from flask import Flask
from discord.ext import commands
import re
import datetime
from utilities import enhancer
import os
from PIL import Image


dc_token = config("DC_TOKEN")
prefix = "!"

#Configurar Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=f"{prefix}", intents=intents)

@bot.event
async def on_ready():
  print(f"Bot {bot.user.name} está pronto!")


@bot.command()
async def ping(ctx):
    #PONG
    await ctx.send("Pong :)")

@bot.command()                                                                                                  
async def mario(ctx):
    #Credo mano
    await ctx.send("https://pm1.aminoapps.com/6868/9bd680702e657d438cafd346a0304ded76b4ea3ar1-720-661v2_hq.jpg")

@bot.command()
async def eleé(ctx, pessoa, palavra):
    if pessoa.lower() == "gabriel" or pessoa.lower() == "biel" or pessoa.lower() == "biz3l":
        await ctx.send(f"{pessoa} é muito macho, não é viado não viu")
    else:
        await ctx.send(f"Sim em minha concordância o(a) {pessoa} é {palavra}")
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
    attachment = ctx.message.attachments[0]
    if not attachment.content_type.startswith("image/"):
        await ctx.send("O conteúdo necessita ser uma imagem! ")
        return
    try:
        await ctx.send("Processando imagem, por favor aguarde.")
        file_path = f"utilities/{attachment.filename}"
        await attachment.save(file_path)
        enhancer.converterimg(f"utilities/{attachment.filename}")
        os.remove(f"utilities/{attachment.filename}")
        enhancer.upscale(f'utilities/convert.jpg')
        await ctx.send("Aqui está sua imagem:", file=discord.File("utilities/output.png"))
        os.remove(f"utilities/convert.jpg")
        os.remove(f"utilities/output.png")
    except:
        await ctx.send('fiquei doidão e não consegui enviar a imagem')

bot.run(dc_token)