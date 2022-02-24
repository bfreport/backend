from fastapi import APIRouter
from oauth.main import CasdoorSDK
from authlib.jose import jwt
from config import Config

router = APIRouter()


sdk = CasdoorSDK(
    Config.Auth.url,
    Config.Auth.client_id,
    Config.Auth.client_secret,
    Config.Auth.pub_key,
    Config.Auth.org,
)

@router.get("/auth/callback", 
    summary="save auth"
    )
async def login(code: str):
    access_token = sdk.get_oauth_token(code)
    # save this
    
    # use in program
    decoded_msg = jwt.decode(access_token, Config.Auth.pub_key)
    