from passlib.hash import bcrypt


def hash_password(plain_password: str) -> str:
    return bcrypt.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.verify(plain_password, hashed_password)
