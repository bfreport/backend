from fastapi import FastAPI

app = FastAPI(
    title="BFReport API docs",
    description="""BFReport is a shared report system for the Battlefield series\n
                ...""",
    version="0.0.1",
)

@app.get("/")
def root():
    return {"message": "Hello World"}