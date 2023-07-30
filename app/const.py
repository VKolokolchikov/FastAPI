"""Constants for project"""

from dataclasses import dataclass
from enum import Enum


@dataclass
class CanSeeFriends:
    ALL_MEMBERS = 1
    ONLY_FRIENDS = 2
    NOBODY = 3


@dataclass
class CanSeeWish(CanSeeFriends):
    ...


@dataclass
class EventsType:
    SINGLE = "SINGLE"
    BIRTHDAY = "BIRTHDAY"
    BUSINESS = "BUSINESS"
    ANNIVERSARY = "ANNIVERSARY"
    FELICITATION = "FELICITATION"

    WITH_CONNECT_USER = (
        BIRTHDAY,
        ANNIVERSARY,
        FELICITATION,
    )


class AnswerStatus(str, Enum):
    SUCCESS = 'success'
    DENIED = 'denied'


class Gender(str, Enum):
    MAN = 'MAN'
    WOMAN = 'WOMAN'
