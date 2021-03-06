from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import auth, main

app = FastAPI(
    title="BFReport API docs",
    description="""BFReport is a shared report system for the Battlefield series\n
                ...""",
    version="0.0.1",
)

app.include_router(main.router)
app.include_router(auth.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://bfreport.com",
        "http://localhost:8081",
        "http://localhost:8082",
    ],
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=[
        "Authorization",
        "Content-Type"
    ],
    max_age=43200,
)