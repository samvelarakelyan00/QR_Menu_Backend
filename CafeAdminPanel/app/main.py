from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.openapi.docs import get_swagger_ui_html

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from api import router


app = FastAPI(title="Cafe Admin Panel",
              docs_url="/api/cafeadmin/docs/")


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
    return get_swagger_ui_html(openapi_url="/api/cafeadmin/openapi.json", title="docs")


@app.get("/")
def main():
    return "Cafe Admin Panel"


@app.get("/cafe-admin-panel")
def index():
    return FileResponse('../../Cafe-Menu/pages/cafeAdminLogin.html')


@app.get("/cafe-admin-my-accout-page")
def index():
    return FileResponse('../../Cafe-Menu/pages/cafeAdminMyAccount.html')


app.include_router(router)
