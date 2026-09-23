# 📱 Phone Price Aggregator

A Python tool that scrapes and aggregates refurbished/used iPhone pricing from multiple resale marketplaces — **Swappie**, **Backmarket**, and **Refurbed** — and stores the results in a local database for comparison and tracking.

## How it works

The aggregator pulls listings for a set of tracked iPhone models from each provider, normalizes them into a common `PhoneOffer` format, and saves them to a local SQLite database (`phones.db`).

- **Swappie** — pulled directly from Swappie's API, returning all available offers for a given model.
- **Backmarket / Refurbed** — scraped from each phone's offer page HTML.

Each offer is normalized into a shared model, for example:

```python
PhoneOffer(
    brand='Apple',
    model='iPhone 11',
    storage=64,
    condition='C',
    price='€155',
    currency='EUR',
    source='Swappie',
    url='https://swappie.com/ie/iphone/iphone-11/iphone-11-64gb-black-3'
)
```

### Condition grading (Refurbed)

Refurbed offer URLs encode a condition grade as a suffix letter, e.g. `https://www.refurbed.ie/o/14162c/`:

| Suffix | Grade |
|--------|-------|
| `c`    | Good |
| `b`    | Very good |
| `aa`   | Premium |
| *(none)* | Excellent |

## Tracked models

The aggregator currently targets the following iPhone models (being extended to other brands):

iPhone 11, 11 Pro, 11 Pro Max, 12, 12 mini, 12 Pro, 12 Pro Max, 13, 13 mini, 13 Pro, 13 Pro Max, 14, 14 Plus, 14 Pro, 14 Pro Max, 15, 15 Plus, 15 Pro, 15 Pro Max, 16, 16e, 16 Plus, 16 Pro, 16 Pro Max, 17, 17e, 17 Pro, 17 Pro Max, iPhone Air, SE (2020), SE (2022)

## Project structure

```
.
├── main.py         # Entry point — runs the aggregator and persists results
├── aggregator.py    # Core aggregation logic, coordinates provider scrapers
├── providers/       # Per-marketplace scrapers (Swappie, Backmarket, Refurbed)
├── models.py        # PhoneOffer data model
├── db.py            # Database setup and persistence (SQLite)
├── logger.py        # Logging configuration
├── tests/           # Test suite
├── phones.db         # SQLite database of saved offers
└── pytest.ini        # Pytest configuration
```

## Getting started

### Prerequisites

- Python 3.9+

### Installation

```bash
git clone https://github.com/kacperslenzak/phone-price-aggregator.git
cd phone-price-aggregator
pip install -r requirements.txt
```

> **Note:** If a `requirements.txt` isn't present yet, install the scraping/HTTP libraries your providers rely on (e.g. `requests`, `beautifulsoup4`) manually.

### Usage

Run the aggregator:

```bash
python main.py
```

This will:
1. Initialize the local database (`phones.db`)
2. Run each provider scraper to collect current offers
3. Save all collected offers to the database
4. Log a summary of how many offers were saved

### Running tests

```bash
pytest
```

## Roadmap

- [ ] Expand model coverage to brands outside of Apples
- [ ] Add price history tracking over time
- [ ] Add a way to query/export aggregated offers (CLI or simple API)
- [ ] Add more marketplaces

## Contributing

Issues and pull requests are welcome. If you'd like to add a new marketplace provider, follow the existing pattern in `providers/` and normalize results into the `PhoneOffer` model.