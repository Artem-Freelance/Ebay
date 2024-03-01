import time
import fake_useragent
import requests
from bs4 import BeautifulSoup
import csv
from fake_useragent import UserAgent

user = UserAgent()

headers = {
    'User-Agent': user.random,
    'Accept-Language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
}


def writing(price_iterations, name_iterations, url_iterations):
    l_urls, l_names, l_prices = [], [], []

    pages = 1

    last_page = False
    while not last_page:
        # settings
        url = f"https://www.ebay.com/b/Jordan-1-Retro-OG-High-UNC-Toe/15709/bn_7119139207?_pgn={pages}&rt=nc"
        req = requests.get(url, headers=headers).text
        soup = BeautifulSoup(req, 'lxml')

        # finds
        cards = soup.find_all('ul', class_='brwrvr__item-results brwrvr__item-results--gallery')
        names = soup.find_all('h3', class_='bsig__title__text')
        urls = soup.find_all('a', class_="bsig__title__wrapper")
        prices = soup.find_all('span', class_="textual-display bsig__price bsig__price--displayprice")

        # questions
        if not cards:
            last_page = True

        # cycles
        for name in names:
            print(f"Оброблена: {name_iterations} назва")
            name_iterations += 1
            l_names.append(name.text)

        for url in urls:
            print(f"Оброблена: {url_iterations} силка")
            url_iterations += 1
            l_urls.append(url['href'])

        for price in prices:
            print(f"Оброблена: {price_iterations} ціна")
            price_iterations += 1
            price = price.text
            l_prices.append(price)

        if cards:
            print(f"[INFO] - Оброблено {pages}/26 сторінок")
            time.sleep(3)
        elif not cards:
            last_page = True

        pages += 1

    # convert to csv
    try:
        with open('jordan.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            for url_writing, name_writing, price_writing in zip(l_names, l_urls, l_prices):
                writer.writerow([name_writing, url_writing, price_writing])
    except Exception as e:
        print(F'Не можемо відкрити файл. [ERROR]: {e}')

    print(f'Дані успішно записані у csv: {file}')


def main():
    writing(1, 1, 1)

if __name__ == '__main__':
    main()
