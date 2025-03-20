from sqlalchemy import Column, String, Integer, Float, ForeignKey, TIMESTAMP, text, func

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
    image_src = Column(String, nullable=True)
    logo = Column(String, nullable=True)
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
    category = Column(String, nullable=False)
    name = Column(String, nullable=False)
    quantity = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    image_src = Column(String, nullable=False)
    language = Column(String, nullable=False)

    preparation_time = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    calories = Column(Float, nullable=True)

    created_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))

    horekaclient_id = Column(Integer, ForeignKey("horekaclients.id"))


class UserFeedback(Base):
    __tablename__ = "user_feedbacks"

    id = Column(Integer, primary_key=True)
    rating = Column(Integer, nullable=False)
    feedback_text = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))

    horeka_client_id = Column(Integer, ForeignKey("horekaclients.id"))


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, unique=True, index=True)  # Bill number from merchant
    amount = Column(Float)
    status = Column(String)  # Payment status (e.g., "pending", "paid", "failed", etc.)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now() + text("Interval '4 hours'"))
    updated_at = Column(TIMESTAMP, nullable=False, default=func.now() + text("Interval '4 hours'"),
                        onupdate=func.now() + text("Interval '4 hours'"))
    available_to = Column(TIMESTAMP, nullable=False, default=func.now()
                                                             + text("Interval '4 hours'")
                                                             + text("Interval '31 days'"))

    # Foreign key to associate payment with a user
    horeka_client_id = Column(Integer, ForeignKey('horekaclients.id'))

    # Fields for tracking Idram-specific payment information
    payer_account = Column(String, nullable=True)  # Idram ID of the payer
    trans_id = Column(String, nullable=True)  # Transaction ID from Idram
    trans_date = Column(String, nullable=True)  # Transaction date from Idram

    subs_plan = Column(String, nullable=False)


class QRScanInfo(Base):
    __tablename__ = "qr_scan_info"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))
    horeka_client_id = Column(Integer, ForeignKey("horekaclients.id"))
