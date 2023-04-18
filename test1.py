import time
import requests
from bs4 import BeautifulSoup

city = 'tyumen'
domain = f'https://{city}.drom.ru/auto'
final_url = f'{domain}/all/?maxprice=500000&pts=2&w=2&unsold=1'

get_html = requests.get(final_url)
soup = BeautifulSoup(get_html.content, "lxml")
div = soup.find('div', class_='css-1nvf6xk eojktn00').find_all('a', class_='css-xb5nz8 e1huvdhj1')

link = div[0]['href']  # Ok
car_id = link.split('/')[-1]  # Ok
name, year = div[0].find('div', class_="css-l1wt7n e3f4v4l2").find('span').text.split(', ')  # Ok

characters = div[0].find("div", class_="css-1fe6w6s e162wx9x0").find_all('span', class_='css-1l9tp44 e162wx9x0')
lst = []
for i in characters:
    lst.append(i.text.replace(',', ''))  # Ok

price = div[0].find('span', class_='css-46itwz e162wx9x0').text  # Ok
price_grade = div[0].find('div', class_='css-11m58oj evjskuu0').text  # Ok
print(price_grade)

car_dict = {
    'Марка': name,
    'Год': year,
    'Характеристики': ' | '.join(lst),
    'Цена': price,
    'Оценка': price_grade,
    'Ссылка': link
    }  # Ok
