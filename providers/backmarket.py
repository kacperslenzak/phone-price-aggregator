import logging
import re
from typing import List, Optional
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from models import PhoneOffer
from models.enums import Condition
from providers import BaseProvider
from utils import generate_id


class BackMarketProvider(BaseProvider):
    name = "backmarket"
    BASE_URL = "https://www.backmarket.ie/en-ie/p/"
    AVAILABLE_MODELS = [
        "iphone-11",
        "iphone-11-pro",
        "iphone-11-pro-max",
        "iphone-12",
        "iphone-12-mini",
        "iphone-12-pro",
        "iphone-12-pro-max",
        "iphone-13",
        "iphone-13-mini",
        "iphone-13-pro",
        "iphone-13-pro-max",
        "iphone-14",
        "iphone-14-plus",
        "iphone-14-pro",
        "iphone-14-pro-max",
        "iphone-15",
        "iphone-15-plus",
        "iphone-15-pro",
        "iphone-15-pro-max",
        "iphone-16",
        "iphone-16-plus",
        "iphone-16-pro",
        "iphone-16-pro-max",
        "iphone-16e",
        "iphone-17",
        "iphone-17e",
        "iphone-17-pro",
        "iphone-17-pro-max",
        "iphone-se-2020",
        "iphone-se-2022",
        "iphone-air",
    ]
    logger = logging.getLogger("providers.backmarket")

    def _ensure_browser(self):
        if not hasattr(self, "_playwright"):
            self._playwright = sync_playwright().start()
            self._browser = self._playwright.chromium.launch(
                args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
            )

    @property
    def browser(self):
        self._ensure_browser()
        return self._browser

    def get_page_data(self, url: str) -> Optional[dict]:
        self._ensure_browser()
        context = self.browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1920, "height": 1080},
            locale="en-IE",
        )
        page = context.new_page()
        page.add_init_script(
            'Object.defineProperty(navigator, "webdriver", {get: () => undefined});'
        )
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            body_text = page.evaluate("document.body.innerText")
            title = page.title()
            page.close()
            context.close()
            return {"title": title, "body_text": body_text}
        except Exception as e:
            self.logger.warning("Failed to load %s: %s", url, e)
            page.close()
            context.close()
            return None

    def fetch_listings(self, model):
        url = self.BASE_URL + model
        data = self.get_page_data(url)
        if data is None:
            return []
        return self.normalize(data, url)

    def normalize(self, data: dict, url: str) -> List[PhoneOffer]:
        offers = []
        body_text = data["body_text"]
        title = data["title"]

        model_name = title.replace("Refurbished | Back Market", "").strip()
        if not model_name:
            model_name = "Unknown"

        storage = self._extract_storage(body_text)
        condition_prices = self._extract_condition_prices(body_text)

        if condition_prices:
            for cond, price in condition_prices.items():
                offers.append(
                    PhoneOffer(
                        id=generate_id("BackMarket", f"{url}-{cond.value}"),
                        brand="Apple",
                        model=model_name,
                        storage=storage,
                        condition=cond,
                        price=price,
                        currency="EUR",
                        source="BackMarket",
                        url=url,
                    )
                )

        if not offers:
            default_price = self._extract_default_price(body_text)
            if default_price:
                offers.append(
                    PhoneOffer(
                        id=generate_id("BackMarket", url),
                        brand="Apple",
                        model=model_name,
                        storage=storage,
                        condition=Condition.C,
                        price=default_price,
                        currency="EUR",
                        source="BackMarket",
                        url=url,
                    )
                )

        if not offers:
            self.logger.warning("No offers extracted from %s", url)

        return offers

    def _extract_condition_prices(self, body_text: str) -> dict:
        result = {}
        cond_price_pat = re.compile(
            r"(Fair|Good|Excellent|Premium)\s{1,10}€\s*([\d,.]+)", re.I
        )
        for match in cond_price_pat.finditer(body_text):
            label = match.group(1).lower()
            try:
                price = float(match.group(2).replace(",", ""))
            except ValueError:
                continue
            if label == "fair":
                cond = Condition.D
            elif label == "good":
                cond = Condition.C
            elif label == "excellent":
                cond = Condition.B
            elif label == "premium":
                cond = Condition.A
            else:
                continue
            if cond not in result or price < result[cond]:
                result[cond] = price

        return result

    def _extract_storage(self, body_text: str) -> int:
        match = re.search(r"\b(\d+)\s*(?:GB)\b", body_text, re.I)
        return int(match.group(1)) if match else 0

    def _extract_default_price(self, body_text: str) -> Optional[float]:
        match = re.search(r"€\s*([\d,.]+)", body_text)
        if match:
            try:
                return float(match.group(1).replace(",", ""))
            except ValueError:
                pass
        return None
