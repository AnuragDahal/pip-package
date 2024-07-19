from fastapi import Request, HTTPException
from fastapi import Request, HTTPException
from jose import jwt, JWTError
from .envutils import Environment
env = Environment()

env = Environment()


async def get_email_from_token(req: Request) -> str:
    auth_header = req.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header[7:]
        try:
            payload = jwt.decode(token, env.SECRET_KEY,
                                 algorithms=[env.ALGORITHM])
            email = payload.get('sub')
            if email is None:
                raise HTTPException(status_code=401, detail="Invalid Token")
            return email
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid Token")
    else:
        raise HTTPException(
            status_code=401, detail="Could not find the appropriate headers")