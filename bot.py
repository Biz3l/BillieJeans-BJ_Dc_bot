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
intents.messages = True
bot = commands.bot(command_prefix=":", intents=intents)

@bot.event
async def on_ready():
  print(f"Bot {bot.user.name} está pronto!")

@bot.command()
async def ask(ctx, *, question):
    await ctx.trigger_typing()
    try:
        response = model.generate_content(question)
        await ctx.send(response.text)
    except Exception as e:
        await ctx.send("Erro ao gerar resposta com Gemini.")
        print(e)
keep_alive()
bot.run(dc_token)