import yt_dlp
from yt_dlp import YoutubeDL

def ytdownloader(url):
  caminho_arquivo = None
  def meu_hook(d):
        nonlocal caminho_arquivo  # diz que vamos alterar a variável do escopo externo
        if d['status'] == 'finished':
            caminho_arquivo = d['info_dict']['filepath']

  ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
       'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': './utilities/ytdownloader/%(title)s.%(ext)s',
      # Nome do arquivo de saída
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
                      '(KHTML, like Gecko) Chrome/115.0 Safari/537.36'},
      'postprocessor_hooks': [meu_hook],
      'restrictfilenames': True,
      'noplaylist': True,
}
  
  with YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
  return caminho_arquivo
  
  
