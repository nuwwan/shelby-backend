from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.models.auth_user import AuthUser  # noqa: F401  (registers the table on Base.metadata)
from app.routes.auth_user import router as auth_user_router


# Create tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

# Include routers  
app.include_router(auth_user_router)


# Root endpoint
@app.get("/")
def read_root():
    return {"Hello": "World"}
