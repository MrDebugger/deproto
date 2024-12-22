from __future__ import annotations
from typing import List, Union, Optional, Any
from deproto.node import Node
from deproto.types import DataTypeFactory, BaseType


class Cluster:
    """Represents a cluster of nodes in the protobuf structure."""

    def __init__(
        self,
        index: int,
        nodes: Optional[List[Union[Node, 'Cluster']]] = None,
        parent: Optional['Cluster'] = None
    ):
        """Initialize a cluster.

        :param index: Cluster index (1-based)
        :param nodes: Optional list of nodes/clusters to initialize with
        :param parent: Optional parent cluster
        """
        self.nodes: List[Union[Node, 'Cluster']] = []
        self.total: int = 0
        self.index: int = index - 1
        self.parent: Optional['Cluster'] = parent

        if nodes:
            for node in nodes:
                self.append(node)

    def set_parent(self, parent: Optional['Cluster']) -> None:
        """Set the parent cluster for this cluster."""
        self.parent = parent

    def append(self, item: Union[Node, 'Cluster']) -> None:
        """Append a node or cluster to this cluster."""
        item.set_parent(self)
        self.nodes.append(item)
        amount = item.total + 1 if isinstance(item, Cluster) else 1
        self._increment_total(amount)

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

    def insert(self, index: int, item: Union[Node, 'Cluster']) -> None:
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

    def delete(self, index: int) -> Optional[Union[Node, 'Cluster']]:
        """Delete a node by its index.

        :param index: Index of node to delete (1-based)
        :return: Deleted node or None if not found
        """
        for i, node in enumerate(self.nodes):
            if node.index + 1 == index:
                deleted = self.nodes.pop(i)
                deleted.set_parent(None)
                self._decrement_total()
                return deleted
        return None

    def encode(self) -> str:
        """Encode the cluster back to protobuf format.

        :return: Encoded protobuf string
        :rtype: str
        """
        result = f"!{self.index + 1}m{self.total}" if self.parent else ""
        for node in self.nodes:
            result += node.encode()
        return result

    def __len__(self):
        return len(self.nodes)

    def __getitem__(self, index):
        return self.nodes[index]

    def __setitem__(self, index, value):
        self.nodes[index] = value

    def __delitem__(self, index):
        node = self.nodes[index]
        node.set_parent(None)
        del self.nodes[index]
        self._decrement_total()

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

    def add(
        self,
        index: int,
        value: Any,
        dtype: Optional[BaseType] = None
    ) -> Union[Node, 'Cluster']:
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
