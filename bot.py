import discord
from decouple import config
from flask import Flask
import google.generativeai as genai
from discord.ext import commands
from keep_alive import keep_alive

dc_token = config("DC_TOKEN")
gemini_api = config("GOOGLEGEMINIAPI")

genai.configure(api_key=gemini_api)
model = genai.GenerativeModel("gemini-2.0-flash")

#Configurar Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

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
async def miguel(ctx, palavra):
    await ctx.send(f"Sim em minha concordância o Miguel é {palavra}")

bot.run(dc_token)