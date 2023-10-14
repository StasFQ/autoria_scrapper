import requests
import re
from bs4 import BeautifulSoup


from db.models import session
from script.tasks import create_car_credential
from utils.celery_config import app


def parse_car_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    car_name = soup.find('h1', class_='head')
    price = soup.select_one('#showLeftBarView > section.price.mb-15.mhide > div.price_value > strong')
    mileage = soup.select_one('#showLeftBarView > section.price.mb-15.mhide > div.base-information.bold > span')
    seller_name = soup.select_one('#userInfoBlock > div.seller_info.mb-15 > div > div.seller_info_name.bold')
    photos_count = soup.select_one('#photosBlock > div.preview-gallery.mhide > div.action_disp_all_block > a')
    photos_count_result = None
    if photos_count:
        photos_count_result = re.search(r'\d+', str(photos_count.text))
    car_vin = soup.find('div', class_='t-check').text
    div_element = soup.find('div', class_='gallery-order carousel')
    image_src = None
    if div_element:
        image_src = div_element.find('img').get('src')
    car_number = soup.find('div', class_='t-check').find('span', class_='state-num ua', recursive=False)
    car_credentials = create_car_credential(url, car_name, price, mileage, seller_name,  int(photos_count_result.group()), car_number, car_vin,
                                            image_url=image_src)
    try:
        session.add(car_credentials)
        session.commit()
        print("Дані успішно збережено в базі даних")
    except Exception as e:
        session.rollback()
        print(f"Помилка при збереженні в базі даних: {e}")
    finally:
        session.close()


@app.task
def parser():
    base_url = 'https://auto.ria.com/car/used/'
    suffix = ''
    url = base_url

    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        elements = soup.find_all('div', class_='ticket-title')

        for element in elements:
            link = element.find('a', class_='address').get('href')
            print("Посилання:", link)
            parse_car_page(link)

        next_button = soup.select_one('#pagination > nav > span.page-item.next.text-r > a')
        if next_button:
            next_page_url = next_button.get('href')
            print('Посилання на наступну сторінку:', next_page_url)
        if not next_page_url:
            break
        url = next_page_url
