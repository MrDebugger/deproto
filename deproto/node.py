from typing import Any
from deproto.types import BaseType


class Node:
    """Represents a single node in the protobuf structure."""

    def __init__(self, index: int, value: Any, dtype: BaseType):
        self.index: int = index - 1
        self.value: Any = dtype.decode(value)
        self.value_raw: str = value
        self.dtype: BaseType = dtype
        self.type: str = dtype.type

    def change(self, value: Any) -> None:
        """Change the node's value.

        :param value: New value to set
        :type value: Any
        """
        self.value = value
        self.value_raw = self.dtype.encode(value)[1]

    def encode(self) -> str:
        """Encode the node back to protobuf format.

        :return: Encoded protobuf string
        :rtype: str
        """
        return f"!{self.index + 1}{self.type}{self.value_raw}"

    def __eq__(self, other):
        return (
            self.index == other.index and
            self.value == other.value and
            self.type == other.type
        )

    def __repr__(self):
        return f"Node({self.index}, {self.type}, {self.value})"
