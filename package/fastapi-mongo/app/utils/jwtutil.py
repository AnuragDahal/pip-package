from datetime import datetime, timedelta, timezone
from ..utils.envutils import Environment
from jose import jwt
import os

env = Environment()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, env.SECRET_KEY,
                             algorithm=env.ALGORITHM)
    return encoded_jwt
