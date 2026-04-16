from dataclasses import dataclass

from models.enums import Condition


@dataclass
class PhoneOffer:
    brand: str
    model: str
    storage: int
    condition: Condition
    price: float
    currency: str
    source: str
    url: str
