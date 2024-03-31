from fastapi import FastAPI

from app.controllers import posts, users

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
