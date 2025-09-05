from realesrgan import RealESRGANer
from PIL import Image
from basicsr.archs.rrdbnet_arch import RRDBNet
import torch
import warnings
import numpy as np
import os
import uuid


warnings.filterwarnings('ignore')

def upscale(image):

  model_path = 'utilities/enhancer/RealESRGAN_x4plus.pth'

  state_dict = torch.load(model_path, map_location=torch.device('cuda'))['params_ema']

  model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
  model.load_state_dict(state_dict, strict=True)

  upsampler = RealESRGANer(
   scale=4,
   model_path=model_path,
    model=model,
   tile=0,
    pre_pad=0,
    half=True
  )

  img = Image.open(image).convert('RGB')
  img = np.array(img)

  output, _ = upsampler.enhance(img, outscale=4)

  output_img = Image.fromarray(output)

  unique_id = uuid.uuid4().hex

  output_img.save(f'utilities/enhancer/{unique_id}.png')
  return f'utilities/enhancer/{unique_id}.png'


def converterimg(caminhoimagem):
  imagem = Image.open(caminhoimagem)
  
  imagem = imagem.convert('RGB')

  nome_file = os.path.splitext(os.path.basename(caminhoimagem))[0]
  
  nome_saida = f'{nome_file}' + ".jpg"

  imagem.save(f'utilities/enhancer/{nome_saida}', "JPEG")

  print('Imagem Salva com Sucesso!')

  return nome_saida

  