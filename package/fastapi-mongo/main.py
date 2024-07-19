from fastapi import FastAPI, Query, Response, Request
from app.apis import user, auth, google, posts, comments, friends
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import client
from starlette.middleware.sessions import SessionMiddleware
from app.utils.envutils import Environment
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


env = Environment()

app = FastAPI(title="CONNECTIFY", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["http://localhost:5173", "http://localhost:8000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=env.OAUTHSECRET_KEY)

try:
    client.admin.command("ping")
    print("Connected to MongoDB")
except Exception as e:
    print("Failed to connect to MongoDB")
    print(e)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Customize the response as needed
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Invalid email type "},
    )


@app.get('/')
def root():
    return {"message": "Welcome to Webservice API, navigate to /docs for documentation."}


@app.get('/home')
def home(res: Response = None, token: str = Query(...)):
    # res.set_cookie(key="token", value=token, expires=18000)
    return {"message": "You have been logged in through Google OAuth."}


# include routers from routers folder
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(google.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(friends.router)
