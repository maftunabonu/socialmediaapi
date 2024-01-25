from typing import Union, Optional

from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": "banana"}


@app.get("/posts/{post_id}")
def get_post(post_id: int, post: Union[str, None] = None):
    return {"post_id": post_id, "post": "Hello guys"}


@app.post("/createposts")
def create_post(new_post: Post):
    print(new_post)
    new_post.model_dump()
    return {"new_post": new_post}
