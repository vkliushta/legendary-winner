from sys import getsizeof
from typing import Annotated

from cachetools import TTLCache, cached
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.controllers.users import get_current_user_id
from app.database import get_db
from app.models import models
from app.views import models as views_models

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[views_models.PostFromDB],
)
@cached(cache=TTLCache(maxsize=1024, ttl=600))
def get_posts(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    user_id = get_current_user_id(token)
    posts = db.query(models.Post).filter(models.Post.user_id == user_id).all()
    return posts


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=views_models.PostID
)
def add_post(
    token: Annotated[str, Depends(oauth2_scheme)],
    text: views_models.PostFromUserRequest,
    db: Session = Depends(get_db),
):
    if getsizeof(text) > 1024 * 1024:  # 1MB in bytes
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Text size run out of the 1MB limit",
        )

    user_id = get_current_user_id(token)
    new_post = models.Post(text=text, user_id=user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return views_models.PostID(post_id=new_post.id)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    token: Annotated[str, Depends(oauth2_scheme)],
    post_id: int,
    db: Session = Depends(get_db),
):
    post = db.query(models.Post).filter(models.Post.id == post_id)

    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with {post_id=} not found",
        )
    user_id = get_current_user_id(token)
    if post.first().user_id != int(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Missing permissions to delete post with {post_id=}",
        )
    post.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
