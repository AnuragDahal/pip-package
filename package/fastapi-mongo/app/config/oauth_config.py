from authlib.jose import jwt, JsonWebKey
from authlib.integrations.starlette_client import OAuth
import secrets
import requests
from ..utils.envutils import Environment

env = Environment()
oauth = OAuth()

# Configure the OAuth client
google = oauth.register(
    name='google',
    client_id=env.CLIENT_ID,
    client_secret=env.CLIENT_SECRET,
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)


def generate_state():
    return secrets.token_urlsafe(16)


def validate_token(id_token):
    # Fetch Google's public keys
    jwks_url = 'https://www.googleapis.com/oauth2/v3/certs'
    jwks = requests.get(jwks_url).json()

    # Decode and validate the ID token
    claims = jwt.decode(id_token, key=JsonWebKey.import_key_set(jwks))

    # Validate the 'iss' claim
    valid_issuers = ["https://accounts.google.com", "accounts.google.com"]
    if claims['iss'] not in valid_issuers:
        raise Exception(f"Invalid issuer: {claims['iss']}")

    return claims
