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
        cluster = Cluster(int(_id))
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
        type = DataTypeFactory.get_type(kind)
        return Node(int(_id), type.decode(value), type)

    def decode(self) -> Cluster:
        """Decode the protobuf string into a tree structure."""
        self.split()
        nodes = self.nodes.copy()
        self.root = Cluster(1)

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

    def _tree_lines(self, node: Cluster, prefix: str) -> List[str]:
        """Helper method to generate tree lines recursively.

        :param node: Cluster node to process
        :param prefix: Current indentation prefix
        :return: List of formatted tree lines
        """
        result = []
        for i, child in enumerate(node.nodes):
            is_last = i == len(node.nodes) - 1
            connector = "└── " if is_last else "├── "
            line = f"{prefix}{connector}{child.index + 1}"

            if isinstance(child, Cluster):
                line += f"m{child.total}"
                result.append(line)
                new_prefix = prefix + ("    " if is_last else "│   ")
                result.extend(self._tree_lines(child, new_prefix))
            else:
                line += f"{child.type}{child.value_raw}"
                result.append(line)

        return result

    def print_tree(self, node=None, prefix="", stdout=True) -> Optional[str]:
        """Print or return a visual representation of the tree.

        :param node: Starting node (defaults to root)
        :param prefix: Prefix for tree indentation
        :param stdout: If True, prints the tree to stdout
        :return: String representation of the tree if stdout is False,
            None otherwise
        """
        result = []
        if node is None:
            node = self.root
            result.append(f"{node.index + 1}m{node.total}")

        if isinstance(node, Cluster):
            result.extend(self._tree_lines(node, prefix))

        tree_str = "\n".join(result)

        if stdout:
            print(tree_str)
        else:
            return tree_str
