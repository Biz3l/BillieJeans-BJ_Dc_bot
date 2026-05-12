from datetime import datetime
from pydantic import BaseModel

class userCreateOut(BaseModel):
  id: int
  coins: int
  created_at: datetime