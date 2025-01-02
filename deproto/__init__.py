"""deproto.

A decoder for Google Maps protobuf format.

This package provides tools to decode, manipulate, and encode protobuf
structures commonly found in Google Maps data.

Main Components:
    - Protobuf: Main decoder/encoder class
    - Cluster: Container for nodes and nested clusters
    - Node: Individual data node
    - Types: Various data type handlers
"""

from .cluster import Cluster
from .node import Node
from .protobuf import Protobuf
from .types import DataTypeFactory

__all__ = ["Protobuf", "Cluster", "Node", "DataTypeFactory"]

__version__ = "0.2.5"
