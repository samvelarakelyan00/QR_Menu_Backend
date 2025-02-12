from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from api import router


app = FastAPI(title="Our Admin Panel")


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
    return "Our Admin Panel"


app.include_router(router)
