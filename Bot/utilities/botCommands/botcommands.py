import os

def comandos():
  with open(os.path.join((os.path.dirname(os.path.abspath(__file__))), "commands.txt"), 'r') as file:
    content = file.read();
  return content