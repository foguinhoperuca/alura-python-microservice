import os
from typing import Optional, Self

import httpx


class ClientManager:
    DEFAULT_TIMEOUT_PAYMENT: float = 10.0
    DEFAULT_TIMEOUT_INVENTORY: float = 30.0
    DEFAULT_TIMEOUT_ORDER: float = 15.0

    def __init__(self: Self) -> None:
        self._payment_client: Optional[httpx.AsyncClient] = None
        self._inventory_client: Optional[httpx.AsyncClient] = None
        self._order_client: Optional[httpx.AsyncClient] = None

    @property
    def payment_client(self: Self) -> httpx.AsyncClient:
        if not self._payment_client:
            raise RuntimeError('Payment client *NOT* initialized!!')

        return self._payment_client

    @property
    def inventory_client(self: Self) -> httpx.AsyncClient:
        if not self._inventory_client:
            raise RuntimeError('Inventory client *NOT* initialized!!')

        return self._inventory_client

    @property
    def order_client(self: Self) -> httpx.AsyncClient:
        if not self._order_client:
            raise RuntimeError('Order client *NOT* initialized!!')

        return self._order_client

    async def startup(self: Self) -> None:
        payment_service_url: str = os.getenv('URL_SERVICE_PAYMENT')
        inventory_service_url: str = os.getenv('URL_SERVICE_INVENTORY')
        order_service_url: str = os.getenv('URL_SERVICE_ORDER')
        timeout_payment: float = float(os.getenv('TIMEOUT_PAYMENT', ClientManager.DEFAULT_TIMEOUT_PAYMENT))
        timeout_inventory: float = float(os.getenv('TIMEOUT_INVENTORY', ClientManager.DEFAULT_TIMEOUT_INVENTORY))
        timeout_order: float = float(os.getenv('TIMEOUT_ORDER', ClientManager.DEFAULT_TIMEOUT_ORDER))

        self._payment_client = httpx.AsyncClient(base_url=payment_service_url, timeout=timeout_payment)
        self._inventory_client = httpx.AsyncClient(base_url=inventory_service_url, timeout=timeout_inventory)
        self._order_client = httpx.AsyncClient(base_url=order_service_url, timeout=timeout_order)

    async def shutdown(self: Self) -> None:
        if self._payment_client:
            await self._payment_client.aclose()

        if self._inventory_client:
            await self._inventory_client.aclose()

        if self._order_client:
            await self._order_client.aclose()


client_manager_factory: ClientManager = ClientManager()
