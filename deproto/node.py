"""Node Module.

This module provides the Node class for representing individual data points
in the protobuf structure.
"""

from __future__ import annotations

from typing import Any, Optional

from deproto.types import BaseType


class Node:
    """
    A single node in the protobuf structure.

    Represents an individual data point with a specific type and value.
    Nodes can be part of a cluster and maintain a reference to their parent.

    :param index: The 1-based index of the node in its parent cluster
    :type index: int
    :param value: The value stored in the node
    :type value: Any
    :param dtype: The data type handler for the value
    :type dtype: BaseType
    :param parent: The parent cluster containing this node, defaults to None
    :type parent: Optional[Cluster]
    """

    def __init__(
        self,
        index: int,
        value: Any,
        dtype: BaseType,
        parent: Optional["Cluster"] = None,  # noqa: F821
    ):
        self.index: int = index - 1
        self.value: Any = value
        self.value_raw: str = dtype.encode(value)[1]
        self.dtype: BaseType = dtype
        self.type: str = dtype.type
        self.parent: Optional["Cluster"] = parent  # noqa: F821

    def change(self, value: Any) -> None:
        """
        Change the node's value.

        Updates both the value and its raw encoded form.

        :param value: New value to set
        :type value: Any
        """
        self.value = value
        self.value_raw = self.dtype.encode(value)[1]

    def encode(self) -> str:
        """
        Encode the node back to protobuf format.

        :return: Encoded protobuf string
        :rtype: str
        """
        return f"!{self.index + 1}{self.type}{self.value_raw}"

    def __eq__(self, other: Any) -> bool:
        """
        Compare this node with another for equality.

        :param other: Another node to compare with
        :type other: Any
        :return: True if nodes are equal, False otherwise
        :rtype: bool
        """
        return (
            self.index == other.index
            and self.value == other.value
            and self.type == other.type
        )

    def __repr__(self) -> str:
        """
        Get string representation of the node.

        :return: String representation
        :rtype: str
        """
        return f"Node({self.index + 1}, {self.type}, {self.value})"

    def set_parent(self, parent: "Cluster") -> None:  # noqa: F821
        """
        Set the parent cluster for this node.

        :param parent: The cluster to set as parent
        :type parent: Cluster
        """
        self.parent = parent
