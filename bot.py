import discord
from decouple import config
from flask import Flask
import google.generativeai as genai
from discord.ext import commands

dc_token = config("DC_TOKEN")
gemini_api = config("GOOGLEGEMINIAPI")

genai.configure(api_key=gemini_api)
model = genai.GenerativeModel("gemini-2.0-flash")
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
    await ctx.send(f"Sim em minha concordância o(a) {pessoa} é {palavra}")
    await ctx.send(f"Lembrando, ele gosta de tu hein cuidado")

@bot.command()
async def h(ctx):
    await ctx.send(f"""
Aqui estão alguns dos meus comandos!
{prefix}ask
Perguntas e respostas diretamente com inteligência artificial, caso dê algum erro,
 provavelmente é pelo tamanho da sua pergunta/resposta!
_______________________________________________________________________
{prefix}ping
Pong!
_______________________________________________________________________
{prefix}mario
Um negócio meio nojento
_______________________________________________________________________
{prefix}eleé
Envie um nome e uma palabvra que uma pessoa pode ser = Matheus Corno
""")

bot.run(dc_token)