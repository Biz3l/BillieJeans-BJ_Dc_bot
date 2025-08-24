import discord
from decouple import config
from flask import Flask
import google.generativeai as genai
from discord.ext import commands
import re
import datetime

dc_token = config("DC_TOKEN")
gemini_api = config("GOOGLEGEMINIAPI")

genai.configure(api_key=gemini_api)
model = genai.GenerativeModel("gemini-2.5-pro")
prefix = "!"

#Configurar Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=f"{prefix}", intents=intents)

@bot.event
async def on_ready():
  print(f"Bot {bot.user.name} está pronto!")

@bot.command()
async def ask(ctx, *, question):
  try:
        async with ctx.typing():
            response = model.generate_content(question)
            await ctx.send(response.text)
  except Exception as e:
      await ctx.send("Erro ao gerar resposta com Gemini.")
      print(e)

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
async def minhafoto(ctx):
    fotousr = ctx.author.display_avatar
    await ctx.send(f"{fotousr}")

@bot.command()
async def usrdata(ctx, idusr: int):
        usr = await bot.fetch_user(idusr)
        usr_display = re.sub(r"([^a-zA-Z0-9\s])", r"\\\1", usr.display_name)
        usr_name = re.sub(r"([^a-zA-Z0-9\s])", r"\\\1", usr.name)
        await ctx.send(f"Display name: {usr_display}")
        await ctx.send(f"{usr.display_avatar}")
        await ctx.send(f"Conta criada em: {usr.created_at.strftime("%d/%m/%Y %H:%M:%S")}")
        await ctx.send(f"Usuário: @{usr_name}")

@bot.command()
async def diaehora(ctx):
    hoje = datetime.datetime.now()
    await ctx.send(f"{hoje.strftime("%A -- %H:%M:%S")}")

bot.run(dc_token)