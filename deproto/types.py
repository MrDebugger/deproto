"""Data types for deproto."""

from base64 import urlsafe_b64decode, urlsafe_b64encode
from typing import Any


class BaseType:
    type: str

    @staticmethod
    def decode(value):
        return value

    @staticmethod
    def encode(value):
        return "s", str(value)


class BytesType(BaseType):
    type: str = "B"

    @staticmethod
    def decode(value):
        padding = "=" * (-len(value) % 4)
        return urlsafe_b64decode(value + padding).decode("utf8")

    @staticmethod
    def encode(value):
        if isinstance(value, str):
            value = value.encode("utf8")
        return "B", urlsafe_b64encode(value).rstrip(b"=").decode("utf8")


class BoolType(BaseType):
    type: str = "b"

    @staticmethod
    def decode(value):
        return value == "1"

    @staticmethod
    def encode(value):
        return "b", "1" if value else "0"


class FloatType(BaseType):
    type: str = "f"

    @staticmethod
    def decode(value):
        return float(value)

    @staticmethod
    def encode(value):
        return "f", str(value)


class DoubleType(FloatType):
    type: str = "d"

    @staticmethod
    def encode(value):
        return "d", str(value)


class IntType(BaseType):
    type: str = "i"

    @staticmethod
    def decode(value):
        return int(value)

    @staticmethod
    def encode(value):
        return "i", str(value)


class EnumType(IntType):
    type: str = "e"

    @staticmethod
    def encode(value):
        return "e", str(value)


class SFixed32Type(IntType):
    type: str = "g"

    @staticmethod
    def encode(value):
        return "g", str(value)


class SFixed64Type(IntType):
    type: str = "h"

    @staticmethod
    def encode(value):
        return "h", str(value)


class SInt32Type(IntType):
    type: str = "n"

    @staticmethod
    def encode(value):
        return "n", str(value)


class SInt64Type(IntType):
    type: str = "o"

    @staticmethod
    def encode(value):
        return "o", str(value)


class UInt32Type(IntType):
    type: str = "u"

    @staticmethod
    def encode(value):
        return "u", str(value)


class UInt64Type(IntType):
    type: str = "v"

    @staticmethod
    def encode(value):
        return "v", str(value)


class Fixed32Type(IntType):
    type: str = "x"

    @staticmethod
    def encode(value):
        return "x", str(value)


class Fixed64Type(IntType):
    type: str = "y"

    @staticmethod
    def encode(value):
        return "y", str(value)


class StringType(BaseType):
    type: str = "s"

    @staticmethod
    def decode(value):
        return value.replace("*21", "!").replace("*2A", "*")

    @staticmethod
    def encode(value):
        return "s", value.replace("*", "*2A").replace("!", "*21")


class Base64StringType(BaseType):
    type: str = "z"

    @staticmethod
    def decode(value) -> str:
        padding = "=" * (-len(value) % 4)
        return urlsafe_b64decode(value + padding).decode("utf8")

    @staticmethod
    def encode(value):
        if isinstance(value, str):
            value = value.encode("utf8")
        return ("z", urlsafe_b64encode(value).rstrip(b"=").decode("utf8"))


class DataTypeFactory:
    _type_classes = {
        "B": BytesType,
        "b": BoolType,
        "d": DoubleType,
        "e": EnumType,
        "f": FloatType,
        "g": SFixed32Type,
        "h": SFixed64Type,
        "i": IntType,
        "j": IntType,
        "m": BaseType,
        "n": SInt32Type,
        "o": SInt64Type,
        "s": StringType,
        "u": UInt32Type,
        "v": UInt64Type,
        "x": Fixed32Type,
        "y": Fixed64Type,
        "z": Base64StringType,
    }

    @staticmethod
    def get_type(kind: str) -> BaseType:
        if kind in DataTypeFactory._type_classes:
            return DataTypeFactory._type_classes[kind]
        else:
            raise ValueError(f"Unknown data type: {kind}")

    @staticmethod
    def get_type_by_value(value: Any) -> BaseType:
        if isinstance(value, bytes):
            return BytesType
        elif isinstance(value, bool):
            return BoolType
        elif isinstance(value, float):
            if value * 10 % 1 == 0:
                return FloatType
            return DoubleType
        elif isinstance(value, int):
            return IntType
        elif isinstance(value, str):
            if value.isascii():
                return StringType
            else:
                return Base64StringType
        else:
            return BaseType
