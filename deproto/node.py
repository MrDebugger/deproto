from __future__ import annotations
from typing import Any, Optional, Union
from deproto.types import BaseType


class Node:
    """Represents a single node in the protobuf structure."""

    def __init__(
        self,
        index: int,
        value: Any,
        dtype: BaseType,
        parent: Optional['Cluster'] = None
    ):
        self.index: int = index - 1
        self.value: Any = value
        self.value_raw: str = dtype.encode(value)[1]
        self.dtype: BaseType = dtype
        self.type: str = dtype.type
        self.parent: Optional[Union[Node, 'Cluster']] = parent

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
        return f"Node({self.index + 1}, {self.type}, {self.value})"

    def set_parent(self, parent: Union[Node, 'Cluster']) -> None:
        """Set the parent cluster for this node."""
        self.parent = parent
