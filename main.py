from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.responses import ORJSONResponse


from models import Base, User
from database import engine, SessionLocal
from schemas import (
    UserSignupSchema,
    UserLoginSchema,
    UsernameChangeSchema
)
from security import get_current_user, create_token


Base.metadata.create_all(bind=engine)

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Max-Age": "3600"
}


app = FastAPI()


@app.get("/")
def main():
    return ORJSONResponse(content={"message": "This is the main page!"},
                          headers=CORS_HEADERS)


@app.get("/api/users")
def get_all_users():
    try:
        session = SessionLocal()

        all_users = session.query(User).all()

        return all_users
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while trying to get all users!"
                   f"ERR: {err}"
        )


@app.get("/api/users/{id}")
def get_all_users(id: int):
    try:
        session = SessionLocal()
        user = session.query(User).filter_by(id=id).first()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error while trying to get the user with id '{id}'!"
                   f"ERR: {err}"
        )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id '{id}' was not found!"
        )

    return user


@app.post("/api/auth/sign-up")
def sign_up(user_signup_data: UserSignupSchema):
    try:
        session = SessionLocal()

        new_user = User(**user_signup_data.dict())

        session.add(new_user)
        session.commit()
        session.close()
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error while trying to add user to db"
                                   f"ERR: {err}")

    return ORJSONResponse(content={"message": "User successfully signup!"},
                          headers=CORS_HEADERS)


@app.post("/api/auth/login")
def login(user_login_data: UserLoginSchema):
    session = SessionLocal()

    user = session.query(User).filter_by(username=user_login_data.username).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username '{user_login_data.username}' was not found!"
        )

    if user.__dict__.get("password") != user_login_data.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Wrong password '{user_login_data.password}'!"
        )

    token = create_token(user)

    return token


@app.put("/api/users/change-username")
def change_username(new_username_change_data: UsernameChangeSchema,
                    current_user=Depends(get_current_user)):
    try:
        username = current_user.username

        session = SessionLocal()
        user = session.query(User).filter_by(username=username).first()
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error while trying to get user!"
                                   f"ERR: {err}")

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username '{username}' was not found!")

    try:
        user.username = new_username_change_data.username
        session.commit()
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error while trying to change username"
                                   f"ERR: {err}")

    return ORJSONResponse(content={"message": "Username changed successfully!"},
                          headers=CORS_HEADERS)
