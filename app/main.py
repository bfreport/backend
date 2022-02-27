from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import auth, main

def create_app() -> CORSMiddleware:
    """Create app wrapper to overcome middleware issues."""
    fastapi_app = FastAPI(
        title="BFReport API docs",
        description="""BFReport is a shared report system for the Battlefield series\n
                    ...""",
        version="0.0.1",
    )
    fastapi_app.include_router(main.router)
    fastapi_app.include_router(auth.router)
    return CORSMiddleware(
        allow_origins=[
            "https://bfportal.com",
            "http://localhost:8081",
            "http://localhost:8082",
        ],
        allow_credentials=True,
        allow_methods=["POST", "GET", "OPTIONS"],
        allow_headers=[
            "Access-Control-Allow-Headers",
            "Origin",
            "Accept",
            "X-Requested-With",
            "Content-Type",
            "Access-Control-Request-Method",
            "Access-Control-Request-Headers",
            "Access-Control-Allow-Credentials",
            "Access-Control-Allow-Origin",
            "Access-Control-Allow-Methods"
            "Authorization",
            "X-Amz-Date",
            "X-Api-Key",
            "X-Amz-Security-Token"
        ],
        max_age=3600,
    )


app = create_app()