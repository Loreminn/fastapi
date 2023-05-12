from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from typing import List, Dict, Optional, Any, Union
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


all_posts: List[dict[str, str]] = [
    {"id": 1, "title": "Post 1", "content": "Content 1"},
    {"id": 2, "title": "Post 2", "content": "Content 2"}
]


@app.get('/')
def root() -> Dict[str, str]:
    return {"message": "Welcome to my API"}


@app.get('/posts')
def get_posts() -> Dict[str, List[dict[str, Any]]]:
    return {"data": all_posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post) -> Dict[str, Dict[str, Any]]:
    post_dic = post.dict()
    post_dic['id'] = randrange(0, 100000)
    all_posts.append(post_dic)
    return {"data": post_dic}


def find_post(id: int) -> Optional[dict[str, Any] | None]:
    for post in all_posts:
        if post['id'] == id:
            return post
    return None


@app.get('/posts/{id}')
def get_post(id: int, response: Response) -> Dict[str, Dict[str, Any] | str]:
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"data": post}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    all_posts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    post_dic = post.dict()
    post_dic['id'] = id
    for post in all_posts:
        if post['id'] == id:
            post.update(post_dic)
            return {"data": post}
