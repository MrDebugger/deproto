# deproto

<div align="center">
  <img src="assets/icons/DEPROTO.gif" alt="deproto logo" width="200"/>
</div>

<h4 align="center">A Python package for Google Maps protobuf format</h4>

<p align="center">
  <a href="https://pypi.org/project/deproto/">
    <img src="https://img.shields.io/pypi/v/deproto.svg" alt="PyPI version"/>
  </a>
  <a href="https://pypi.org/project/deproto/">
    <img src="https://img.shields.io/pypi/pyversions/deproto.svg" alt="Python versions"/>
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/github/license/MrDebugger/deproto.svg" alt="License"/>
  </a>
  <a href="https://github.com/MrDebugger/deproto/stargazers">
    <img src="https://img.shields.io/github/stars/MrDebugger/deproto.svg" alt="GitHub stars"/>
  </a>
  <a href="https://github.com/MrDebugger/deproto/network">
    <img src="https://img.shields.io/github/forks/MrDebugger/deproto.svg" alt="GitHub forks"/>
  </a>
  <a href="https://github.com/MrDebugger/deproto/issues">
    <img src="https://img.shields.io/github/issues/MrDebugger/deproto.svg" alt="GitHub issues"/>
  </a>
  <a href="https://pepy.tech/project/deproto">
    <img src="https://pepy.tech/badge/deproto" alt="Downloads"/>
  </a>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#building-protobuf-structures">Documentation</a> •
  <a href="#advanced-usage">Advanced</a> •
  <a href="#testing">Testing</a>
</p>

A Python package for decoding, manipulating, and encoding Google Maps protobuf format strings. This library provides an intuitive way to work with protobuf structures commonly found in Google Maps URLs and data.

## Features

- Decode Google Maps protobuf strings into a tree structure
- Create and modify protobuf structures using multiple approaches
- Automatic type detection and handling
- Parent-child relationship tracking
- Automatic total count management in clusters
- Tree visualization for debugging
- Support for various data types

## Installation

Install using pip:

```bash
pip install -U deproto
```

## Quick Start

```python
from deproto import Protobuf

# Example protobuf string from Google Maps
pb_string = "!1m3!1s2024!2i42!3stest"

# Create decoder instance
decoder = Protobuf(pb_string)

# Decode the string into a tree structure
cluster = decoder.decode()

# Print the tree structure
decoder.print_tree()

# Make changes to values
cluster[0][0].change("2025")

# Encode back to protobuf format
encoded = decoder.encode()
```

## Building Protobuf Structures

There are multiple ways to build protobuf structures:

### 1. Direct Construction

```python
from deproto.cluster import Cluster
from deproto.node import Node
from deproto.types import StringType, IntType

# Create a structure directly
root = Cluster(1, [
    Node(1, "hello", StringType()),
    Cluster(2, [
        Node(1, 42, IntType())
    ])
])
```

### 2. Using add() with Tuples

```python
root = Cluster(1)
root.add(1, [(1, "hello"), (2, 42)])  # Types auto-detected
```

### 3. Using add() with Nodes

```python
root = Cluster(1)
root.add(1, [
    Node(1, "hello", StringType()),
    Node(2, 42, IntType())
])
```

### 4. Mixed Approach

```python
root = Cluster(1)
root.add(1, Node(1, "hello", StringType()))
root.add(2, [(1, 42)])  # Type auto-detected
```

## Complex Structures

You can build complex nested structures:

```python
root = Cluster(1, [
    Node(1, "metadata", StringType()),
    Cluster(2, [
        Node(1, 42, IntType()),
        Node(2, True, BoolType()),
        Cluster(3, [
            Node(1, "nested", StringType()),
            Node(2, 3.14, IntType())
        ])
    ]),
    Node(3, "end", StringType())
])
```

## Tree Visualization

The `print_tree()` method provides a clear visualization of the protobuf structure:

```
1m3
├── 1s2024
├── 2i42
└── 3stest
```

## Supported Data Types

| Type | Description | Example |
|------|-------------|---------|
| `B` | Bytes | Binary data |
| `b` | Boolean | True/False |
| `d` | Double | 3.14159 |
| `e` | Enum | 1, 2, 3 |
| `f` | Float | 3.14 |
| `i` | Int32/64 | 42 |
| `s` | String | "hello" |
| `x` | Fixed32 | 12345 |
| `y` | Fixed64 | 123456789 |
| `z` | Base64String | Encoded string |

## Advanced Usage

### Parent-Child Relationships

The library maintains parent-child relationships automatically:

```python
root = Cluster(1)
child = Cluster(2, [
    Node(1, True, BoolType())
])
root.append(child)

assert child.parent == root
assert child[0].parent == child
```

### Automatic Total Management

Cluster totals are managed automatically when adding or removing nodes. The total includes both nodes and clusters:

```python
root = Cluster(1)

# Adding nodes in a cluster
root.add(1, [  # This creates: Cluster(1, [Node(1, "test"), Node(2, 42)])
    Node(1, "test", StringType()),
    Node(2, 42, IntType())
])
print(root.total)  # 3 (1 for the cluster + 2 for the nodes)

# Adding a single node
root.add(2, Node(3, "direct", StringType()))
print(root.total)  # 4 (previous 3 + 1 for the new node)

# Complex structure
root.add(3, [  # Creates nested clusters
    Node(1, "hello", StringType()),
    Cluster(2, [
        Node(1, 42, IntType())
    ])
])
print(root.total)  # 8 (previous 4 + 1 for new cluster + 1 for Node("hello") 
                   #    + 1 for inner Cluster + 1 for Node(42))

# Removing a cluster removes its total contribution
root.delete(3)  # Removes the complex structure
print(root.total)  # 4 (back to previous state)
```

Note: When using `add()` with a list, it creates a new cluster containing those items, which adds to the total count.

### Special Character Handling

String values with special characters are handled automatically:

```python
node = Node(1, "test!*", StringType())
print(node.value_raw)  # "test*21*2A"
print(node.value)      # "test!*"
```

## Testing

Run the test suite:

```bash
# Using pytest
pytest tests/

# With coverage
coverage run -m pytest tests/
coverage report
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Ijaz Ur Rahim ([ijazurrahim.com](https://ijazurrahim.com) | [@MrDebugger](https://github.com/MrDebugger))

## Current Version

**0.2.0** - See [CHANGELOG.md](CHANGELOG.md) for version history and details.
