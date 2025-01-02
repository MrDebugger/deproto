"""Cluster module.

This module provides the Cluster class for representing a cluster of nodes
in the protobuf structure.
"""

from __future__ import annotations

from typing import Any, List, Optional, Union

from deproto.node import Node
from deproto.types import BaseType, DataTypeFactory


class Cluster:
    """Represents a cluster of nodes in the protobuf structure."""

    total: int = 0
    index: int = 0

    def __init__(
        self,
        index: int,
        nodes: Optional[List[Union[Node, "Cluster"]]] = None,
        parent: Optional["Cluster"] = None,
    ):
        """Initialize a cluster.

        :param index: Cluster index (1-based)
        :param nodes: Optional list of nodes/clusters to initialize with
        :param parent: Optional parent cluster
        """
        self.nodes: List[Union[Node, "Cluster"]] = []
        self.total: int = 0
        self.index: int = index - 1
        self.parent: Optional["Cluster"] = parent

        if nodes:
            for node in nodes:
                self.append(node)

    def _increment_total(self, amount: int = 1) -> None:
        """Increment total and propagate up to parent."""
        self.total += amount
        if self.parent:
            self.parent._increment_total(amount)

    def _decrement_total(self, amount: int = 1) -> None:
        """Decrement total and propagate up to parent."""
        self.total -= amount
        if self.parent:
            self.parent._decrement_total(amount)

    def set_parent(self, parent: Optional["Cluster"]) -> None:
        """Set the parent cluster for this cluster."""
        self.parent = parent

    def append(self, item: Union[Node, "Cluster"]) -> None:
        """Append a node or cluster to this cluster."""
        item.set_parent(self)
        self.nodes.append(item)
        amount = item.total + 1 if isinstance(item, Cluster) else 1
        self._increment_total(amount)

    def find(
        self, index: int, _raise: bool = False
    ) -> Optional[Union[Node, "Cluster"]]:
        """Find a node or cluster at a specific index.

        :param index: Index of node to find (1-based)
        :param _raise: If True, raise IndexError if index is not found
        :return: Node or Cluster at index
        """
        for node in self.nodes:
            if node.index + 1 == index:
                return node
        if _raise:
            raise IndexError(f"Index {index} not found in cluster")
        return None

    def insert(self, index: int, item: Union[Node, "Cluster"]) -> None:
        """Insert a node or cluster at a specific index position.

        :param index: Target index for insertion (1-based)
        :param item: Node or Cluster to insert
        """
        pos = 0
        for i, node in enumerate(self.nodes):
            if node.index + 1 > index:
                pos = i
                break
            pos = i + 1

        self.nodes.insert(pos, item)
        self._increment_total()

    def delete(self, index: int) -> Optional[Union[Node, "Cluster"]]:
        """Delete a node by its index.

        :param index: Index of node to delete (1-based)
        :return: Deleted node
        :raises: IndexError if index is not found
        """
        node = self.find(index, _raise=True)
        node.set_parent(None)
        self.nodes.remove(node)
        self._decrement_total()
        return node

    def encode(self) -> str:
        """Encode the cluster back to protobuf format.

        :return: Encoded protobuf string
        :rtype: str
        """
        result = f"!{self.index + 1}m{self.total}" if self.parent else ""
        for node in self.nodes:
            result += node.encode()
        return result

    def replace(
        self,
        index: int,
        value: Union[Node, "Cluster"],
    ) -> Union[Node, "Cluster"]:
        """Replace a node at a specific index.

        :param index: Index of node to replace (1-based)
        :param value: New value for node
        :return: Replaced node
        """
        node = self.delete(index)
        self.insert(index, value)
        return node

    def at(self, index: int):
        """Get a node at a specific index.

        :param index: Index of node to get (0-based)
        :return: Node at index
        """
        return self.nodes[index]

    def __len__(self):
        return len(self.nodes)

    def __getitem__(self, index):
        """Get a node at a specific index.

        :param index: Index of node to get (1-based)
        :return: Node at index
        """
        return self.find(index, _raise=True)

    def __setitem__(self, index, value):
        """Set a node at a specific index.

        :param index: Index of node to set (1-based)
        :param value: New value for node
        :return: Set node
        """
        node = self.find(index, _raise=True)
        node.value = value
        return node

    def __delitem__(self, index):
        """Delete a node at a specific index.

        :param index: Index of node to delete (1-based)
        :return: Deleted node
        """
        return self.delete(index)

    def __contains__(self, item):
        return item in self.nodes

    def __repr__(self):
        node_reprs = []
        for node in self.nodes:
            if isinstance(node, Cluster):
                node_reprs.append("Cluster([...])")
            else:
                node_reprs.append(repr(node))
        return f"Cluster([{', '.join(node_reprs)}])"

    def _fill_missing_nodes(self, nodes: list, index: int) -> None:
        """Fill missing nodes in the list."""
        missing_nodes = index - len(nodes)
        if missing_nodes > 0:
            nodes.extend([None] * missing_nodes)

    def to_json(self) -> list:
        """Convert the cluster to a JSON-serializable dictionary.

        :return: List representation of the cluster
        :rtype: list
        """
        nodes = []
        for node in self.nodes:
            self._fill_missing_nodes(nodes, node.index)
            if isinstance(node, Cluster):
                nodes.append(node.to_json())
            else:
                nodes.append(node.value)
        return nodes

    def add(
        self, index: int, value: Any, dtype: Optional[BaseType] = None
    ) -> Union[Node, "Cluster"]:
        """Add a node or cluster in a single line.

        Supports multiple formats:
        - add(1, "value")  # auto-detect type
        - add(1, "value", StringType())  # explicit type
        - add(1, [(1, "value")])  # Cluster of Nodes
        - add(1, Node(1, "value", StringType()))  # direct Node
        - add(1, Cluster(1, [...]))  # direct Cluster
        """
        if isinstance(value, (Node, Cluster)):
            self.append(value)
            return value

        if isinstance(value, (list, tuple)):
            cluster = Cluster(index)
            for item in value:
                if isinstance(item, (Node, Cluster)):
                    cluster.append(item)
                elif len(item) == 2:
                    idx, val = item
                    cluster.add(idx, val)
                else:
                    idx, val, typ = item
                    cluster.add(idx, val, typ)
            self.append(cluster)
            return cluster

        if dtype is None:
            dtype = DataTypeFactory.get_type_by_value(value)()
        node = Node(index, value, dtype)
        self.append(node)
        return node
