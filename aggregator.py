from typing import List
from models import PhoneOffer
from providers import load_providers
import logging


class Aggregator:
    providers = load_providers()
    phone_offers: List[PhoneOffer] = []
    logger = logging.getLogger('aggregator')

    def run_aggregator(self):
        for provider in self.providers:
            for model in provider.AVAILABLE_MODELS:
                count = 0
                try:
                    self.logger.info(f"[{provider.name}]: fetching {model}")
                    offer = provider.fetch_listings(model)
                    if isinstance(offer, List):
                        self.phone_offers.extend(offer)
                    else:
                        self.phone_offers.append(offer)
                    count += 1
                    self.logger.info(f"[{provider.name}] -> [iteration: {count}]: appended {model}")
                except Exception as e:
                    self.logger.exception(f"[{provider.name}]: failed to fetch {model} -> {e}")
