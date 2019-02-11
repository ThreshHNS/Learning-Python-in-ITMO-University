from bottle import (
    route, run, template, request, redirect, static_file
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier
import string


@route('/static/<filename>')
def server_static(filename):
    print(filename)
    return static_file(filename, root='static')


@route("/")
def home_page():
    return template('index')


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    rnews = s.query(News).filter(News.id == request.query.id).first()
    rnews.label = request.query.label
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    news = get_news("https://news.ycombinator.com/newest", n_pages=30)
    s = session()
    for item in news:
        if s.query(News).filter(News.title == item['title'], News.author == item['author']).first():
            break
        else:
            s.add(News(**item))
    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    labeled_news = s.query(News).filter(News.label != None).all()
    x_train = [clean(news.title) for news in labeled_news]
    y_train = [news.label for news in labeled_news]
    classifier.fit(x_train, y_train)

    rows = s.query(News).filter(News.label == None).all()
    good, maybe, never = [], [], []
    for row in rows:
        [prediction] = classifier.predict([clean(row.title)])
        if prediction == 'good':
            good.append(row)
        elif prediction == "maybe":
            maybe.append(row)
        else:
            never.append(row)

    return template('news_recommendations', good=good, maybe=maybe, never=never)


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator).lower()


if __name__ == '__main__':
    s = session()
    labeled_news = s.query(News).filter(News.label != None).all()
    x_train = [clean(news.title) for news in labeled_news]
    y_train = [news.label for news in labeled_news]
    classifier = NaiveBayesClassifier()
    classifier.fit(x_train, y_train)
    run(host="localhost", port=8080)
