from fastapi import Depends, HTTPException, status, Response, Request
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from ..utils.envutils import Environment
from ..core.database import user_collection
from ..utils.passhashutils import Encrypt

env = Environment()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):

    return verify_token


async def verify_token(req: Request, res: Response):
    try:
        token = await req.cookies.get("token")

        if token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials: Token missing",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            payload = jwt.decode(token, env.SECRET_KEY,
                                 algorithms=[env.algorithm])
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        email: str = payload.get("sub")
        password: str = payload.get("password")
        # Check the password from the token
        user = await user_collection.find_one({"email": email})
        if not user or not Encrypt.verify_password(password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials: Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while verifying the token.",
        )
