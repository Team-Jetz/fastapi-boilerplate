from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.exceptions import HTTPException
from app.blog.models import Post

router = APIRouter(
    prefix='/posts',
    tags=['posts']
)

my_posts = [
    {
        "title":"title of post",
        "content": "content of post",
        "id":1
    },
    {
        "title":"title of second post",
        "content": "content of post",
        "id":2
    },
]

@router.post("/")
def create_posts(post: Post):
    return post

@router.get("/")
def get_posts():
    return my_posts

@router.get("/{id}")
def get_post(id):
    post =  id
    return post

@router.patch("/{id}/update/")
def update_post(id):
    post =  id
    return {
        "message":"Post was successfully updated."
    }

@router.delete("/{id}/delete/")
def delete_post(id):
    post =  id
    return {
        "message":"Post was successfully deleted."
    }