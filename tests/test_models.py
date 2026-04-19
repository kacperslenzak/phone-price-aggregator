from models.enums import Condition
from models.models import PhoneOffer


def test_phone_offer_dataclass():
    offer = PhoneOffer(
        brand="Apple",
        model="iPhone 15",
        storage=128,
        condition=Condition.B,
        price=799.99,
        currency="EUR",
        source="Test",
        url="https://example.com",
    )

    assert offer.brand == "Apple"
    assert offer.condition == Condition.B
