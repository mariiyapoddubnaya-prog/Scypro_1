from smartphone import Smartphone

catalog = [
    Smartphone("Apple", "iPhone 14", "+79001112233"),
    Smartphone("Samsung", "Galaxy S23", "+79004445566"),
    Smartphone("Xiaomi", "Redmi Note 12", "+79007778899"),
    Smartphone("Google", "Pixel 7", "+79001234567"),
    Smartphone("OnePlus", "11", "+79009876543"),
]

for phone in catalog:
    print(f"{phone.brand} - {phone.model}. {phone.phone_number}")
