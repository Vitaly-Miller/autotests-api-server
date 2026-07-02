from enum import Enum


class APIRoutes(str, Enum):
    USERS = '/users'
    FILES = '/files'
    COURSES = '/courses'
    EXERCISES = '/exercises'
    AUTHENTICATION = '/authentication'
    CLEANUP = '/cleanup'

    def as_tag(self) -> str:
        return self[1:]
