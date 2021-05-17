import yaml
from fastapi import FastAPI
from loguru import logger
from motor import motor_asyncio
from fastapi.middleware.cors import CORSMiddleware

from .service import UserService

VERSION = "1.0"

config = yaml.load(open("config.yaml", "r"), Loader=yaml.FullLoader)

logger.add("backend.log", rotation="1 week")

motor = motor_asyncio.AsyncIOMotorClient(config["core"]["mongodb_url"])
db = motor[config["core"]["mongodb_db"]]
user_service = UserService(db.users)


app = FastAPI(title="poc", version=VERSION)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

from .routes import auth, main  # noqa: E402

app.include_router(router=main.router)
app.include_router(router=auth.router)