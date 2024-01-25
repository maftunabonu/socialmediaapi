from typing import Union, Optional
from random import randrange
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

my_posts = []


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


def find_post(post_id):
    for post in my_posts:
        if post_id == post["id"]:
            return post


def find_index_post(post_id):
    for i, post in enumerate(my_posts):
        if post["id"] == post_id:
            return i


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": "banana"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    print(new_post)
    new_post_dict = new_post.model_dump()
    new_post_dict["id"] = randrange(0, 10000000000000000000000)
    my_posts.append(new_post_dict)
    return {"new_post": new_post}


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    post = find_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post not found")
    return {"post_details": post}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    index = find_index_post(post_id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    my_posts.pop(index)
    return {"message": "your post has successfully been delteted"}


@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    index = find_index_post(post_id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    post_dict = post.model_dump()
    post_dict["id"] = post_id
    my_posts[index] = post_dict
    print(my_posts[index])
    return {"message": "updated"}
