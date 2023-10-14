import requests
from bs4 import BeautifulSoup

from db.models import CarCredential


def create_car_credential(url, title, price_usd, odometer, username, images_count, car_number, car_vin, image_url=None):
    return CarCredential(
        url=url,
        title=title.text.strip() if title else None,
        price_usd=int(price_usd.text.replace('$', '').replace('€', '').replace(' ', '').strip()) if price_usd else None,
        odometer=int(odometer.text.strip()) if odometer else None,
        username=username.text.strip() if username else None,
        phone_number=None,
        image_url=image_url if image_url else None,
        images_count=images_count,
        car_number=car_number.text.strip() if car_number else None,
        car_vin=car_vin if car_vin else None
    )
