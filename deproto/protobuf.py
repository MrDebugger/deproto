import re
from typing import List, Tuple, Optional
from deproto.node import Node
from deproto.cluster import Cluster
from deproto.types import DataTypeFactory


class Protobuf:
    """Decoder for Google Maps protobuf format."""

    def __init__(self, pb_string: str):
        self.pb_string: str = pb_string
        self.nodes: List[Tuple[str, str, str]] = []
        self.original_nodes: List[Tuple[str, str, str]] = []
        self.root: Optional[Cluster] = None

    def reset(self) -> None:
        """Reset the decoder to its original state."""
        self.nodes = self.original_nodes.copy()
        self.decode()

    def split(self) -> None:
        """Split the protobuf string into node tuples."""
        self.nodes = [
            self.expand(node)
            for node in self.pb_string.split('!')
            if node
        ]
        self.original_nodes = self.nodes.copy()

    def expand(self, node: str) -> Tuple[str, str, str]:
        """Expand a protobuf node string into components."""
        matches = re.match(r'(\d+)([a-zA-Z])(.*)', node)
        if not matches or len(matches.groups()) != 3:
            raise ValueError(
                f"Invalid protobuf-encoded string: {node}"
            )
        return matches.groups()

    def to_cluster(self, nodes: List[Tuple[str, str, str]]) -> Cluster:
        """Convert nodes list to a cluster structure."""
        _id, kind, value = nodes.pop(0)
        cluster = Cluster(int(_id), int(value))
        needed_nodes = [
            nodes.pop(0)
            for _ in range(int(value))
        ]

        while needed_nodes:
            node = needed_nodes[0]
            if node[1] == 'm':
                sub_cluster = self.to_cluster(needed_nodes)
                cluster.append(sub_cluster)
            else:
                cluster.append(self.to_node(needed_nodes.pop(0)))

        return cluster

    def to_node(self, node: Tuple[str, str, str]) -> Node:
        """Convert node tuple to Node object."""
        _id, kind, value = node
        return Node(int(_id), value, DataTypeFactory.get_type(kind))

    def decode(self) -> Cluster:
        """Decode the protobuf string into a tree structure."""
        self.split()
        nodes = self.nodes.copy()
        self.root = Cluster(1, len(nodes))

        while nodes:
            node = nodes[0]
            if node[1] == 'm':
                cluster = self.to_cluster(nodes)
                self.root.append(cluster)
            else:
                self.root.append(self.to_node(nodes.pop(0)))

        return self.root

    def encode(self) -> str:
        """Encode the current structure back to protobuf format.

        :return: Encoded protobuf string
        :rtype: str
        """
        if not self.root:
            return ""
        return "".join(node.encode() for node in self.root.nodes)

    def print_tree(self, node=None, prefix="") -> None:
        """Print visual representation of the tree."""
        if node is None:
            node = self.root
            prefix = ""
            print(f"{node.index + 1}m{node.total}")

        if isinstance(node, Cluster):
            for i, child in enumerate(node.nodes):
                is_last = i == len(node.nodes) - 1
                connector = "└── " if is_last else "├── "
                print(f"{prefix}{connector}{child.index + 1}", end="")

                if isinstance(child, Cluster):
                    print(f"m{child.total}")
                    new_prefix = prefix + ("    " if is_last else "│   ")
                    self.print_tree(child, new_prefix)
                else:
                    print(f"{child.type}{child.value_raw}")
