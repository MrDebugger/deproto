# deproto

A Python package for decoding and manipulating Google Maps protobuf format strings. This library allows you to decode, modify, and re-encode protobuf strings commonly found in Google Maps URLs and data structures.

## Installation

Install using pip:

```bash
pip install deproto
```

## Quick Start

```python
from deproto import Protobuf

# Example protobuf string from Google Maps
pb_string = ('!3m1!1e3!4m12!3m11!1s0x4795cd1c65280cb9:0xad3b34d7340adc02'
             '!5m3!1s2024-12-21!4m1!1i2!8m2!3d49.167174!4d7.22149!9m1!1b1'
             '!16s%2Fg%2F1tfr93pp')

# Create decoder instance
decoder = Protobuf(pb_string)

# Decode the string into a tree structure
cluster = decoder.decode()

# Print the tree structure
decoder.print_tree()

# Make changes to values
cluster[1][0][1][0].change("2025-01-01")

# Encode back to protobuf format
encoded = decoder.encode()
```

## Features

- Decode Google Maps protobuf strings into a tree structure
- Modify the decoded structure
- Encode the structure back to protobuf format
- Print tree visualization of the structure
- Support for various data types (int, float, string, etc.)

### Tree Structure Visualization

The `print_tree()` method provides a clear visualization of the protobuf structure:

```
1m3
├── 3m1
│   └── 1e3
├── 4m12
│   └── 3m11
│       ├── 1s0x4795cd1c65280cb9:0xad3b34d7340adc02
│       ├── 5m3
│       │   └── 1s2024-12-21
│       └── ...
```

### Supported Data Types

- Bytes (`B`)
- Boolean (`b`)
- Double (`d`)
- Enum (`e`)
- Float (`f`)
- Fixed32 (`x`)
- Fixed64 (`y`)
- Int32/64 (`i`)
- SFixed32 (`g`)
- SFixed64 (`h`)
- SInt32 (`n`)
- SInt64 (`o`)
- String (`s`)
- UInt32 (`u`)
- UInt64 (`v`)
- Base64String (`z`)

### Tree Manipulation

```python
# Access nodes using index
node = cluster[0][1]

# Change values
node.change("new_value")

# Delete nodes
cluster[1][0].delete(5)

# Insert nodes
from deproto import Node
from deproto.data_types import IntType
cluster.insert(4, Node(4, '42', IntType()))
```

### State Management

```python
# Reset to original state
decoder.reset()
```

## Advanced Usage

### Working with Clusters

Clusters are collections of nodes that can be manipulated as a group:

```python
from deproto import Cluster, Node
from deproto.data_types import StringType

# Create a new cluster
cluster = Cluster(1, 2)

# Add nodes
cluster.append(Node(1, "value1", StringType()))
cluster.append(Node(3, "value2", StringType()))

# Insert at specific position
cluster.insert(2, Node(2, "inserted", StringType()))
```

### Custom Data Type Handling

The package includes a `DataTypeFactory` for handling various protobuf data types:

```python
from deproto.data_types import DataTypeFactory

# Get type handler
string_type = DataTypeFactory.get_type('s')  # StringType
int_type = DataTypeFactory.get_type('i')     # IntType

# Auto-detect type
value_type = DataTypeFactory.get_type_by_value("some string")  # Returns StringType
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Ijaz Ur Rahim ([ijazurrahim.com](https://ijazurrahim.com) | [@MrDebugger](https://github.com/MrDebugger))
