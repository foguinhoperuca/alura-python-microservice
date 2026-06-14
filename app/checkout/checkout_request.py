from pydantic import BaseModel


class PaymentMethodRequest(BaseModel):
    pay_type: str             # FIXME original code was type only - classh with reserved word
    card_number: str
    card_expiry: str
    card_cvv: str


class ShippingAddressRequest(BaseModel):
    street: str
    number: str
    city: str
    state: str
    zip_code: str


class ItemRequest(BaseModel):
    prodcut_id: str
    quantity: int
    price: float


class CheckoutRequest(BaseModel):
    payment_method: PaymentMethodRequest
    shipping_address: ShippingAddressRequest
    items: ItemRequest
    customer_email: str
