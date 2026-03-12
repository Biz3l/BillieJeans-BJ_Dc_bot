from flask import Flask
from threading import Thread
from decouple import config
from flask import request
import sqlite3
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask("API")

limiter = Limiter(
  get_remote_address,
  app=app,
  default_limits=["200 per day", "50 per hour"],
  storage_uri="memory://"
)

@app.route("/")
def home():
  return "Bot funcional!"

def run():
  app.run(host='0.0.0.0', port=8080)

def keepAlive():
  t = Thread(target=run)
  t.start()

@app.route("/pay", methods=["POST"])
@limiter.limit("5 per minute")
def pay():
  CHAVE_SECRETA = config("SECRET_KEY")
  error = 'none'
  data = request.get_json(force=True, silent=True)

  if not data:
    return{"error": "JSON INVÁLIDO!"}, 400
  
  if data.get("SECRET") != CHAVE_SECRETA:
    return {"error": "Não autorizado"}, 403
  
  user = data.get("user")
  user_id = data.get("user_id")
  coins = data.get("coins")

  if not isinstance (coins, int):
    return {"error": "COINS PRECISA SER UMA QUANTIA"}, 400

  if coins <= 0:
    return {"error": "QUANTIDADE INVÁLIDA"}, 400
  
  if coins > 10000:
    return {"ERRO": "QUANTIA MUITO ALTA"}, 400
  
  if not isinstance (user_id, int): 
    return {"ERRO": "USER_ID PRECISA SER UM INTEIRO"}, 400
  
  if not isinstance (user, str) or not user:
    return {"ERRO": "USER INVÁLIDO"}, 400

  try:

    db = "dc_bot.db"
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute("INSERT OR IGNORE INTO users (user_id, user, coins) VALUES (?, ?, ?)", (user_id, user, 0,))

    cur.execute("UPDATE users SET coins = coins + ? WHERE user_id = ?", (coins, user_id,))

    conn.commit()
  except Exception as e:
    return {"error": "Erro Interno"}, 500
  
  finally:
    conn.close()

  return {"SUCESSO": f"MOEDAS ADICIONADAS PARA O USUÁRIO {user} id:{user_id}"}, 200