from realesrgan import RealESRGANer
from PIL import Image
from basicsr.archs.rrdbnet_arch import RRDBNet
import torch
import warnings
import numpy as np
import os
import uuid

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Upscaler():
  def __init__(self):
        print("Inicializando REALESRGAN")
        
        model_path = os.path.join(BASE_DIR, 'RealESRGAN_x4plus.pth')
    
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
        print(f"DISPOSITIVO: {device}")
    
        state_dict = torch.load(model_path, map_location=device)['params_ema']
    
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
        model.load_state_dict(state_dict, strict=True)
    
        half = True if device.type == "cuda" else False
    
        self.upsampler = RealESRGANer(
        scale=4,
        model_path=model_path,
          model=model,
        tile=0,
          pre_pad=0,
          half=half
        )

  def upscale(self, image):
    try:

      img = Image.open(image).convert('RGB')
      img = np.array(img)

      output, _ = self.upsampler.enhance(img, outscale=4)

      output_img = Image.fromarray(output)

      unique_id = uuid.uuid4().hex

      output_img.save(f'{os.path.join(BASE_DIR, unique_id)}.png')
      return f'{os.path.join(BASE_DIR, unique_id)}.png'
    except Exception as e:
      print(e)

  def converterimg(self, caminhoimagem):
    
    imagem = Image.open(caminhoimagem)
    
    imagem = imagem.convert('RGB')

    nome_file = os.path.splitext(os.path.basename(caminhoimagem))[0]
    
    nome_saida = f'{nome_file}' + ".jpg"

    imagem.save(f'{os.path.join(BASE_DIR, nome_saida)}', "JPEG")

    return nome_saida
