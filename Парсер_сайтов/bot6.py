import requests
from bs4 import BeautifulSoup

url = 'https://scrapingclub.com/exercise/list_basic/'
params = {'page': 1}
# задаем число больше номера первой страницы, для старта цикла
pages = 2
n = 1

while params['page'] <= pages:
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all('div', class_='col-lg-4 col-md-6 mb-4')

for n, i in enumerate(items, start=n):
    itemName = i.find('h4', class_='card-title').text.strip()
    itemPrice = i.find('h5').text
    print(f'{n}: {itemPrice} за {itemName}')

# [-2] предпоследнее значение, потому что последнее "Next"
last_page_num = int(soup.find_all('a', class_='page-link')[-2].text)
pages = last_page_num if pages < last_page_num else pages
params['page'] += 1