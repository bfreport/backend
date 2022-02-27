from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware

from .routes import auth

origins = [
    "https://bfportal.com",
    "http://localhost:8081",
    "http://localhost:8082",
]
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["POST", "GET"],
        allow_headers=["*"],
        max_age=3600,
    )
]


app = FastAPI(
    title="BFReport API docs",
    description="""BFReport is a shared report system for the Battlefield series\n
                ...""",
    version="0.0.1",
    middleware=middleware
)

@app.get("/")
async def root():
    response = RedirectResponse(url='/docs')
    return response

app.include_router(auth.router)