from fastapi import FastAPI
import app.blog.routes as BlogRouter
app = FastAPI()

app.include_router(BlogRouter.router)

@app.get("/")
async def root():
    return {
        "message":"Hello World"
    }
