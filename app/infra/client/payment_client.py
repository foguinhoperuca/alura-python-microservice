from typing import Any, Dict, Self

import httpx

from app.checkout.checkout_request import PaymentMethodRequest
from app.client_manager import client_manager_factory


class PaymentClient:
    def __init__(self: Self, client: httpx.AsyncClient) -> None:
        self.client = client

    async def process(self: Self, total_amount: float, payment_method: PaymentMethodRequest, customer_email: str) -> Dict[str, Any]:
        try:
            payload = {
                'amount': total_amount,
                'payment_method': {
                    'type': payment_method.type,
                    'card_number': payment_method.card_number,
                    'card_expiry': payment_method.card_expiry,
                    'card_cvv': payment_method.card_cvv,
                },
                'customer_email': customer_email
            }
            response = await self.client.post('payments/process', json=payload)
            response.raise_for_status()
            transaction_id = response.json()['transactionId']

            return {'transaction_id': transaction_id, 'error': None}
        except httpx.HTTPStatusError as e:
            return {'transaction_id': None, 'error': e.response.text}
        except Exception as e:
            return {'transaction_id': None, 'error': str(e)}


def get_payment_client() -> PaymentClient:
    return PaymentClient(client=client_manager_factory.payment_client)
