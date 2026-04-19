import logging
from typing import List
from logger import setup_logging
from aggregator import Aggregator
from db import init_db, save_offer
from models import PhoneOffer

logger = logging.getLogger('main')


def save_offers(offers: List[PhoneOffer]):
    for offer in offers:
        try:
            save_offer(offer)
        except Exception as e:
            logger.exception(e)


def main():
    """This function runs the aggregator service"""
    setup_logging()

    logger.info("Setting up database")
    init_db()

    logger.info("Setting up aggregator")
    aggregator = Aggregator()
    aggregator.run_aggregator()

    logger.info("Attempting to save offers")
    save_offers(aggregator.phone_offers)

    logger.info(f"Saved {len(aggregator.phone_offers)} offers")


if __name__ == "__main__":
    main()
