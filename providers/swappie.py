from providers import BaseProvider
from models import PhoneOffer
import requests


def parse_model_name_to_slug(model_name):
    return model_name.lower().replace(" ", "-")


class SwappieProvider(BaseProvider):
    name = "swappie"
    BASE_URL = "https://swappie.com/api/model/ie/"
    AVAILABLE_MODELS = ['iPhone%2011', 'iPhone%2012', 'iPhone%2013', 'iPhone%2014', 'iPhone%2015', 'iPhone%2016', 'iPhone%2017']

    def fetch_listings(self):
        phones = []
        phone_api_request = requests.get(self.BASE_URL + self.AVAILABLE_MODELS[0]).json()
        for phone in phone_api_request['availablePhones']:
            phone_offer = self.normalize(phone)
            phones.append(phone_offer)
        print(phones)

    def normalize(self, phone_offer: dict):
        return PhoneOffer(
            brand="Apple",
            model=phone_offer['modelName'],
            storage=phone_offer['storage'],
            condition=phone_offer['grade'],
            price=phone_offer['price'],
            currency=phone_offer['normalPrice']['currency'],
            source="Swappie",
            url=f"https://swappie.com/ie/iphone/{parse_model_name_to_slug(phone_offer['modelName'])}/{phone_offer['slug']}"
        )


if __name__ == '__main__':
    provider = SwappieProvider()
    provider.fetch_listings()
