from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str


class Post(BaseModel):
    text: str


class PostFromUserRequest(Post):
    pass


class PostFromDB(Post):
    pass


class PostID(BaseModel):
    post_id: int


class Token(BaseModel):
    access_token: str
    token_type: str
