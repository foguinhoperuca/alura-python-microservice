import asyncio
from typing import Any, Dict, Self

import httpx

from app.checkout.checkout_request import PaymentMethodRequest
from app.client_manager import client_manager_factory


class PaymentClient:
    def __init__(self: Self, client: httpx.AsyncClient, max_retries: int = 3) -> None:
        self.client: httpx.AsyncClient = client
        self.max_retries: int = max_retries

    async def process(self: Self, total_amount: float, payment_method: PaymentMethodRequest, customer_email: str) -> Dict[str, Any]:
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
        last_error = None
        for attempt in range(self.max_retries):
            try:
                response = await self.client.post('payments/process', json=payload)
                response.raise_for_status()
                transaction_id = response.json()['transactionId']

                return {'transaction_id': transaction_id, 'error': None}
            except httpx.HTTPStatusError as e:
                last_error = e.response.text
                if 400 <= e.response.status_code <= 500:
                    return {'transaction_id': None, 'error': f'HTTP ERROR {e.response.status_code} force to already return in attempt {attempt} with error {last_error}'}
            except (httpx.RequestError, httpx.TimeoutException) as e:
                last_error = str(e)
            except Exception as e:
                return {'transaction_id': None, 'error': str(e)}

            if attempt < self.max_retries - 1:
                wait_time: int = 2 ** attempt
                await asyncio.sleep(wait_time)

        return {'transaction_id': None, 'error': f'Payment failed after {self.max_retries} attempts: {last_error}'}


def get_payment_client() -> PaymentClient:
    return PaymentClient(client=client_manager_factory.payment_client)
