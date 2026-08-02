from typing import Any, Dict, List, Self

import httpx

from app.checkout.checkout_request import ItemRequest
from app.client_manager import client_manager_factory


class InventoryClient:
    def __init__(self: Self, client: httpx.AsyncClient) -> None:
        self.client: httpx.AsyncClient = client

    async def deduct(self: Self, items: List[ItemRequest]) -> Dict[str, Any]:
        try:
            payload = {"items": [{'product_id': item.product_id, 'quantity': item.quantity, } for item in items]}
            response = await self.client.post('/inventory/deduct', json=payload)
            response.raise_for_status()

            return {'success': True, 'error': None}
        except httpx.HTTPStatusError as e:
            return {'success': False, 'error': e.response.text}
        except Exception as e:
            return {'success': False, 'error': str(e)}


def get_inventory_client() -> InventoryClient:
    return InventoryClient(client=client_manager_factory.inventory_client)
