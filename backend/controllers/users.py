from fastapi import APIRouter, HTTPException, status
from schemas.users import userIn
from models.users import users
from db import database
from datetime import datetime
from views.users import userCreateOut

router = APIRouter(prefix='/users')



@router.post('/addUser', response_model=userCreateOut)
async def add_user(user: userIn):
  query = users.insert().values(
    discord_id = user.discord_id,
    coins = 0,
    joined_at = datetime.now()
  )

  await database.execute(query)

  return {
    "id": user.discord_id,
    "coins": 0,
    "created_at": datetime.now()  
  }


@router.post('/getUser')
async def get_user(user: userIn):
  query = users.select().where(users.c.discord_id == user.discord_id)
  discord_user = await database.fetch_one(query)

  if not discord_user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
  

  return {
    discord_user
  }