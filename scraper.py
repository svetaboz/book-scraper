import json
import re
import time
from urllib.parse import urljoin
import requests
import schedule
from bs4 import BeautifulSoup

def get_book_data(book_url: str) -> dict:
    """
    Функция собирает данные о книге с ее веб-страницы.

    book_url: str, URL-адрес страницы книги.
    Возвращает: dict с названием, ценой, наличием, рейтингом,
    описанием и информацией о продукте.
    """
    response = requests.get(book_url, timeout=10)
    response.raise_for_status()
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    heading = soup.find("h1")
    title = heading.get_text(strip=True)

    price_element = soup.find("p", class_="price_color")
    price = (
        price_element.get_text(strip=True)
        if price_element
        else "Цена не указана"
    )

    instock_text = soup.find("p", class_="instock availability")
    in_stock = (
        instock_text.get_text(strip=True)
        if instock_text
        else "Информация не указана"
    )
    in_stock_number = re.search(r"\d+", in_stock)
    stock = (
        int(in_stock_number.group())
        if in_stock_number
        else "Количество не указано"
    )

    rating_element = soup.find("p", class_="star-rating")
    rating = (
        rating_element.get("class")[1]
        if rating_element
        else "Рейтинг не указан"
    )

    description_header = soup.find("div", id="product_description")
    if description_header:
        description_element = description_header.find_next_sibling("p")
    else:
        description_element = None

    description = (
        description_element.get_text(strip=True)
        if description_element
        else "Описания нет"
    )

    product_info = {}
    rows = soup.find_all("tr")
    for row in rows:
        key_element = row.find("th").get_text(strip=True)
        value_element = row.find("td").get_text(strip=True)
        product_info[key_element] = value_element

    book = {
        "title": title,
        "price": price,
        "in_stock": stock,
        "rating": rating,
        "description": description,
        "product_info": product_info,
    }
    return book

def scrape_books(is_save=False) -> list:
    """
    Собирает данные обо всех книгах каталога.
    is_save: bool, при True данные сохраняются в файл.
    Возвращает: список list с данными книг.
    """
    books = []
    catalog_url = "https://books.toscrape.com/catalogue/page-1.html"
          
    while catalog_url:
            response=requests.get(catalog_url, timeout=10)
            response.raise_for_status()
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")
            cards = soup.find_all("article", class_="product_pod")
                
            for card in cards:
                link = card.find("a")
                href = link["href"]
                book_url = urljoin(catalog_url, href)
                books.append(get_book_data(book_url))

            next_item = soup.find("li", class_="next")
            if next_item:
                next_link = next_item.find("a")
                catalog_url = urljoin(catalog_url, next_link["href"])
            else:
                break
    
    if is_save:
        with open("books_data.txt", "w", encoding="utf-8") as file:
            json.dump(books, file, ensure_ascii=False, indent=2)
    
    return books