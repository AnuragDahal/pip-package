from fastapi import HTTPException, APIRouter, Request
from starlette.responses import RedirectResponse
from ..config.oauth_config import google, generate_state, validate_token
from ..handlers.User.userhandler import Validate
from ..core.database import user_collection
from ..utils.jwtutil import create_access_token
from ..handlers.exception import ErrorHandler
from ..utils.envutils import Environment
from datetime import timedelta
env = Environment()


router = APIRouter(tags=['Google OAuth'], prefix='/api/v1/google')


@router.get('/login')
async def login(request: Request):
    state = generate_state()
    request.session['state'] = state
    redirect_uri = request.url_for('auth')
    # print(f"State in /login: {state}")
    return await google.authorize_redirect(request, redirect_uri, state=state)


@router.get('/auth')
async def auth(request: Request):
    state = request.session.get('state')
    stateInQuery = request.query_params.get('state')
    if not state or state != stateInQuery:
        return ErrorHandler.Error(f"State mismatch: session state {state} != query state {stateInQuery}")

    token = await google.authorize_access_token(request)
    id_token = token.get('id_token')

    if not id_token:
        return ErrorHandler.Unauthorized('Unable to authenticate.')

    try:
        claims = validate_token(id_token)
        username = claims.get('name')
        user_email = claims.get('email')
        isEmailVerified = claims.get('email_verified')
        profile_picture = claims.get('picture')

        isUser = await Validate.verify_email(user_email)
        if not isUser:
            await user_collection.insert_one({
                "name": username,
                "email": user_email,
                "password": "google_oauth",  # differentiate OAuth users
                "profile_picture": profile_picture,
                "isEmailVerified": isEmailVerified,
                "friends": [],
                "friend_requests": [],
                "posts": [],
                "commented": [],
                "comments_on_posts": [],
                "likes": [],
            })
        access_token_expires = timedelta(
            minutes=env.ACCESS_TOKEN_EXPIRE_DAYS)
        access_token = create_access_token(
            data={"sub": user_email}, expires_delta=access_token_expires)
    except Exception as e:
        print(f"Token validation error: {e}")
        return ErrorHandler.Unauthorized('Invalid token.')

    return RedirectResponse(url=f'/home?token={access_token}')
