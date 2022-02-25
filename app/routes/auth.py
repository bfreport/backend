from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from oauth.main import CasdoorSDK
from authlib.jose import jwt
from authlib.jose.errors import DecodeError
from ..config import Config
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.security import OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel

from starlette.responses import RedirectResponse
from starlette.status import HTTP_403_FORBIDDEN
from starlette.requests import Request

router = APIRouter()

sdk = CasdoorSDK(
    Config.Auth.url,
    Config.Auth.client_id,
    Config.Auth.client_secret,
    Config.Auth.pub_key,
    Config.Auth.org,
)

class DictToUser(object):
    def __init__(self, user_dict):
        for key in user_dict:
            setattr(self, key, user_dict[key])

class User:
    sub: str
    name: str
    createdTime: str
    displayName: str
    avatar: str
    type: str
    email: str

class OAuth2PasswordBearerCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        header_authorization: str = request.headers.get("Authorization")
        cookie_authorization: str = request.cookies.get("Authorization")

        header_scheme, header_param = get_authorization_scheme_param(
            header_authorization
        )
        cookie_scheme, cookie_param = get_authorization_scheme_param(
            cookie_authorization
        )

        if header_scheme.lower() == "bearer":
            authorization = True
            scheme = header_scheme
            param = header_param

        elif cookie_scheme.lower() == "bearer":
            authorization = True
            scheme = cookie_scheme
            param = cookie_param

        else:
            authorization = False

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None
        return param

oauth2_scheme = OAuth2PasswordBearerCookie(tokenUrl="/token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, Config.Auth.pub_key)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except DecodeError:
        raise credentials_exception
    user = DictToUser(payload)
    return user

@router.get("/auth/callback", 
    summary="save auth"
    )
async def callback(code: str):
    token = sdk.get_oauth_token(code)
    response = RedirectResponse(url="/auth/test")
    response.set_cookie(
            "Authorization",
            value=f"Bearer {token}",
            domain=Config.Auth.domain,
            httponly=True,
            max_age=1800,
            expires=1800,
    )
    return response

@router.get('/locallogin')
async def login():
    return RedirectResponse(url='https://auth.bfreport.com/login/oauth/authorize?client_id=6493dc8b964b65fc0591&response_type=code&redirect_uri=https%3A%2F%2F127.0.0.1%3A5051%2Fauth%2Fcallback&scope=read&state=test-app')

@router.get('/login')
async def login():
    return RedirectResponse(url='https://auth.bfreport.com/login/oauth/authorize?client_id=994c97aa8467ae9acf48&response_type=code&redirect_uri=https://api.bfreport.com/auth/callback&scope=read&state=bfreport_main')

@router.get("/auth/logout")
async def route_logout_and_remove_cookie():
    response = RedirectResponse(url="/")
    response.delete_cookie("Authorization", domain=Config.Auth.domain)
    return response

@router.get("/auth/test")
async def test(current_user: User = Depends(get_current_user)):
    return {"name": current_user.name}