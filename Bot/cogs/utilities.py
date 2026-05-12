from error.notMainBot import notMainBot
from discord.ext import commands
import asyncio
from utilities.ytdownloader import ytdownloader
from utilities.enhancer import enhancer
from error.notMainBot import notMainBot
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
  class Utilities(commands.Cog):
    def __init__(self, bot):
      self.bot = bot

    ### NUMERO DE PROCESSOS DO ENHANCER
    Processos = 1

    @commands.command()
    # Comando de Upscaling
    async def upscale(self, ctx, Processos=Processos):

        if not ctx.message.attachments:
            await ctx.reply('Não encontrei nenhum conteúdo anexado!')
        attachment = ctx.message.attachments[0]
        # Verifica se é Imagem
        if not attachment.content_type or not attachment.content_type.startswith("image/"):
            if not attachment.filename.endswith((".png", ".jpg", ".jpeg", ".webp")):
                await ctx.reply("O conteúdo necessita ser uma imagem! 🖨️")
                return
            
        imagemconvertida = None
        imagememupscale = None
        
        try:
            await ctx.reply("Processando imagem, por favor aguarde. ⏳")

            file_path = os.path.join(BASE_DIR, f"utilities/enhancer/{attachment.filename}")

            await attachment.save(file_path)
            
            loop = asyncio.get_event_loop()

            # Pega o nome da imagem convertida e a converte (Já que no caso cada imagem tem nomes diferentes)
            print("Convertendo imagem")

            imagemconvertida = await loop.run_in_executor(None, enhancer.converterimg, os.path.join(BASE_DIR, f"{file_path}"))

            print("Imagem convertida!")


            os.remove(os.path.join(BASE_DIR, f"{file_path}"))


            # Pega o path inteiro do output da imagem em upscale e já upscala a imagem
            imagememupscale = await loop.run_in_executor(None, enhancer.upscale, os.path.join(BASE_DIR, f'utilities/enhancer/{imagemconvertida}'))
            
            print(f"Processo: {Processos} feito com sucesso!")

            await ctx.reply(f"{ctx.author.mention} Aqui está sua imagem:", file=discord.File(os.path.join(BASE_DIR, f"{imagememupscale}")))

            os.remove(os.path.join(BASE_DIR, f"utilities/enhancer/{imagemconvertida}"))

            os.remove(os.path.join(BASE_DIR, f"{imagememupscale}"))

            Processos += 1

        except Exception as e:
            await ctx.reply('Fiquei doidão e não consegui enviar a imagem 😵')
            if hasattr(e, "status") and  e.status == 413:
                await ctx.send("Imagem muito grande!")

            print(f'[ERRO UPSCALE]: {e}')

            if imagemconvertida:
                os.remove(os.path.join(BASE_DIR, f"utilities/enhancer/{imagemconvertida}"))
            if imagememupscale:
                os.remove(os.path.join(BASE_DIR, f"{imagememupscale}"))
            print(f'Imagens apagadas com sucesso')

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