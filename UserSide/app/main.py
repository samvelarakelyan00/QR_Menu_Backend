import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.openapi.docs import get_swagger_ui_html

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from api import router


app = FastAPI(docs_url="/api/docs/")

# Get the absolute path to the Cafe-Menu folder
# base_dir = os.path.dirname(os.path.abspath(__file__))  # This is your backend folder
# static_dir = os.path.join(base_dir, "../..", "Cafe-Menu", "static")  # Go up one level and into Cafe-Menu

# Mount static files
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


@app.get("/docs/", include_in_schema=False)
async def get_docs():
    return get_swagger_ui_html(openapi_url="/api/openapi.json", title="docs")


@app.get("/{id}")
def index():
    return FileResponse('../../Cafe-Menu/index.html')


@app.get("/cafe/menu/get-menu")
def menu():
    return FileResponse('../../Cafe-Menu/pages/menu.html')


@app.get("/cafe/menu/get-about-meal")
def menu():
    return FileResponse('../../Cafe-Menu/pages/about-meal.html')


app.include_router(router)
