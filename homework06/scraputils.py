import requests
from bs4 import BeautifulSoup
import time


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    news_table = parser.find_all("tr", {"class": "athing"})
    table_info = parser.find_all("td", {"class": "subtext"})
    for i in range(len(news_table)):
        links = table_info[i].find_all("a")
        title = news_table[i].find(class_="storylink")
        points = table_info[i].span.text.split()[0]
        try:
            if links[5].text == "discuss":
                comments = "0"
            else:
                comments = links[5].text.split()[0]
        except:
            comments = "0"
        news = {
            'author': links[0].text,
            'comments': comments,
            'points': points,
            'title': title.text,
            'url': title['href']
        }
        news_list.append(news)
    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    return parser.table.find_all('table')[1].find_all('a')[-1]['href']


def get_news(url, n_pages=30):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        print(response)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news
