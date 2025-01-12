from sqlalchemy import Column, String, Integer

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, nullable=False, primary_key=True)

    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
