from models.enums import Condition
from models.models import PhoneOffer
from aggregator import Aggregator
import main


class DummySingleOfferProvider:
    name = "dummy-single"
    AVAILABLE_MODELS = ["model-a", "model-b"]

    def fetch_listings(self, model):
        return PhoneOffer(
            brand="Apple",
            model=model,
            storage=64,
            condition=Condition.C,
            price=100.0,
            currency="EUR",
            source="Dummy",
            url=f"https://example.com/{model}",
        )


class DummyMultiOfferProvider:
    name = "dummy-multi"
    AVAILABLE_MODELS = ["model-c"]

    def fetch_listings(self, model):
        return [
            PhoneOffer(
                brand="Apple",
                model=f"{model}-1",
                storage=128,
                condition=Condition.B,
                price=200.0,
                currency="EUR",
                source="Dummy",
                url=f"https://example.com/{model}-1",
            ),
            PhoneOffer(
                brand="Apple",
                model=f"{model}-2",
                storage=256,
                condition=Condition.A,
                price=300.0,
                currency="EUR",
                source="Dummy",
                url=f"https://example.com/{model}-2",
            ),
        ]


class DummyFailingProvider:
    name = "dummy-failing"
    AVAILABLE_MODELS = ["broken-model"]

    def fetch_listings(self, model):
        raise RuntimeError("boom")


def test_aggregator_collects_single_and_multiple_offers(monkeypatch):
    monkeypatch.setattr(
        Aggregator,
        "providers",
        [DummySingleOfferProvider(), DummyMultiOfferProvider()],
        raising=False,
    )

    aggregator = Aggregator()
    aggregator.phone_offers = []
    aggregator.run_aggregator()

    assert len(aggregator.phone_offers) == 4
    assert aggregator.phone_offers[0].model == "model-a"
    assert aggregator.phone_offers[1].model == "model-b"
    assert aggregator.phone_offers[2].model == "model-c-1"
    assert aggregator.phone_offers[3].model == "model-c-2"


def test_aggregator_skips_failing_provider(monkeypatch):
    monkeypatch.setattr(
        Aggregator,
        "providers",
        [DummyFailingProvider()],
        raising=False,
    )

    aggregator = Aggregator()
    aggregator.phone_offers = []
    aggregator.run_aggregator()

    assert aggregator.phone_offers == []


def test_save_offers_calls_save_offer_for_each_offer(monkeypatch):
    calls = []

    def fake_save_offer(offer):
        calls.append(offer)

    monkeypatch.setattr(main, "save_offer", fake_save_offer)

    offers = [
        PhoneOffer("Apple", "iPhone 11", 64, Condition.C, 155.0, "EUR", "Swappie", "u1"),
        PhoneOffer("Apple", "iPhone 12", 128, Condition.B, 255.0, "EUR", "Refurbed", "u2"),
    ]

    main.save_offers(offers)

    assert len(calls) == 2
    assert calls[0].model == "iPhone 11"
    assert calls[1].model == "iPhone 12"


def test_main_runs_without_real_db_or_network(monkeypatch):
    events = []

    monkeypatch.setattr(main, "setup_logging", lambda: events.append("logging"))
    monkeypatch.setattr(main, "init_db", lambda: events.append("db"))

    class DummyAggregator:
        def __init__(self):
            self.phone_offers = [
                PhoneOffer("Apple", "iPhone 11", 64, Condition.C, 155.0, "EUR", "Swappie", "u1")
            ]

        def run_aggregator(self):
            events.append("aggregator")

    monkeypatch.setattr(main, "Aggregator", DummyAggregator)
    monkeypatch.setattr(main, "save_offers", lambda offers: events.append(f"saved:{len(offers)}"))

    main.main()

    assert events == ["logging", "db", "aggregator", "saved:1"]
