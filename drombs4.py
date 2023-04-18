import time
import requests
from bs4 import BeautifulSoup

city = 'tyumen'
domain = f'https://{city}.drom.ru/auto'
start_url = 'https://auto.drom.ru/region72/suv/all/?maxprice=1300000&inomarka=1&pts=2&damaged=2&w=2&unsold=1'


class Car:
    def __init__(self, **kwargs):
        self.characters = kwargs

    def print_car(self):
        for item, value in self.characters.items():
            print(f"{item}: {value}")
        print('_______________________________________________________________________________________\n')

    def get_characters(self):
        return self.characters


def get_main_div(url):
    get_html = requests.get(url)
    soup = BeautifulSoup(get_html.content, "lxml")
    main_div = soup.find('div', class_='css-1nvf6xk eojktn00')
    return main_div


def get_car_list(div):
    div_list = div.find_all('a', class_='css-xb5nz8 e1huvdhj1')
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
        price_grade = div.find('div', class_='css-11m58oj evjskuu0')
        if not price_grade:
            price_grade = 'без оценки'
        else:
            price_grade = price_grade.text

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


count = 1
main_div = get_main_div(start_url)
while main_div:
    for i in get_car_list(main_div):
        print(count, end='. ')
        get_car(i).print_car()
        count += 1
    next_page_link = main_div.find('a', class_='css-4gbnjj e24vrp30')
    if next_page_link:
        next_page_link = next_page_link['href']
        main_div = get_main_div(next_page_link)
    else:
        main_div = None

# next_page = get