import os
from datetime import timedelta, datetime
from typing import Optional

from fastapi import Depends
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer

from .db import get_user
from .exceptions import CREDENTIALS_EXCEPTION

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_encoded_jwt(data):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def get_decode_jwt(token):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return get_encoded_jwt(to_encode)

async def get_current_username(token: str = Depends(oauth2_scheme)):
    """
        token을 통해 username 획득
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise CREDENTIALS_EXCEPTION
    except JWTError:
        raise CREDENTIALS_EXCEPTION
    user = get_user(username=username)
    if user is None:
        raise CREDENTIALS_EXCEPTION
    return user.username