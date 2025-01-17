from sqlalchemy import Column, String, Integer

from ..database import Base


class Test(Base):
    __tablename__ = "test"

    id = Column(Integer, nullable=False, primary_key=True)