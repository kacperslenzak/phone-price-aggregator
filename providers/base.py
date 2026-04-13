from abc import ABC, abstractmethod


class BaseProvider(ABC):
    name = "base"

    @abstractmethod
    def fetch_listings(self):
        """Return listings"""
        pass

    @abstractmethod
    def normalize(self, phone_offer):
        """Normalize data into structured listing"""
        pass
