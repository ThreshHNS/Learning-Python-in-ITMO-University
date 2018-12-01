from typing import List, Optional
from pydantic import BaseModel


class BaseUser(BaseModel):
    """ Модель пользователя с базовыми полями """
    id: int
    first_name: str
    last_name: str
    online: Optional[int]
    deactivated: Optional[str]


class User(BaseUser):
    """ Модель пользователя с необязательным полем дата рождения """
    bdate: Optional[str]


class Message(BaseModel):
    """ Модель сообщения """
    id: int
    peer_id: int
    from_id: Optional[str]
    date: float
    text: str
    random_id: int
    important: bool