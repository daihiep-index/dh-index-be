from enum import Enum


class EnumType(str, Enum):
    @classmethod
    def choices(cls):
        return tuple((x.value, x.name) for x in cls)

    @classmethod
    def list(cls):
        return list(map(lambda x: x.value, cls))

    def __str__(self):
        return self.value


class TypeEmailEnum(EnumType):
    REGISTER = "REGISTER"
    RESET_PASSWORD = "RESET_PASSWORD"
