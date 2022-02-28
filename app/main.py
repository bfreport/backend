from fastapi import FastAPI, Request
from fastapi.responses import Response

from .routes import auth, main

app = FastAPI(
    title="BFReport API docs",
    description="""BFReport is a shared report system for the Battlefield series\n
                ...""",
    version="0.0.1",
)

app.include_router(main.router)
app.include_router(auth.router)

@app.options("/{rest_of_path:path}")
async def preflight_handler(request: Request, rest_of_path: str) -> Response:
    """
    Handles CORS preflight requests.
    """
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = "https://bfportal.com"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, DELETE, PATCH, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
    return response

@app.middleware("http")
async def add_cors_header(request: Request, call_next):
    """
    Sets CORS headers.
    """
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "https://bfportal.com"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, DELETE, PATCH, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
    return response

# return CORSMiddleware(
#     fastapi_app,
#     allow_origins=[
#         "https://bfportal.com",
#         "http://localhost:8081",
#         "http://localhost:8082",
#     ],
#     allow_credentials=True,
#     allow_methods=["POST", "GET", "OPTIONS"],
#     allow_headers=[
#         "Access-Control-Allow-Headers",
#         "Origin",
#         "Accept",
#         "X-Requested-With",
#         "Content-Type",
#         "Access-Control-Request-Method",
#         "Access-Control-Request-Headers",
#         "Access-Control-Allow-Credentials",
#         "Access-Control-Allow-Origin",
#         "Access-Control-Allow-Methods"
#         "Authorization",
#         "X-Amz-Date",
#         "X-Api-Key",
#         "X-Amz-Security-Token"
#     ],
#     max_age=3600,
# )