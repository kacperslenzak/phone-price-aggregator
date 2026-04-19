from providers.base import BaseProvider
from providers.swappie import SwappieProvider
from providers.refurbed import RefurbedProvider

def load_providers():
    return [
        SwappieProvider(),
        RefurbedProvider()
    ]
