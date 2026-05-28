from providers.base import BaseProvider
from providers.swappie import SwappieProvider
from providers.refurbed import RefurbedProvider
from providers.backmarket import BackMarketProvider


def load_providers():
    return [
        SwappieProvider(),
        RefurbedProvider(),
        BackMarketProvider()
    ]
