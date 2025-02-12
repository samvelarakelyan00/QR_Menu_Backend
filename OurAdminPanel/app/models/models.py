from sqlalchemy import Column, String, Integer, Float, Time, ForeignKey, TIMESTAMP, text

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class OurAdmin(Base):
    __tablename__ = "ouradmins"

    id = Column(Integer, nullable=False, primary_key=True)

    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))


class HoReKaClient(Base):
    __tablename__ = "horekaclients"

    id = Column(Integer, nullable=False, primary_key=True)

    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))


class HoReKaAdmin(Base):
    __tablename__ = "horekadmin"

    id = Column(Integer, nullable=False, primary_key=True)

    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))

    horekaclient_id = Column(Integer, ForeignKey("horekaclients.id"))


class HoReKaMenu(Base):
    __tablename__ = "horekamenu"

    id = Column(Integer, nullable=False, primary_key=True)

    kind = Column(String, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    image_src = Column(String, nullable=True)

    preparation_time = Column(Time, nullable=True)
    weight = Column(Float, nullable=True)
    calories = Column(Float, nullable=True)

    created_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))

    horekaclient_id = Column(Integer, ForeignKey("horekaclients.id"))
