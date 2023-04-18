import time
import requests
from bs4 import BeautifulSoup

city = 'tyumen'
domain = f'https://{city}.drom.ru/auto'
start_url = f'{domain}/all/?maxprice=500000&pts=2&w=2&unsold=1'


class Car:
    def __init__(self, **kwargs):
        self.characters = kwargs

    def print_car(self):
        for item, value in self.characters.items():
            print(f"{item}: {value}")
        print('_______________________________________________________________________________________\n')

    def get_characters(self):
        return self.characters


def get_div_list(url):
    get_html = requests.get(url)
    soup = BeautifulSoup(get_html.content, "lxml")
    div_list = soup.find('div', class_='css-1nvf6xk eojktn00').find_all('a', class_='css-xb5nz8 e1huvdhj1')
    return div_list


def get_car(div):
    try:
        # Ищем нужные нам параметры автомобиля
        link = div['href']
        car_id = link.split('/')[-1]
        name, year = div.find('div', class_="css-l1wt7n e3f4v4l2").find('span').text.split(', ')

        characters = div.find("div", class_="css-1fe6w6s e162wx9x0").find_all('span', class_='css-1l9tp44 e162wx9x0')
        lst = []
        for items in characters:
            lst.append(items.text.replace(',', ''))
        # engine = characters[0].text.replace(',', '')
        # fuel = characters[1].text.replace(',', '')
        # transmission = characters[2].text.replace(',', '')
        # wheel_drive = characters[3].text.replace(',', '')
        # run = characters[4].text.replace(',', '')

        price = div.find('span', class_='css-46itwz e162wx9x0').text
        price_grade = div.find('div', class_='css-11m58oj evjskuu0').text

        car = Car(
            link=link,
            car_id=car_id,
            name=name,
            year=year,
            characters=' | '.join(lst),
            price=price,
            price_grade=price_grade
        )

        return car
    except Exception as ex:
        print(ex)
        time.sleep(20)


for i in get_div_list(start_url):
    get_car(i).print_car()

