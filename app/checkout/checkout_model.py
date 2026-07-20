from datetime import datetime
from enum import auto, Enum

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.infra.database import Base


class CheckoutStatus(Enum):
    PENDING = auto()
    PROCESS_PAYMENT = auto()
    PROCESS_INVENTORY = auto()
    CREATING_ORDER = auto()
    SUCCESS = auto()
    FAILED = auto()


class CheckoutModel(Base):
    __tablename__ = 'checkouts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    payment_id = Column(String(64), nullable=True)
    order_id = Column(String(64), nullable=True)
    customer_email = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.timezone.utc, nullable=False)
    updated_at = Column(DateTime, default=datetime.timezone.utc, nullable=True)
    status = Column(String(24), default=CheckoutStatus.PENDING.value, nullable=False)
    error = Column(String, nullable=True)
    total_amount = Column(Float, nullable=False)
