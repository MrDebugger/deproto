from typing import List, Union, Optional
from deproto.node import Node


class Cluster:
    """Represents a cluster of nodes in the protobuf structure."""

    def __init__(self, index: int, total: int):
        self.nodes: List[Union[Node, 'Cluster']] = []
        self.total: int = total
        self.index: int = index - 1

    def append(self, item: Union[Node, 'Cluster']) -> None:
        """Append a node or cluster to this cluster."""
        self.nodes.append(item)

    def insert(self, index: int, item: Union[Node, 'Cluster']) -> None:
        """Insert a node or cluster at a specific index position.

        :param index: Target index for insertion (1-based)
        :param item: Node or Cluster to insert
        """
        # Find insertion position based on node indexes
        pos = 0
        for i, node in enumerate(self.nodes):
            if node.index + 1 > index:
                pos = i
                break
            pos = i + 1

        self.nodes.insert(pos, item)
        self.total += 1

    def delete(self, index: int) -> Optional[Union[Node, 'Cluster']]:
        """Delete a node by its index.

        :param index: Index of node to delete (1-based)
        :return: Deleted node or None if not found
        """
        for i, node in enumerate(self.nodes):
            if node.index + 1 == index:
                return self.nodes.pop(i)
        return None

    def encode(self) -> str:
        """Encode the cluster back to protobuf format.

        :return: Encoded protobuf string
        :rtype: str
        """
        result = f"!{self.index + 1}m{self.total}"
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
        del self.nodes[index]
        self.total -= 1

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
