from fastapi import FastAPI, Depends
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from fastapi.openapi.docs import get_swagger_ui_html

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from schemas.user_schemas import (
    UserScanQRSchema
)

from services.user import UserService

from api import router


app = FastAPI(docs_url="/api/docs/")
# Mount static files
app.mount("/static", StaticFiles(directory="../../Cafe-Menu/static"), name="static")
origins = ["*"]

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



@app.get("/")
def menu():
    return FileResponse('../../Cafe-Menu/main.html')


@app.get("/{id}")
def index(id: int,
          user_service: UserService=Depends()):
    qr_scan_data = UserScanQRSchema(horeka_client_id=id)

    user_service.scan_qr_info(qr_scan_data)

    return FileResponse('../../Cafe-Menu/index.html')


@app.get("/cafe/menu/get-menu")
def menu():
    return FileResponse('../../Cafe-Menu/pages/menu.html')


@app.get("/cafe/menu/get-about-meal")
def menu():
    return FileResponse('../../Cafe-Menu/pages/about-meal.html')


@app.get("/cafe/menu/feedback")
def menu():
    return FileResponse('../../Cafe-Menu/pages/feedback.html')


@app.get("/cafe/menu/tip")
def menu():
    return FileResponse('../../Cafe-Menu/pages/tip.html')


@app.get("/cafe/menu/users/{term}/{lang}")
def user_get_term(term, lang):
    try:
        if term == "cancellation_policy":
            if lang == "en":
                return FileResponse('../../Cafe-Menu/pages/Terms/EN/cancellation_policy.html')
            elif lang == "ru":
                return FileResponse('../../Cafe-Menu/pages/Terms/RU/cancellation_policy.html')
            elif lang == "hy":
                return FileResponse('../../Cafe-Menu/pages/Terms/HY/cancellation_policy.html')
        elif term == "privacy_policy":
            if lang == "en":
                return FileResponse('../../Cafe-Menu/pages/Terms/EN/privacy_policy.html')
            elif lang == "ru":
                return FileResponse('../../Cafe-Menu/pages/Terms/RU/privacy_policy.html')
            elif lang == "hy":
                return FileResponse('../../Cafe-Menu/pages/Terms/HY/privacy_policy.html')
        elif term == "terms_of_use":
            if lang == "en":
                return FileResponse('../../Cafe-Menu/pages/Terms/EN/terms_of_use.html')
            elif lang == "ru":
                return FileResponse('../../Cafe-Menu/pages/Terms/RU/terms_of_use.html')
            elif lang == "hy":
                return FileResponse('../../Cafe-Menu/pages/Terms/HY/terms_of_use.html')
        if term == "personal_data":
            if lang == "en":
                return FileResponse('../../Cafe-Menu/pages/Terms/EN/personal_data.html')
            elif lang == "ru":
                return FileResponse('../../Cafe-Menu/pages/Terms/RU/personal_data.html')
            elif lang == "hy":
                return FileResponse('../../Cafe-Menu/pages/Terms/HY/personal_data.html')
    except Exception:
        raise HTTPException(status_code=500)


app.include_router(router)
