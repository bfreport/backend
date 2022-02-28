from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

from ..config import Config
from authlib.jose import jwt
from ..auth import sdk, get_current_user, User

router = APIRouter()


@router.get("/auth/callback",
            summary="save auth",
            tags=["Auth"]
            )
async def callback(code: str):
    token = sdk.get_oauth_token(code)
    try:
        payload = jwt.decode(token, Config.Auth.pub_key)
    except:
        payload = None
    id: str = payload.get("sub")
    if id is None:
        raise HTTPException(
            status_code=403, detail="Error authenticating"
        )
    response = RedirectResponse(url=Config.Auth.redirect_location)
    response.set_cookie(
        "Authorization",
        value=f"Bearer {token}",
        domain=Config.Auth.domain,
        httponly=True,
        max_age=3600,
        expires=3600,
    )
    return response


@router.get('/locallogin',
            summary="Do login action within test env",
            tags=["Auth"])
async def login():
    return RedirectResponse(url='https://auth.bfreport.com/login/oauth/authorize?client_id=6493dc8b964b65fc0591&response_type=code&redirect_uri=https%3A%2F%2Flocalhost%3A5051%2Fauth%2Fcallback&scope=read&state=test-app')


@router.get('/login',
            summary="Do login action",
            tags=["Auth"])
async def login():
    return RedirectResponse(url='https://auth.bfreport.com/login/oauth/authorize?client_id=994c97aa8467ae9acf48&response_type=code&redirect_uri=https://api.bfreport.com/auth/callback&scope=read&state=bfreport_main')


@router.get("/auth/logout",
            summary="Delete the session",
            tags=["Auth"])
async def route_logout_and_remove_cookie():
    response = RedirectResponse(url="/")
    response.delete_cookie("Authorization", domain=Config.Auth.domain)
    return response


@router.get("/auth/current",
            summary="Get the current user",
            tags=["Auth"])
async def current_user(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.sub,
        "name": current_user.name,
        "avatar": current_user.avatar,
        "createdAt": current_user.createdTime,
        "email": current_user.email,
        "displayName": current_user.displayName
    }
