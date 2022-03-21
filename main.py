from fastapi import FastAPI
# from settings.databases import engine

from app.account import routes as AccountRouter
from app.authentication import routes as AuthenticationRouter
from app.blog import routes as BlogRouter


app = FastAPI()

app.include_router(AccountRouter.router)
app.include_router(AuthenticationRouter.router)
app.include_router(BlogRouter.router)


@app.get("/")
async def root():
    return {
        "message":"Hello World"
    }

# If you are not using alembic you can uncomment the line below
# BlogModels.Base.metadata.create_all(engine)