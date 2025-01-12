from fastapi import FastAPI, HTTPException, status


from models import Base, User
from database import engine, SessionLocal
from schemas import (
    UserSignupSchema,
    UserLoginSchema
)


Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/")
def main():
    return {"message": "This is the main page!!!"}


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

    return {"message": "User successfully signup!"}


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

    return {"Message": "User successfully logged in!"}  # TODO return token


@app.put("/api/users/change-username")  # TODO change username with token
def change_username():
    pass
