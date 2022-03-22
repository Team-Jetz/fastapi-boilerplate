from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from settings.config import CORS_ALLOWED_ORIGINS
# from settings.databases import engine

from app.account import routes as AccountRouter
from app.authentication import routes as AuthenticationRouter
from app.blog import routes as BlogRouter


app = FastAPI()

origins = CORS_ALLOWED_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(AccountRouter.router)
app.include_router(AuthenticationRouter.router)
app.include_router(BlogRouter.router)


@app.get("/")
async def root():
    print(datetime.now())
    return {
        "message":"Hello World"
    }

# If you are not using alembic you can uncomment the line below
# BlogModels.Base.metadata.create_all(engine)