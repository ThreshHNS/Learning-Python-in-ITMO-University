import requests
import time

from config import VK_CONFIG, PLOTLY_CONFIG
from api_models import Message

def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    for retry in range(max_retries):
        try:
            r = requests.get(url, params=params, timeout=timeout)
            return r
        except requests.exceptions.RequestException:
            if retry == max_retries - 1:
                raise
            backoff_value = backoff_factor * (2 ** retry)
            time.sleep(backoff_value)


def get_friends(user_id, fields):
    """ Вернуть данных о друзьях пользователя

    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"

    query_params = {
        'access_token': VK_CONFIG['access_token'],
        'v': VK_CONFIG['version'],
        'user_id': user_id,
        'fields': fields
    }

    url = f"{VK_CONFIG['domain']}/friends.get"
    response = get(url, params=query_params)
    return response.json()


def messages_get_history(user_id, offset=0, count=20):
    """ Получить историю переписки с указанным пользователем

    :param user_id: идентификатор пользователя, с которым нужно получить историю переписки
    :param offset: смещение в истории переписки
    :param count: число сообщений, которое нужно получить
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"

    messages = []
    max_count = 200
    query_params = {
        'access_token': VK_CONFIG['access_token'],
        'v': VK_CONFIG['version'],
        'user_id': user_id,
        'offset': offset,
        'count': min(max_count, count)
    }

    url = f"{VK_CONFIG['domain']}/messages.getHistory"

    while count > 0:

        response = get(url, params=query_params)
        count -= min(count, max_count)
        query_params['offset'] += 200
        query_params['count'] = min(count, max_count)
        messages += response.json()['response']['items']
        time.sleep(0.4)

    messages_list = [Message(**message) for message in messages]
    return messages_list

if __name__ == '__main__':
    s = messages_get_history(53369046, count=250)
    print(count_dates_from_messages(s))