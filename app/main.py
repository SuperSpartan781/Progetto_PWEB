from app.config import config  # NB: do not add imports qui!
from pathlib import Path
import os
if Path(__file__).parent == Path(os.getcwd()):
    config.root_dir = "."

from fastapi import FastAPI
from app.routers import frontend
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.data.db import init_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    yield

app = FastAPI(lifespan=lifespan)

app.mount(
    "/static",
    StaticFiles(directory=config.root_dir / "static"),
    name="static"
)

app.include_router(frontend.router)

from app.routers.users import router as users_router
from app.routers.events import router as events_router
from app.routers.registrations import router as registrations_router

app.include_router(users_router)
app.include_router(events_router)
app.include_router(registrations_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
