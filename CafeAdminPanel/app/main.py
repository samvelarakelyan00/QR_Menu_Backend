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
def cafe_admin_panel():
    return FileResponse('../../Cafe-Menu/pages/cafeAdminLogin.html')


@app.get("/cafe-admin-my-account-page")
def admin_my_accout():
    return FileResponse('../../Cafe-Menu/pages/cafeAdminMyAccount.html')


@app.get("/cafe-admin-pricing")
def get_pricing_page():
    return FileResponse('../../Cafe-Menu/pages/pricing.html')


@app.get("/cafe-admin-menu")
def admin_menu():
    return FileResponse('../../Cafe-Menu/pages/adminMenu.html')


@app.get("/cafe-admin-menu-about-meal")
def admin_about_meal():
    return FileResponse('../../Cafe-Menu/pages/adminMenuAboutMeal.html')


@app.get("/cafe-admin-menu-add-meal")
def admin_add_meal():
    return FileResponse('../../Cafe-Menu/pages/addMeal.html')


@app.get("/cafe-admin-terms/{term}/{lang}")
def admin_get_term(term, lang):
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


app.include_router(router)
