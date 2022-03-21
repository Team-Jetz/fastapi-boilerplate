from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.exceptions import HTTPException

from sqlalchemy.orm.session import Session
from app.authentication.oauth import get_current_user
from app.authentication.schemas import UserAuth

from app.blog.schemas import PostBase, PostBaseUpdate, PostDisplay, PostVoteDisplay, VoteBase
from app.blog import views

from settings.databases import get_db


router = APIRouter(
    prefix='/posts',
    tags=['posts']
)


# @router.get("/", response_model=List[PostDisplay])
@router.get("/", response_model=List[PostVoteDisplay])
def get_posts(db:Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    return views.get_posts(db, limit, skip, search)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostDisplay)
def create_posts(request: PostBase = Depends(), image: UploadFile = File(None), db: Session  = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    # if not request.author_id:
    #     request.author_id = current_user.id
    return views.create_post(db, request, image, current_user)


@router.get("/{id}", response_model=PostVoteDisplay)
def get_post(id: UUID, db:Session = Depends(get_db)):
    return views.get_post(db, id)


@router.patch("/{id}/update/", response_model=PostDisplay)
def update_post(id: UUID,  request: PostBaseUpdate = Depends(), image: UploadFile = File(None), db:Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return views.update_post(db, id, request, image, current_user)


@router.delete("/{id}/delete/")
def delete_post(id: UUID, db:Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return views.delete_post(db, id, current_user)


@router.post("/{id}/vote")
def vote(id: UUID, db:Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return views.vote(db, id, current_user)
