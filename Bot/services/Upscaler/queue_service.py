import asyncio
import os
from Bot.services.Upscaler.model_service import Upscaler
from discord import File

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class UpscaleQueueService():

  def __init__(self):
    self.queue = asyncio.Queue()
    self.worker_task = None
    self.upscaler = Upscaler()

  async def start(self):
    self.worker_task = asyncio.create_task(self.worker())

  async def worker(self):
    #FIXME: Arrumar a questão do bot travar o fluxo totalmente com imagens grandes
    while True:
      ctx, image_path = await self.queue.get()
      try:
        await ctx.send(f"{ctx.author.mention} processando sua Imagem agora!")
        final_path = await asyncio.to_thread(self.upscale_image, image_path)
        await ctx.reply(
                  f"{ctx.author.mention} Aqui está sua imagem:",
                  file=File(final_path))
      except Exception as e:
        print(e)
      finally:
        os.remove(os.path.join(BASE_DIR, f"{final_path}"))
        self.queue.task_done()

  async def add_job(self, ctx, image_path):
    await self.queue.put((ctx, image_path))

  def get_queue_size(self):
    return self.queue.qsize() + 1
  
  def upscale_image(self, image_path):    
        imagem_em_upscale = None
        imagem_convertida = None
        print("Convertendo imagem")
        imagem_convertida = self.upscaler.converterimg(image_path)
        print("Imagem convertida")
        os.remove(os.path.join(BASE_DIR, f"{image_path}"))
        imagem_em_upscale = self.upscaler.upscale(os.path.join(BASE_DIR, f"Upscaler/{imagem_convertida}"))
        os.remove(os.path.join(BASE_DIR, f"Upscaler/{imagem_convertida}"))
        return imagem_em_upscale
        
