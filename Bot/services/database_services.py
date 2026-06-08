from database.connection import metadata, database, engine
from database.models import users
import datetime

class database_bot_services():
  async def create_user_if_not_exist(self, ctx):
    create_user_query = users.insert().values(
            discord_id = ctx.author.id,
            username = ctx.author.display_name,
            avatar = str(ctx.author.display_avatar.url),
            coins = 0,
            joined_at = datetime.datetime.now(),
        )
    await database.execute(create_user_query)