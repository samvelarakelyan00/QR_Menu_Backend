from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount("/static", StaticFiles(directory="../../cafeMenu-example/static"), name="static")


origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def main():
    return "OK"


@app.get("/index")
def index():
    return FileResponse("../../cafeMenu-example/index.html")


@app.get("/appetizers")
def get_appetizers_html_page():
    return FileResponse("../../cafeMenu-example/appetizers.html")


@app.get("/desserts")
def get_desserts_html_page():
    return FileResponse("../../cafeMenu-example/desserts.html")


@app.get("/drinks")
def get_drinks_html_page():
    return FileResponse("../../cafeMenu-example/drinks.html")


@app.get("/main-dishes")
def get_main_dishes_html_page():
    return FileResponse("../../cafeMenu-example/main-dishes.html")
