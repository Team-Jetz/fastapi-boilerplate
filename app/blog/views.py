from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session
from app.blog.models import Post, Votes
from sqlalchemy import update, desc, func
from custom_functions import image_editor

from custom_functions.query import dynamic_update
from settings.s3_storage import S3Storage

def create_post(db: Session, request, image, current_user):
    if image:
        filename = image_editor.img_file_name_generator(image)
        request.image_url = S3Storage.upload_image(image, filename)

    # post = Post(
    #     title = request.title,
    #     content = request.content,
    #     author_id = request.author_id
    # )
    post = Post(**request.dict())
    post.author_id =  current_user.id
    # print(request.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def get_posts(db: Session, limit, skip, search):
    results = db.query(
        Post, func.count(Votes.post_id).label("votes")
    ).join(
        Votes, Votes.post_id == Post.id, isouter=True
    ).group_by(Post.id).filter(
        Post.title.contains(search)
    ).order_by(desc(Post.created_at)).limit(limit).offset(skip).all()

    # post = db.query(Post).filter(Post.title.contains(search)).order_by(desc(Post.created_at)).limit(limit).offset(skip).all()

    return results


def get_post(db: Session, id):
    return db.query(
        Post, func.count(Votes.post_id).label("votes")
    ).join(
        Votes, Votes.post_id == Post.id, isouter=True
    ).group_by(Post.id).filter(Post.id == id).first()


def update_post(db: Session, id, request, image, current_user):
    post = db.query(Post).filter(Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} not found.')

    if post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'You cannot update any post you did not authored.')

    if image:
        filename = image_editor.img_file_name_generator(image)
        request.image_url = S3Storage.upload_image(image, filename)

    if request.remove_image:
        request.image_url = None

    dynamic_update(db, post, request)

    db.refresh(post)

    return post


def delete_post(db: Session, id, current_user):
    post = db.query(Post).filter(Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} not found.')

    if post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'You cannot delete a post you did not authored.')

    db.delete(post)
    db.commit()

    return {
        'message':'The post has been successfully deleted.'
    }


def vote(db: Session, id, current_user):
    post = db.query(Post).filter(Post.id==id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'Post does not exist.')

    vote = db.query(Votes).filter(Votes.post_id == id, Votes.user_id == current_user.id).first()

    if not vote:
        vote = Votes(
            post_id = id,
            user_id = current_user.id
        )

        db.add(vote)
        db.commit()

        return {
            "message":f"You casted a voted in a post with an id of {post.id}."
        }

    else:

        if vote.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'You are not allowed to unvote on this post.')

        db.delete(vote)
        db.commit()

        return {
            "message":f"You uncast your vote in a post with an id of {post.id}."
        }
