"""Protobuf module.

This module provides the Protobuf class for decoding and encoding Google Maps
protobuf format strings. The format consists of nodes and clusters arranged in
a hierarchical structure.

The protobuf format uses a simple encoding scheme:
- Each node starts with '!' followed by an index number
- A single character indicates the data type (e.g. 's' => string, 'f' => float)
- The remaining characters contain the encoded value
- Clusters are indicated by 'm' type and contain a count of nested nodes

Example:
    !1s5Hello!2f3.14!3m2!4b1!5sWorld

Main Components:
    - Protobuf: Main decoder/encoder class
    - split(): Splits protobuf string into node tuples
    - expand(): Expands node strings into components
    - to_cluster(): Converts nodes to hierarchical cluster structure
"""

import re
import sys
from typing import List, Optional, Tuple

from deproto.cluster import Cluster
from deproto.node import Node
from deproto.types import DataTypeFactory

# Tree connectors as (branch, last branch, vertical continuation).
UNICODE_CONNECTORS: Tuple[str, str, str] = ("├── ", "└── ", "│   ")
ASCII_CONNECTORS: Tuple[str, str, str] = ("|-- ", "`-- ", "|   ")


def _can_encode(text: str, encoding: Optional[str]) -> bool:
    """Check whether ``text`` can be encoded with ``encoding``.

    :param text: Text to check
    :param encoding: Target encoding; ``None`` means the stream accepts
        any ``str`` (e.g. ``io.StringIO``)
    :return: True if the text can be encoded, False otherwise
    """
    if not encoding:
        return True
    try:
        text.encode(encoding)
    except (UnicodeEncodeError, LookupError):
        return False
    return True


def _replace_unencodable(text: str, encoding: str) -> str:
    """Replace characters that ``encoding`` cannot represent with '?'.

    :param text: Text to sanitize
    :param encoding: Target encoding; unknown encodings fall back to ASCII
    :return: Text that can be safely encoded with ``encoding``
    """
    try:
        return text.encode(encoding, "replace").decode(encoding)
    except LookupError:
        return text.encode("ascii", "replace").decode("ascii")


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
        pb_split = self.pb_string.split("!")
        self.nodes = [self.expand(node) for node in pb_split if node]
        self.original_nodes = self.nodes.copy()

    def expand(self, node: str) -> Tuple[str, str, str]:
        """Expand a protobuf node string into components."""
        matches = re.match(r"(\d+)([a-zA-Z])(.*)", node)
        if not matches or len(matches.groups()) != 3:
            raise ValueError(f"Invalid protobuf-encoded string: {node}")
        return matches.groups()

    def to_cluster(self, nodes: List[Tuple[str, str, str]]) -> Cluster:
        """Convert nodes list to a cluster structure."""
        _id, kind, value = nodes.pop(0)
        cluster = Cluster(int(_id))
        needed_nodes = [nodes.pop(0) for _ in range(int(value))]

        while needed_nodes:
            node = needed_nodes[0]
            if node[1] == "m":
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
            if node[1] == "m":
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

    def _tree_lines(
        self,
        node: Cluster,
        prefix: str,
        connectors: Tuple[str, str, str] = UNICODE_CONNECTORS,
    ) -> List[str]:
        """Generate tree lines recursively.

        :param node: Cluster node to process
        :param prefix: Current indentation prefix
        :param connectors: (branch, last branch, vertical) connector strings
        :return: List of formatted tree lines
        """
        branch, last_branch, vertical = connectors
        result = []
        for i, child in enumerate(node.nodes):
            is_last = i == len(node.nodes) - 1
            connector = last_branch if is_last else branch
            line = f"{prefix}{connector}{child.index + 1}"

            if isinstance(child, Cluster):
                line += f"m{child.total}"
                result.append(line)
                new_prefix = prefix + ("    " if is_last else vertical)
                result.extend(self._tree_lines(child, new_prefix, connectors))
            else:
                line += f"{child.type}{child.value_raw}"
                result.append(line)

        return result

    def _format_tree(
        self,
        cluster: Optional[Cluster],
        prefix: str,
        connectors: Tuple[str, str, str],
    ) -> str:
        """Build the tree string using the given connectors.

        :param cluster: Cluster to render, or None for the root
        :param prefix: Initial indentation prefix
        :param connectors: (branch, last branch, vertical) connector strings
        :return: Tree representation as a string
        """
        result = []
        if cluster is None:
            cluster = self.root
            result.append(f"{cluster.index + 1}m{cluster.total}")

        if isinstance(cluster, Cluster):
            result.extend(self._tree_lines(cluster, prefix, connectors))

        return "\n".join(result)

    def print_tree(
        self,
        cluster: Optional[Cluster] = None,
        prefix: str = "",
        stdout: bool = True,
    ) -> Optional[str]:
        """Print or return a visual representation of the tree.

        The returned string always uses Unicode box-drawing connectors. When
        printing, if ``sys.stdout`` cannot encode them (e.g. a cp1252 Windows
        console), ASCII connectors are printed instead, and any remaining
        unencodable characters are replaced rather than raising.

        :param cluster: Cluster to render, or None for the root
        :param prefix: Initial indentation prefix
        :param stdout: Whether to print the tree to ``sys.stdout``
        :return: Tree representation with Unicode connectors
        """
        tree_str = self._format_tree(cluster, prefix, UNICODE_CONNECTORS)

        if stdout:
            encoding = getattr(sys.stdout, "encoding", None)
            output = tree_str
            if not _can_encode(output, encoding):
                output = self._format_tree(cluster, prefix, ASCII_CONNECTORS)
            if not _can_encode(output, encoding):
                output = _replace_unencodable(output, encoding)
            print(output)
        return tree_str
