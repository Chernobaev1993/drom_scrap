import time
import requests
from bs4 import BeautifulSoup
from car import Car

domain = 'https://auto.drom.ru/'
start_url = f'{domain}region72/all/?maxprice=500000&minyear=2008&inomarka=1&pts=2&damaged=2&w=2&unsold=1'


# Возвращает главный тег <div>
def get_main_page_div(url):
    get_html = requests.get(url)
    soup = BeautifulSoup(get_html.content, "lxml")
    main_page_div = soup.find('div', class_='css-1nvf6xk eojktn00')
    return main_page_div


# Возвращает список с каждым тегом <div>, в которых авто
def get_car_list(div):
    div_list = div.find_all('a', class_='css-xb5nz8 e1huvdhj1')
    return div_list


# Возвращает объект класса Car, который создается с помощью разбора тега <div> конкретного авто
def get_car(div):
    try:
        # Ищем нужные нам параметры автомобиля
        link = div['href']
        link_lst = link.split('/')
        brand = link_lst[3]
        model = link_lst[4]
        car_id = link_lst[5].split('.')[0]
        year = int(div.find('div', class_="css-l1wt7n e3f4v4l2").find('span').text.split(', ')[1])

        # characters = div.find("div", class_="css-1fe6w6s e162wx9x0").find_all('span', class_='css-1l9tp44 e162wx9x0')
        characters = div.find("div", class_="css-1fe6w6s e162wx9x0").find_all('span', attrs={"data-ftid": "bull_description-item"})
        characters_lst = []
        for item in characters:
            characters_lst.append(item.text.replace(',', ''))
        print(characters_lst)
        price = int(div.find('span', class_='css-46itwz e162wx9x0').text.replace('\u00A0', '').replace('₽', ''))
        price_grade = div.find('div', class_='css-11m58oj evjskuu0')
        if not price_grade:
            price_grade = 'без оценки'
        else:
            price_grade = price_grade.text

        # avg_price = get_avg_price(brand, model, year, 72)
        # dif_price = price - avg_price

        car = Car(
            car_id=car_id,
            link=link,
            brand=brand.upper(),
            model=model.upper(),
            year=year,
            price=price,
            price_grade=price_grade,
            characters=characters_lst,
            # avg_price=avg_price,
            # dif_price=dif_price
        )
        return car
    except Exception as ex:
        print(ex)
        time.sleep(20)


# Возвращает среднюю цену (int) на конкретный авто по конкретному региону
# def get_avg_price(brand, model, year, region):
#     url = f'{domain}region{region}/{brand}/{model}/?minyear={year-1}&maxyear={year+1}&pts=2&damaged=2&unsold=1'
#     price = []
#     main_div = get_main_page_div(url)
#     while main_div:
#         for car_div in get_car_list(main_div):
#             car_price = int(car_div.find('span', class_='css-46itwz e162wx9x0').text.replace('\u00A0', '').replace('₽', ''))
#             price.append(car_price)
#         next_page_link = main_div.find('a', class_='css-4gbnjj e24vrp30')
#         if next_page_link:
#             next_page_link = next_page_link['href']
#             main_div = get_main_page_div(next_page_link)
#         else:
#             main_div = None
#     return int(sum(price)/len(price))


# Запуск основной функции
def start():
    main_div = get_main_page_div(start_url)
    while main_div:
        for car_div in get_car_list(main_div):
            get_car(car_div).print_car()

        # Получаем следующую страницу
        next_page_link = main_div.find('a', class_='css-4gbnjj e24vrp30')
        if next_page_link:
            next_page_link = next_page_link['href']
            main_div = get_main_page_div(next_page_link)
        else:
            main_div = None


start()

# data-ftid=bull_description-item