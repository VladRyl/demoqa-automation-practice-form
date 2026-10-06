from enum import Enum


class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"


class Hobby(Enum):
    SPORTS = "Sports"
    READING = "Reading"
    MUSIC = "Music"


class ValidationState(Enum):
    VALID = "rgb(25, 135, 84)"
    INVALID = "rgb(220, 53, 69)"
