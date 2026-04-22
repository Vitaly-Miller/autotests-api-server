from enum import Enum


class APIRoutes(str, Enum):
    USERS = '/users'
    FILES = '/files'
    COURSES = '/courses'
    EXERCISES = '/exercises'
    AUTHENTICATION = '/authentication'

    def as_tag(self) -> str:
        return self[1:]
