from fastapi import FastAPI
from .routes import auth

app = FastAPI(
    title="BFReport API docs",
    description="""BFReport is a shared report system for the Battlefield series\n
                ...""",
    version="0.0.1",
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(auth.router)