from dataclasses import dataclass


@dataclass
class PhoneOffer:
    brand: str
    model: str
    storage: int
    condition: str
    price: float
    currency: str
    source: str
    url: str
