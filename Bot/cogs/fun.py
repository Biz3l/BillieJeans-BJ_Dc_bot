from Bot.error.notMainBot import notMainBot
from discord.ext import commands
import discord
import os


if __name__ == "__main__":
  try:
    raise notMainBot()
  except notMainBot as e:
    print(e.mainError)


else:
  BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  class Fun(commands.Cog):
    def __init__(self, bot):
      self.bot = bot

    @commands.command()
    # Um easter egg do bot (Não vou incluir em help nem em readme, vai ficar escondido, só eu sei que existe)
    async def vazio_roxo(self, ctx):
        async with ctx.typing():
            await ctx.send('Vazio Roxo é a combinação da expansão infinita e da absorção infinita \n — a união dessas duas técnicas cria um espaço onde tudo é apagado. \n É o poder de manipular o espaço até que ele deixe de existir, \n tornando tudo que toca simplesmente inexistente.')
            await ctx.send('🫸🔵🔴🫷')
            await ctx.send('**無量空処**')
            await ctx.send('🤌🟣')
            await ctx.send('https://i.pinimg.com/originals/e8/4e/db/e84edb279472c7ab49e97ec276d4ffda.gif')

    @commands.command()                                                                                                
    async def mario(self, ctx):
        #Credo mano
        await ctx.send("WAAAAAAAAAAAAAH", file=discord.File(os.path.join(BASE_DIR, 'images', 'MARIO.jpg')))

    @discord.app_commands.command(name="mariofoto", description="É o MARIO 😣")
    async def mario_tree(self, interaction: discord.Interaction):
        await interaction.response.send_message(file=discord.File(os.path.join(BASE_DIR, "images", "MARIO.jpg")))

    @commands.command()
    async def eleé(self, ctx, pessoa: str = None, *, frase: str = None):
        if pessoa == None or frase == None:
           await ctx.send(f"<:scaryBongo:1481695942146265129> Opa! Parece que ficou faltando um argumento, por favor envie !help para verificar os argumentos que podem ser utilizados")
           return

        if pessoa.lower() == "gabriel" or pessoa.lower() == "biel" or pessoa.lower() == "biz3l":
            await ctx.send(f"{pessoa} é muito macho, não é {frase} não viu")
            return
        else:
            await ctx.send(f"Sim em minha concordância o(a) {pessoa} é {frase}")
            await ctx.send(f"Lembrando, ele gosta de tu hein cuidado")
            return
        
async def setup(bot):
    await bot.add_cog(Fun(bot))