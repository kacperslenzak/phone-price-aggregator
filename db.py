import sqlite3
from models import PhoneOffer

conn = sqlite3.connect('phones.db')


def init_db():
    with conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS offers (
            id TEXT PRIMARY KEY,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            storage INTEGER NOT NULL,
            condition TEXT NOT NULL,
            price INTEGER NOT NULL,
            currency TEXT NOT NULL,
            source TEXT NOT NULL,
            url TEXT NOT NULL,
            last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )""")


def save_offer(offer: PhoneOffer):
    with conn:
        conn.execute("""
        INSERT INTO offers (
            id, brand, model, storage, condition,
            price, currency, source, url, last_updated
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        ON CONFLICT(id) DO UPDATE SET
            brand = excluded.brand,
            model = excluded.model,
            storage = excluded.storage,
            condition = excluded.condition,
            price = excluded.price,
            currency = excluded.currency,
            source = excluded.source,
            url = excluded.url,
            last_updated = datetime('now')
        """, (
            offer.id,
            offer.brand,
            offer.model,
            offer.storage,
            offer.condition,
            offer.price,
            offer.currency,
            offer.source,
            offer.url
        ))
