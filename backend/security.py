import time
from uuid import uuid4
from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from decouple import config

SECRET = config('SECRET')
ALGORITHM = "HS256"

class AccessToken(BaseModel):
  iss: str
  sub: str
  aud: str
  exp: float
  iat: float
  nbf: float
  jti: str

class JWTToken(BaseModel):
  access_token: AccessToken

def sign_jwt(user_id: int) -> JWTToken:
  now = time.time()
  payload = {
    "iss": "bot-billiejeans.com",
    "sub": str(user_id),
    "aud": "bot-billie",
    "exp": now + (60 * 60),
    "iat": now,
    "nbf": now,
    "jti": uuid4().hex,
  }

  token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)

  return {"access_token": token}

async def decode_jwt(token: str) -> JWTToken | None:
  try:
    decoded_jwt = jwt.decode(token, SECRET, audience='bot-billie', algorithms=[ALGORITHM])
    _token = JWTToken.model_validate({"access_token": decoded_jwt})
    return _token if _token.access_token.exp >= time.time() else None
  except Exception:
    return None
  
class JWTBearer(HTTPBearer):
  async def __call__(self, request: Request) -> JWTToken:
      authorization = request.headers.get("Authorization", "")
      scheme, _, credentials, = authorization.partition(" ")

      if credentials:
        if not scheme == "Bearer":
          raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication scheme.")
        
        payload = await decode_jwt(credentials)
        if not payload:
          raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token.")
        return payload
      else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization code.")
      

async def get_current_user(token: Annotated[JWTToken, Depends(JWTBearer())]) -> dict[str, int]:
  return {"user_id": int(token.access_token.sub)}

def login_required(current_user: Annotated[dict[str, int], Depends(get_current_user)]):
  if not current_user:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
  return current_user