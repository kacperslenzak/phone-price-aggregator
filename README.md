# Phone price aggregator

What phones we will scrape for now
- [ ] iPhone 15
- [ ] iPhone 15 Pro
- [ ] iPhone 14
- [ ] iPhone 13
- [ ] iPhone 14 Pro
- [ ] iPhone 15 Pro Max
- [ ] iPhone 13 Pro
- [ ] iPhone 13 mini
- [ ] iPhone 12
- [ ] iPhone 16 Pro
- [ ] iPhone 14 Pro Max
- [ ] iPhone 16 Pro Max
- [ ] iPhone 12 mini
- [ ] iPhone 13 Pro Max
- [ ] iPhone 11
- [ ] iPhone 15 Plus
- [ ] iPhone 16
- [ ] iPhone 12 Pro
- [ ] iPhone SE 2022
- [ ] iPhone 14 Plus
- [ ] iPhone 12 Pro Max
- [ ] iPhone 11 Pro
- [ ] iPhone 16 Plus
- [ ] iPhone 17 Pro
- [ ] iPhone 11 Pro Max
- [ ] iPhone 16e
- [ ] iPhone SE 2020
- [ ] iPhone Air
- [ ] iPhone 17
- [ ] iPhone 17e
- [ ] iPhone 17 Pro Max

Swappie
- Info directly from api
- Pulls all available offers from a model
- Example of PhoneOffer object returned from swappie api
  - `PhoneOffer(brand='Apple', model='iPhone 11', storage=64, condition='C', price='€155', currency='EUR', source='Swappie', url='https://swappie.com/ie/iphone/iphone-11/iphone-11-64gb-black-3')`

Backmarket
- Scrape html from offers page of dedicated phone
- Example offer url `https://www.refurbed.ie/o/14162c/`
    - Suffix letter indicated grade e.g `c = good, aa = premium, none = excellent, b = very good`
