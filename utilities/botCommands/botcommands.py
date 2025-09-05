def comandos():
  with open('utilities/botCommands/commands.txt', 'r') as file:
    content = file.read();
  return content