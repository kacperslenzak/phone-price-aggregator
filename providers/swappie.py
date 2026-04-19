import logging
import re
from models.enums import Condition
from providers import BaseProvider
from models import PhoneOffer
import requests
from typing import List


def parse_model_name_to_slug(model_name):
    return model_name.lower().replace(" ", "-")


def clean_price(raw: str):
    cleaned = re.sub(r"[^\d.]", "", raw)
    return float(cleaned)


class SwappieProvider(BaseProvider):
    name = "swappie"
    BASE_URL = "https://swappie.com/api/model/ie/"
    AVAILABLE_MODELS = [
        'iPhone%2011',
        'iPhone%2011%20Pro',
        'iPhone%2011%20Pro%20Max',
        'iPhone%2012',
        'iPhone%2012%20mini',
        'iPhone%2012%20Pro',
        'iPhone%2012%20Pro%20Max',
        'iPhone%2013',
        'iPhone%2013%20mini',
        'iPhone%2013%20Pro',
        'iPhone%2013%20Pro%20Max',
        'iPhone%2014',
        'iPhone%2014%20Plus',
        'iPhone%2014%20Pro',
        'iPhone%2014%20Pro%20Max',
        'iPhone%2015',
        'iPhone%2015%20Plus',
        'iPhone%2015%20Pro',
        'iPhone%2015%20Pro%20Max',
        'iPhone%2016',
        'iPhone%2016%20Plus',
        'iPhone%2016%20Pro',
        'iPhone%2016%20Pro%20Max',
        'iPhone%2016e',
        'iPhone%2017',
        'iPhone%2017e',
        'iPhone%2017%20Pro',
        'iPhone%2017%20Pro%20Max',
        'iPhone%20SE%202020',
        'iPhone%20SE%202022',
        'iPhone%20Air'
    ]
    logger = logging.getLogger('providers.swappie')

    def fetch_listings(self, model):
        phone_offers: List[PhoneOffer] = []
        phone_api_request = requests.get(self.BASE_URL + model).json()
        for phone in phone_api_request['availablePhones']:
            phone_offers.append(self.normalize(phone))

        return phone_offers

    def normalize(self, phone_offer: dict):
        return PhoneOffer(
            brand="Apple",
            model=phone_offer['modelName'],
            storage=phone_offer['storage'],
            condition=Condition(phone_offer['grade']),
            price=float(clean_price(phone_offer['price'])),
            currency=phone_offer['normalPrice']['currency'],
            source="Swappie",
            url=f"https://swappie.com/ie/iphone/{parse_model_name_to_slug(phone_offer['modelName'])}/{phone_offer['slug']}"
        )
