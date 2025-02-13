from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from api import router


app = FastAPI()

app.mount("/static", StaticFiles(directory="../../Cafe-Menu/static"), name="static")


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


@app.get("/sherep")
def index():
    return FileResponse('../../Cafe-Menu/sherep.html')


@app.get("/menu")
def index():
    return FileResponse('../../Cafe-Menu/pages/menu.html')


app.include_router(router)
