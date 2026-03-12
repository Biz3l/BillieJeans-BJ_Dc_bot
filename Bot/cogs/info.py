from Bot.error.notMainBot import notMainBot

if __name__ == "__main__":
  try:
    raise notMainBot()
  except notMainBot as e:
    print(e.mainError)

#TODO: Construir o restante das cogs