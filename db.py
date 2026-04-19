import sqlite3

from models import PhoneOffer

conn = sqlite3.connect('phones.db')


def init_db():
    with conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS offers (
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            storage INTEGER NOT NULL,
            condition TEXT NOT NULL,
            price INTEGER NOT NULL,
            currency TEXT NOT NULL,
            source TEXT NOT NULL,
            url TEXT PRIMARY KEY NOT NULL,
            last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )""")


def save_offer(offer: PhoneOffer):
    with conn:
        conn.execute("""
        INSERT OR REPLACE INTO offers (brand, model, storage, condition, price, currency, source, url) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (offer.brand, offer.model, offer.storage, offer.condition,
              offer.price, offer.currency, offer.source, offer.url))
