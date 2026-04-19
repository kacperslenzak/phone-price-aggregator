import pytest
from bs4 import BeautifulSoup

from models.enums import Condition
from models.models import PhoneOffer
from providers.swappie import (
    parse_model_name_to_slug,
    clean_price,
    SwappieProvider,
)
from providers.refurbed import (
    extract_storage,
    extract_price_and_currency,
    extract_condition,
    RefurbedProvider,
)


def test_parse_model_name_to_slug():
    assert parse_model_name_to_slug("iPhone 15 Pro Max") == "iphone-15-pro-max"
    assert parse_model_name_to_slug("iPhone SE 2022") == "iphone-se-2022"


def test_clean_price():
    assert clean_price("€155") == 155.0
    assert clean_price("€1,299.99") == 1299.99
    assert clean_price("155.00 EUR") == 155.0


def test_swappie_normalize():
    provider = SwappieProvider.__new__(SwappieProvider)

    phone_offer = {
        "modelName": "iPhone 11",
        "storage": 64,
        "grade": "C",
        "price": "€155",
        "normalPrice": {"currency": "EUR"},
        "slug": "iphone-11-64gb-black-3",
    }

    result = provider.normalize(phone_offer)

    assert isinstance(result, PhoneOffer)
    assert result.brand == "Apple"
    assert result.model == "iPhone 11"
    assert result.storage == 64
    assert result.condition == Condition.C
    assert result.price == 155.0
    assert result.currency == "EUR"
    assert result.source == "Swappie"
    assert result.url == "https://swappie.com/ie/iphone/iphone-11/iphone-11-64gb-black-3"


def test_swappie_fetch_listings(monkeypatch):
    provider = SwappieProvider.__new__(SwappieProvider)

    response_payload = {
        "availablePhones": [
            {
                "modelName": "iPhone 11",
                "storage": 64,
                "grade": "C",
                "price": "€155",
                "normalPrice": {"currency": "EUR"},
                "slug": "iphone-11-64gb-black-3",
            },
            {
                "modelName": "iPhone 12",
                "storage": 128,
                "grade": "B",
                "price": "€255",
                "normalPrice": {"currency": "EUR"},
                "slug": "iphone-12-128gb-white-1",
            },
        ]
    }

    class DummyResponse:
        def json(self):
            return response_payload

    monkeypatch.setattr("providers.swappie.requests.get", lambda url: DummyResponse())

    def fake_normalize(phone_offer):
        return PhoneOffer(
            brand="Apple",
            model=phone_offer["modelName"],
            storage=phone_offer["storage"],
            condition=Condition(phone_offer["grade"]),
            price=float(phone_offer["price"].replace("€", "")),
            currency=phone_offer["normalPrice"]["currency"],
            source="Swappie",
            url=phone_offer["slug"],
        )

    monkeypatch.setattr(provider, "normalize", fake_normalize)

    result = provider.fetch_listings("iPhone%2011")

    assert len(result) == 2
    assert result[0].model == "iPhone 11"
    assert result[1].model == "iPhone 12"


def test_extract_storage():
    soup = BeautifulSoup("<div data-test='product-basic-details'>128 GB • Very Good</div>", "html.parser")
    tag = soup.find(attrs={"data-test": "product-basic-details"})

    assert extract_storage(tag) == 128


def test_extract_price_and_currency():
    soup = BeautifulSoup("<div data-test='product-price'>€399.99</div>", "html.parser")
    tag = soup.find(attrs={"data-test": "product-price"})

    price, currency = extract_price_and_currency(tag)

    assert price == 399.99
    assert currency == "EUR"


@pytest.mark.parametrize(
    "html,expected",
    [
        ("<div data-test='product-basic-details'>Excellent condition</div>", Condition.B),
        ("<div data-test='product-basic-details'>Very good condition</div>", Condition.C),
        ("<div data-test='product-basic-details'>Premium condition</div>", Condition.A),
        ("<div data-test='product-basic-details'>Unknown condition</div>", Condition.C),
    ],
)
def test_extract_condition(html, expected):
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find(attrs={"data-test": "product-basic-details"})

    assert extract_condition(tag) == expected


def test_refurbed_normalize():
    provider = RefurbedProvider.__new__(RefurbedProvider)
    provider.current_url = "https://www.refurbed.ie/p/iphone-15"

    html = """
    <div>
        <div data-test="product-name">iPhone 15</div>
        <div data-test="product-basic-details">128 GB Excellent</div>
        <div data-test="product-price">€799.99</div>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")

    result = provider.normalize(soup)

    assert isinstance(result, PhoneOffer)
    assert result.brand == "Apple"
    assert result.model == "iPhone 15"
    assert result.storage == 128
    assert result.condition == Condition.B
    assert result.price == 799.99
    assert result.currency == "EUR"
    assert result.source == "Refurbed"
    assert result.url == "https://www.refurbed.ie/p/iphone-15"
