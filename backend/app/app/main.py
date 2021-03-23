from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings
import uvicorn
import os

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        # allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    pass

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=os.environ.get("UVICORN_HOST"),
        port=int(os.environ.get("UVICORN_PORT")),
        reload=True if os.environ.get("UVICORN_MODE") == "DEBUG" else False,
        debug=True if os.environ.get("UVICORN_MODE") == "DEBUG" else False,
        workers=int(os.environ.get("UVICORN_WORKERS")),
    )
