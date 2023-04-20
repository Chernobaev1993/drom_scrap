import time
import requests
from bs4 import BeautifulSoup

# city = 'tyumen'
# domain = f'https://{city}.drom.ru/auto'
start_url = 'https://auto.drom.ru/region72/suv/all/?maxprice=1300000&inomarka=1&pts=2&damaged=2&w=2&unsold=1'


class Car:
    def __init__(self, **kwargs):
        self.attrs = kwargs

    def print_car(self):
        for item, value in self.attrs.items():
            if item == 'characters':
                continue
            print(f"{item}: {value}")
        print('_______________________________________________________________________________________\n')

    def set_attrs(self):
        lst_character = self.attrs['characters'].split(' | ')
        for item in lst_character:
            if 'передний' in item:
                self.attrs['wheel'] = 'передний'
            elif 'задний' in item:
                self.attrs['wheel'] = 'задний'
            elif '4WD' in item:
                self.attrs['wheel'] = 'полный'
            elif 'л.с.' in item:
                self.attrs['engine'] = lst_character[0]
            elif 'АКПП' in item:
                self.attrs['trans'] = 'автомат'
            elif 'механика' in item:
                self.attrs['trans'] = 'механика'
            elif 'робот' in item:
                self.attrs['trans'] = 'робот'
            elif 'вариатор' in item:
                self.attrs['trans'] = 'вариатор'
            elif 'бензин' in item:
                self.attrs['fuel'] = 'бензин'
            elif 'дизель' in item:
                self.attrs['fuel'] = 'дизель'
            elif 'гибрид' in item:
                self.attrs['fuel'] = 'гибрид'
            elif 'электро' in item:
                self.attrs['fuel'] = 'электрический'
            elif 'км' in item:
                self.attrs['run'] = lst_character[-1]

    def get_attrs(self):
        return self.attrs


def get_main_page_div(url):
    get_html = requests.get(url)
    soup = BeautifulSoup(get_html.content, "lxml")
    main_page_div = soup.find('div', class_='css-1nvf6xk eojktn00')
    return main_page_div


def get_car_list(div):
    div_list = div.find_all('a', class_='css-xb5nz8 e1huvdhj1')
    return div_list


# def get_avg_price(brand, model, year):
#     # brand = car.get_attrs()['brand']
#     # model = car.get_attrs()['model']
#     # year = car.get_attrs()['year']
#     url = f'https://auto.drom.ru/region72/{brand.lower()}/{model.lower()}/year-{year}/?pts=2&damaged=2&unsold=1'
#     price = []
#     main_div = get_main_page_div(url)
#     print(url, main_div)
#     while main_div:
#         for car_div in get_car_list(main_div):
#             car_price = car_div.find('span', class_='css-46itwz e162wx9x0').text.replace('\xa0', '')
#             price.append(car_price)
#         next_page_link = main_div.find('a', class_='css-4gbnjj e24vrp30')
#         if next_page_link:
#             next_page_link = next_page_link['href']
#             main_div = get_main_page_div(next_page_link)
#         else:
#             main_div = None
#     return price
    # while main_div:
    #     for car_div in get_car_list(main_div):
    #         get_car(car_div).print_car()
    #     next_page_link = main_div.find('a', class_='css-4gbnjj e24vrp30')
    #     if next_page_link:
    #         next_page_link = next_page_link['href']
    #         main_div = get_main_page_div(next_page_link)
    #     else:
    #         main_div = None
    # div_list = get_car_list(main_div)


def get_car(div):
    try:
        # Ищем нужные нам параметры автомобиля
        link = div['href']
        # Попробуй получить brand и модель через ссылку
        car_id = int(link.split('/')[-1].split('.')[0])
        name, year = div.find('div', class_="css-l1wt7n e3f4v4l2").find('span').text.split(', ')
        brand, *model = name.split(' ')

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
        # avg_price = get_avg_price(brand, '_'.join(model), year)
        car = Car(
            brand=brand.upper(),
            model=' '.join(model).upper(),
            year=year,
            characters=' | '.join(lst),
            price=price,
            price_grade=price_grade,
            car_id=car_id,
            link=link,
            # abf_price=avg_price
        )
        car.set_attrs()
        return car
    except Exception as ex:
        print(ex)
        time.sleep(20)


def start():
    main_div = get_main_page_div(start_url)
    while main_div:
        for car_div in get_car_list(main_div):
            get_car(car_div).print_car()
        next_page_link = main_div.find('a', class_='css-4gbnjj e24vrp30')
        if next_page_link:
            next_page_link = next_page_link['href']
            main_div = get_main_page_div(next_page_link)
        else:
            main_div = None


start()
