# deproto

<div align="center">
  <img src="https://raw.githubusercontent.com/MrDebugger/deproto/main/assets/icons/DEPROTO.gif" alt="deproto logo" width="200"/>
</div>

<h4 align="center">A Python package for Google Maps protobuf format</h4>

<p align="center">
  <a href="https://pypi.org/project/deproto/">
    <img src="https://img.shields.io/pypi/v/deproto.svg" alt="PyPI version"/>
  </a>
  <a href="https://pypi.org/project/deproto/">
    <img src="https://img.shields.io/pypi/pyversions/deproto.svg" alt="Python versions"/>
  </a>
  <a href="https://github.com/MrDebugger/deproto/blob/main/LICENSE">
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
  <a href="https://github.com/MrDebugger/deproto#features">Features</a> •
  <a href="https://github.com/MrDebugger/deproto#installation">Installation</a> •
  <a href="https://github.com/MrDebugger/deproto#quick-start">Quick Start</a> •
  <a href="https://github.com/MrDebugger/deproto#building-protobuf-structures">Documentation</a> •
  <a href="https://github.com/MrDebugger/deproto#advanced-usage">Advanced</a> •
  <a href="https://github.com/MrDebugger/deproto#testing">Testing</a>
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
cluster[1][1].change("2025")

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

## Tree Operations

### Finding and Replacing Nodes

You can find and replace nodes in the tree structure:

```python
from deproto import Protobuf, Cluster, Node
from deproto.types import StringType, IntType

# Create a sample cluster
cluster = Cluster(1, [
    Node(1, "hello", StringType()),
    Node(2, 42, IntType()),
    Node(3, "world", StringType())
])

# Find a node by index
node = cluster.find(2)  # Returns node with value 42

# Replace a node
new_node = Node(2, 100, IntType())
old_node = cluster.replace(2, new_node)
```

### JSON Serialization

The tree structure can be serialized into a simple list representation:

```python
from deproto import Protobuf, Cluster, Node
from deproto.types import StringType, IntType

# Create a simple structure
cluster = Cluster(1, [
    Node(1, "test", StringType()),
    Node(2, 42, IntType())
])

# Convert to list format
json_data = cluster.to_json()
print(json_data)  # Output: ["test", 42]

# Create a nested structure
nested = Cluster(1, [
    Node(1, "outer", StringType()),
    Cluster(2, [
        Node(1, "inner", StringType())
    ])
])

# Nested structures maintain hierarchy
nested_json = nested.to_json()
print(nested_json)  # Output: ["outer", ["inner"]]
```

The `to_json()` method converts:
- Simple nodes into their values
- Clusters into lists of their children's values
- Maintains the nested structure of the tree

## Tree Visualization

The `print_tree()` method provides a clear visualization of the protobuf structure:

For example, given this protobuf string:

```
!1shello!6m4!4m1!1e1!5m1!1e1!2m2!1i42!2sworld!5m2!1sgreeting!7e1!8m5!1b1!2b1!3b1!5b1!7b1!11m4!1e1!2e2!3sen!4sGB!13m1!1e1
```

The tree visualization shows:

```
1m25                      # Root cluster: index=1, total=25 clusters/nodes
├── 1shello               # String node: "hello"
├── 6m4                   # Cluster: index=6, total=4
│   ├── 4m1               # Nested cluster: index=4, total=1
│   │   └── 1e1           # Enum node: value=1
│   └── 5m1               # Another cluster: index=5, total=1
│       └── 1e1           # Enum node: value=1
├── 2m2                   # Cluster: index=2, total=2
│   ├── 1i42              # Int node: value=42 (answer to everything)
│   └── 2sworld           # String node: "world"
├── 5m2                   # Cluster: index=5, total=2
│   ├── 1sgreeting        # String node: "greeting"
│   └── 7e1               # Enum node: value=1
├── 8m5                   # Cluster: index=8, total=5
│   ├── 1b1               # Bool node: true
│   ├── 2b1               # Bool node: true
│   ├── 3b1               # Bool node: true
│   ├── 5b1               # Bool node: true
│   └── 7b1               # Bool node: true
├── 11m4                  # Cluster: index=11, total=4
│   ├── 1e1               # Enum node: value=1
│   ├── 2e2               # Enum node: value=2
│   ├── 3sen              # String node: "en"
│   └── 4sGB              # String node: "GB"
└── 13m1                  # Cluster: index=13, total=1
    └── 1e1               # Enum node: value=1
```

Understanding the numbers:
- First number is the index (1-based)
- `m` indicates a cluster, followed by total count
- Letters indicate type: `s`=string, `i`=int, `e`=enum, `b`=bool

Total count includes:
- Direct children nodes
- Nested clusters
- Children of nested clusters

For example, in `6m4`:
- Has 2 direct children (4m1 clusters)
- Each 4m1 cluster has 1 child (1e1 nodes)
- Total = 2 clusters + 2 nodes = 4

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
assert child[1].parent == child
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

This project is licensed under the MIT License - see the [LICENSE](https://github.com/MrDebugger/deproto/blob/main/LICENSE) file for details.

## Author

Ijaz Ur Rahim ([ijazurrahim.com](https://ijazurrahim.com) | [@MrDebugger](https://github.com/MrDebugger))

## Current Version

**0.2.3** - See [CHANGELOG.md](https://github.com/MrDebugger/deproto/blob/main/CHANGELOG.md) for version history and details.
