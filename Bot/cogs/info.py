from Bot.error.notMainBot import notMainBot
from discord.ext import commands
import discord
import datetime
import re
from Bot.utilities.botCommands import botcommands

if __name__ == "__main__":
  try:
    raise notMainBot()
  except notMainBot as e:
    print(e.mainError)
else:
  bot_version = 0.7 #Versão do bot
  BOT_HELP = botcommands.comandos()

  class Info(commands.Cog):
    def __init__(self, bot):
       self.bot = bot
    
    @commands.command()
    async def version(self, ctx):
        criador = await self.bot.fetch_user('239568901204213760')
        await ctx.send(f'Atualmente estou na versão **{bot_version}**, e meu criador {criador.name} tem muito amor a mim!')

    @discord.app_commands.command(name='versionyay', description='Mostra a versão do bot')
    async def version_tree(self, interaction: discord.Interaction):
        criador = await self.bot.fetch_user('239568901204213760')
        await interaction.response.send_message(f'Atualmente estou na versão **{bot_version}**, e meu criador {criador.name} tem muito amor a mim! <a:BongoCatMany:1476209882582745111>')
    
    @commands.command()
    # Comando pra ver o dia e a hora
    async def diaehora(self, ctx):
      hoje = datetime.datetime.now()
      await ctx.send(f"{hoje.strftime('%A -- %H:%M:%S')}")

    @commands.command()
    # Retorna os dados do usuário no discord
    async def usrdata(self, ctx, usr: discord.User = None):
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


    @commands.command()
    # Retorna a foto de perfil do id/usuario colocado no argumento, se não houver nenhum envia a do próprio autor
    async def fotodata(self, ctx, usr: discord.User = None):
        if usr == None:
            fotousr = ctx.author.display_avatar
            await ctx.reply(f"{fotousr}")
            return
        
        try:
            fotousr = usr.display_avatar
            await ctx.send(f"{fotousr}")

        except Exception as e:
            print(f"ERRO: {e}")

    @commands.command(name='help')
    async def custom_help(self, ctx):
        embed_help = discord.Embed(
            title="Ajuda do Bot 🤖",
            description=BOT_HELP,
            color=discord.Color.red()
        )
        await ctx.send(embed=embed_help)

    @discord.app_commands.command(name='help', description='Puxa os dados de help do bot')
    async def help(self, interaction: discord.Interaction):
        embed_help = discord.Embed(
            title="Ajuda do Bot 🤖",
            description=BOT_HELP,
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed_help)
        

    @commands.command()
    async def ping(self, ctx):
        #PONG
        await ctx.send("Pong :) 🏓")

    # Ping porém em slash / :)
    @discord.app_commands.command(name='pingpong', description='pong!')
    async def pingTree(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Pong! 🏓, {interaction.user.mention}!")