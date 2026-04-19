import logging
from models.enums import Condition
from providers import BaseProvider
from bs4 import BeautifulSoup
import re
from playwright.sync_api import sync_playwright
from models import PhoneOffer


def extract_storage(tag: BeautifulSoup):
    text = tag.get_text(" ", strip=True)

    match = re.search(r"(\d+)\s?GB", text, re.I)
    return int(match.group(1)) if match else None


def extract_price_and_currency(tag: BeautifulSoup):
    text = tag.get_text(" ", strip=True)

    currency = "EUR" if "€" in text else "Unknown"

    match = re.search(r"[\d,.]+", text)
    price = float(match.group(0).replace(",", "")) if match else None

    return price, currency


def extract_condition(tag: BeautifulSoup):
    text = tag.get_text(" ", strip=True).lower()
    if "excellent" in text:
        return Condition("B")
    elif "very good" in text:
        return Condition("C")
    elif "premium" in text:
        return Condition("A")

    return Condition("C")


class RefurbedProvider(BaseProvider):
    name = "refurbed"
    BASE_URL = "https://www.refurbed.ie/p/"
    AVAILABLE_MODELS = [
        "iphone-15",
        "iphone-15-pro",
        "iphone-14",
        "iphone-13",
        "iphone-14-pro",
        "iphone-15-pro-max",
        "iphone-13-pro",
        "iphone-13-mini",
        "iphone-12",
        "iphone-16-pro",
        "iphone-14-pro-max",
        "iphone-16-pro-max",
        "iphone-12-mini",
        "iphone-13-pro-max",
        "iphone-11",
        "iphone-15-plus",
        "iphone-16",
        "iphone-12-pro",
        "iphone-se-2022",
        "iphone-14-plus",
        "iphone-12-pro-max",
        "iphone-11-pro",
        "iphone-16-plus",
        "iphone-17-pro",
        "iphone-11-pro-max",
        "iphone-16e",
        "iphone-se-2020",
        "iphone-air",
        "iphone-17",
        "iphone-17e",
        "iphone-17-pro-max"
    ]
    current_url: str
    logger = logging.getLogger('providers.refurbed')

    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch()

    def get_html_content(self, url: str) -> BeautifulSoup:
        page = self.browser.new_page()
        page.goto(url)
        html = page.content()
        page.close()
        return BeautifulSoup(html, "html.parser")

    def fetch_listings(self, model):
        self.current_url = self.BASE_URL + model
        soup = self.get_html_content(self.current_url)
        return self.normalize(soup)

    def normalize(self, phone_offer: BeautifulSoup) -> PhoneOffer:
        details = phone_offer.find(attrs={'data-test': 'product-basic-details'})
        model = phone_offer.find(attrs={'data-test': 'product-name'}).get_text(strip=True)
        storage = extract_storage(details)
        price, currency = extract_price_and_currency(phone_offer.find(attrs={"data-test": "product-price"}))
        condition = extract_condition(details)

        return PhoneOffer(
            brand="Apple",
            model=model,
            storage=storage,
            condition=condition,
            price=price,
            currency=currency,
            source="Refurbed",
            url=self.current_url
        )
