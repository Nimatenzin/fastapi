from fastapi import FastAPI
import model
from config import engine
from routes import router
from file_upload import router as file_upload_router
from model import Base
from pydantic import BaseModel
import logging
import datetime

current_datetime = datetime.datetime.now()


logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)

log_file = "app.log"
handler = logging.FileHandler(log_file)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)

model.Base.metadata.create_all(bind=engine)


app = FastAPI()

@app.get("/")
async def read_main():
    logger.info(f"API request received at {current_datetime}")
    return {"msg": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    logger.info(f"Item add API request received at {current_datetime}")
    return {"item_id": item_id, "name": f"Item {item_id}"}


class Post(BaseModel):
    id: int
    title: str
    content: str

@app.post("/posts")
def create_post(post: Post):
    logger.info("API request received")
    return post

app.include_router(router, prefix="/book", tags=["book"])
app.include_router(file_upload_router, prefix="/file", tags=["file"])


