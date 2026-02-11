from fastapi import FastAPI, Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI(
    title="FastAPI Blog"
)

templates = Jinja2Templates(
    directory="templates"
)

app.mount("/static",StaticFiles(directory="static"),name="static")


posts: list[dict] = [
    {
        "id": 1,
        "author": "Corey Schafer",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast.",
        "date_posted": "April 20, 2025",
    },
    {
        "id": 2,
        "author": "Jane Doe",
        "title": "Python is Great for Web Development",
        "content": "Python is a great language for web development, and FastAPI makes it even better.",
        "date_posted": "April 21, 2025",
    },
]


@app.get("/",include_in_schema=False,name="home")
@app.get("/posts",include_in_schema=False,name="posts")
def home(request: Request):
    return templates.TemplateResponse(request,"home.html",{"posts" : posts,"title" : "Home"})


@app.get("/posts/{post_id}",status_code=status.HTTP_200_OK,include_in_schema=False)
def get_post_page(post_id: int,request:Request):
    for post in posts:
        
        if post.get("id") == post_id:
            title = post['title'][:50]
            return templates.TemplateResponse(request,"post.html",{"post": post, "title": title})
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The post with the id : {post_id} wasn't found.")


@app.get("/api/posts")
def get_posts():
    return posts
# Automatically converted to JSON Array

@app.get("/api/posts/{post_id}",status_code=status.HTTP_200_OK)
def get_post(post_id: int):
    for i in posts:
        if i.get("id") == post_id:
            return i  
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The post with the id : {post_id} wasn't found.")

