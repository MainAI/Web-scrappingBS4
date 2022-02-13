import requests
import bs4


def scrap_habr(words, key=1):
    """
    Get requests to habr.com, find date, name, href article match with key words. Append request full text each article.
    :param words: list key words
    :param key: key=1 for only date-name-href, key=2 for append full page text for each article
    :return:
    """
    link_dict = {}
    base_url = "https://habr.com"
    url = base_url + "/ru/all/"
    headers = {
        'cookie': '__gads=ID=e93abb8a9168e27a-220272b53ecd008a:T=1644768545:RT=1644768545:S'
                  '=ALNI_MYCU9oKVjjBUa3of9lLx_dWVygHkA; '
                  'fpestid=z4nUvrZXYnczFMcYWf_qOzU2byvS_weRaYZWEnpSj3wkZXJvxaRSFCNZAW9k7_xdDU2aJg',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'if-none-match': 'W/"cd5653446bc5a6cdf57ef387aa5d31c9"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/98.0.4758.82 Safari/537.36 '
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    text = response.text
    soup = bs4.BeautifulSoup(text, features='html.parser')
    articles = soup.find_all('article')
    for article in articles:
        hubs = article.find_all(class_="tm-article-snippet__hubs-item")
        hubs = set(hub.text.strip() for hub in hubs)
        for hub in hubs:
            if hub in words:
                href = article.find(class_="tm-article-snippet__title-link").attrs['href']
                name = article.find(class_="tm-article-snippet__title-link").text
                times = article.find(class_="tm-article-snippet__datetime-published")
                time = times.find('time').attrs['title']
                link = base_url + href
                link_dict[name] = link
                print(f"<{time}> - <{name}> - <{link}>")

    if key == 2:
        for link_key in link_dict.keys():
            print(f"\n{link_key}\n")
            response_page = requests.get(link_dict[link_key], headers=headers)
            response_page.raise_for_status()
            text_full = response_page.text
            soup_full_page = bs4.BeautifulSoup(text_full, features='html.parser')
            ps = soup_full_page.find_all('p')
            for p in ps:
                print(p.get_text())
    return


if __name__ == '__main__':
    KEYWORDS = ['Дизайн', 'Фото', 'Web', 'Python', 'Криптовалюты', 'Телемедицина']
    scrap_habr(KEYWORDS, 2)


