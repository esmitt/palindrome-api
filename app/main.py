import os
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.api.endpoints import router as api_router
from app.db.base import get_engine, init_db
from app.db.models import Base
from app.core.config import get_settings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # init the database at startup
    engine = get_engine()
    print("Initializing database...")
    init_db(engine=engine, base=Base)
    print("Database initialized.")
    yield
    # clean up
    print("Application is shutting down. Cleaning up resources...")


app = FastAPI(
    title=get_settings().APP_NAME,
    description=get_settings().DESCRIPTION,
    version=get_settings().VERSION,
    root_path=get_settings().API_PREFIX,
    lifespan=lifespan
)

app.include_router(api_router)

# Handle any SQLAlchemy-related errors globally
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"info": "A database error occurred."},
    )


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=os.getenv("ENVIRONMENT", "production") == "development"
    )
