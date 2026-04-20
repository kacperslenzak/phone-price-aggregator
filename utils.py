import hashlib

from models import PhoneOffer


def generate_id(source, url):
    key = f"{source}|{url}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()
