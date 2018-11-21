from statistics import median
from typing import Optional
from datetime import datetime, date
from api import get_friends
from api_models import User


def age_predict(user_id: int) -> int:
    """ Наивный прогноз возраста по возрасту друзей
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: идентификатор пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    friends = get_friends(user_id, 'bdate')
    age_list = []

    for friend in friends['response']['items']:
    	person = User(**friend)
    	if person.bdate and len(person.bdate) > 8:
    		time_now = datetime.now()
    		time_bdate = datetime.strptime(person.bdate, "%d.%m.%Y")
    		age = (time_now - time_bdate)
    		age_list.append(int(age.days // 365.25))

    return int(median(age_list)) if age_list else None

