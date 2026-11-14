from scraper import get_book_data

book_url = (
    "https://books.toscrape.com/catalogue/"
    "a-light-in-the-attic_1000/index.html"
)

def test_get_book_data_returns_dict():
    book_test = get_book_data(book_url)
    assert isinstance(book_test, dict)


def test_get_book_data_title():
    book_test = get_book_data(book_url)
    title_test = book_test["title"]
    assert title_test == "A Light in the Attic"


def test_get_book_data_stock():
    book_test = get_book_data(book_url)
    in_stock_test = book_test["in_stock"]
    assert in_stock_test == 22