from database.connection import metadata, database, engine
from database.models import users
import datetime

class database_bot_services():
  async def create_user_if_not_exist(self, ctx):
    create_user_query = users.insert().values(
            discord_id = ctx.author.id,
            username = ctx.author.display_name,
            avatar = str(ctx.author.display_avatar.url),
        )
    await database.execute(create_user_query)

  async def add_coins_to_user(self, ctx, moedas: int = None):
    try:
        query = users.select().where(users.c.discord_id == ctx.author.id)
        result = await database.fetch_one(query)
        if not result:
            await self.create_user_if_not_exist(ctx)
            print("Usuário criado com Sucesso")
        query_coins = users.update().where(users.c.discord_id == ctx.author.id).values(
            coins = users.c.coins + moedas
        )

        await database.execute(query_coins)

        await ctx.send(f"**{moedas}** 🪙 moedas adicionadas com sucesso!")

    except Exception as e:
        await ctx.send("Erro interno!")
        print(e)
