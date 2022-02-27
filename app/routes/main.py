from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.get("/",
    summary="Redirect to docs",
    tags="Default")
async def root():
    response = RedirectResponse(url='/docs')
    return response