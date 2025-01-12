from fastapi import FastAPI


from models import Base
from database import engine

Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/")
def main():
    return {"message": "This is the main page!!!"}


@app.post("/api/auth/sign-up")
def sign_up():
    pass


@app.post("/api/auth/login")
def login():
    pass

@app.put("/api/users/change-username")
def change_username():
    pass
