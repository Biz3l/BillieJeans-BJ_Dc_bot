from contextlib import asynccontextmanager
from fastapi import FastAPI
from database.connection import database, metadata, engine
from controllers import health, users

@asynccontextmanager
async def lifespan(app: FastAPI):
  from database.models import users
  await database.connect()
  metadata.create_all(engine)
  yield
  await database.disconnect()

app = FastAPI(lifespan=lifespan, description="Backend/API do nosso querido Bot BillieJeans :)")
app.include_router(health.router)
app.include_router(users.router)

#TODO: Add more routes (auth, add coins, etc.)