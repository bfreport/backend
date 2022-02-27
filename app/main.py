from fastapi import FastAPI
from .routes import auth
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "https://bfportal.com",
    "http://localhost:8081",
    "http://localhost:8082",
]

app = FastAPI(
    title="BFReport API docs",
    description="""BFReport is a shared report system for the Battlefield series\n
                ...""",
    version="0.0.1",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["Access-Control-Allow-Credentials", "Access-Control-Allow-Origin", "Access-Control-Allow-Headers"],
    max_age=3600,
)

@app.get("/")
async def root():
    response = RedirectResponse(url='/docs')
    return response

app.include_router(auth.router)