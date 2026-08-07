from Bot.error.notMainBot import notMainBot
from discord.ext import commands
import asyncio
from Bot.utilities.ytdownloader import ytdownloader
from discord.ext import commands
import discord
import os
from Bot.services.Upscaler.instance import upscale_queue_services


if __name__ == "__main__":
  try:
    raise notMainBot()
  except notMainBot as e:
    print(e.mainError)

else:
  BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  class Utilities(commands.Cog):
    def __init__(self, bot):
      self.bot = bot

    ### NUMERO DE PROCESSOS DO ENHANCER
    Processos = 1

    @commands.command()
    # Comando de Upscaling
    async def upscale(self, ctx):

        if not ctx.message.attachments:
            await ctx.reply('Não encontrei nenhum conteúdo anexado!')
        attachment = ctx.message.attachments[0]
        # Verifica se é Imagem
        if not attachment.content_type or not attachment.content_type.startswith("image/"):
            if not attachment.filename.endswith((".png", ".jpg", ".jpeg", ".webp")):
                await ctx.reply("O conteúdo necessita ser uma imagem! 🖨️")
                return
        
        await ctx.reply(f"Imagem enviada! a sua imagem é a **{upscale_queue_services.get_queue_size()}** na fila, por favor aguarde⏳")

        file_path = os.path.join(BASE_DIR, f"services/Upscaler/{attachment.filename}")

        await attachment.save(file_path)

        await upscale_queue_services.add_job(ctx, file_path)

    @commands.command()
    # Comando para download de links mp3 do yt!
    async def ytdl(self, ctx, url = None):
        if url == None:
            await ctx.reply('Não encontrei nenhuma URL especificada! Para entender o comando envie "!help" !')
            return
        
        caminhodownload = None

        await ctx.send(f'PROCESSANDO :) \n**ATENÇÃO**, caso o arquivo enviado resulte em mais que 8mb, variando do server, há a possibilidade do arquivo não ser enviado!')
        
        try:
            loop = asyncio.get_event_loop()
            caminhodownload = await loop.run_in_executor(None, ytdownloader.ytdownloader, f"{url}")

            if caminhodownload == None:
                await ctx.send('ERRO: Arquivo não encontrado, possivelmente falha no download')
            
            if os.path.getsize(caminhodownload) > 8 * 1024 * 1024:
                await ctx.send('ERRO: Arquivo grande demais para envio no discord!')
                os.remove(caminhodownload)
                return
            
            await ctx.send(f"{ctx.author.mention} Aqui está seu arquivo baixado:", file=discord.File(os.path.join(BASE_DIR, f"{caminhodownload}")))
            os.remove(caminhodownload)

        except Exception as e:
            await ctx.send(f'Erro ao processar vídeo')
            print(f"Erro Processamento de vídeo: {e}")
            if caminhodownload and os.path.exists(caminhodownload):
                os.remove(caminhodownload)
                return
            return

    @discord.app_commands.command(name="ytdl", description="Faz um download em mp3 do youtube pra você :)")
    @discord.app_commands.describe(url="URL do vídeo que queira baixar!!")
    async def ytdl_tree(self, interaction: discord.Interaction, url: str):
        if url == None:
            await interaction.response.send_message("Não encontrei nenhuma url especificada!")
            return
        await interaction.response.defer(thinking=True)

        caminhodownload = None
        try:
            loop = asyncio.get_event_loop()
            caminhodownload = await loop.run_in_executor(None, ytdownloader.ytdownloader, f"{url}")

            if caminhodownload == None:
                await interaction.followup.send('ERRO: Arquivo não encontrado, possivelmente falha no download')
            
            if os.path.getsize(caminhodownload) > 8 * 1024 * 1024:
                await interaction.followup.send('ERRO: Arquivo grande demais para envio no discord!')
                os.remove(caminhodownload)
                return
            
            await interaction.followup.send(f"Aqui está seu arquivo baixado:", file=discord.File(os.path.join(BASE_DIR, f"{caminhodownload}")))
            os.remove(caminhodownload)

        except Exception as e:
            await interaction.followup.send(f'Erro ao processar vídeo')
            print(f"Erro Processamento de vídeo: {e}")
            if caminhodownload and os.path.exists(caminhodownload):
                os.remove(caminhodownload)
                return
            return
        
async def setup(bot):
    await bot.add_cog(Utilities(bot))