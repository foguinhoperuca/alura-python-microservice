from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.checkout.checkout_request import CheckoutRequest
from app.infra.database import get_db


async def checkout_process(checkout_request: CheckoutRequest, db: AsyncSession = Depends(get_db)):
    pass
