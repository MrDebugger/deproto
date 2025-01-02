# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.5] - 2025-01-02

### Added
- `to_json()` fills missing nodes in the list
- Enhanced JSON serialization with better handling of:
  - Complex nested structures
  - None values
  - Empty clusters
  - Boolean values

### Fixed
- Improved JSON serialization to maintain correct structure with nested clusters

## [0.2.4] - 2024-12-24

### Added
- `find()` method now has an optional `_raise` parameter to raise an IndexError if the index is not found

### Fixed
- `find()` method now returns `None` if the index is not found

## [0.2.3] - 2024-12-23

### Added
- New Cluster methods:
  - `find()` - Find node or cluster at specific index
  - `replace()` - Replace node at index with new value
  - `at()` - Get node at zero-based index
  - `to_json()` - Convert cluster to JSON-serializable format
- Improved tree visualization with optional string return value
- Added JSON serialization support for clusters
- Exposed additional classes in `__init__.py`: `Cluster`, `Node`, `DataTypeFactory`

### Changed
- Modified `print_tree()` to optionally return string representation
- Improved error handling in index-based operations
- Refactored `delete()` method to use `find()`
- Updated `__getitem__`, `__setitem__`, and `__delitem__` to use 1-based indexing consistently

### Fixed
- Consistent 1-based indexing across all methods
- More descriptive error messages for index operations

## [0.2.1] - 2024-12-22

### Fixed
- Fixed broken logo image on PyPI by using absolute GitHub URLs

## [0.2.0] - 2024-12-22

### Added
- Parent-child relationship tracking in nodes and clusters
- Automatic total calculation in nested structures
- Multiple ways to construct protobuf structures:
  - Direct Node/Cluster construction
  - Using add() with tuples
  - Using add() with nodes
  - Mixed approach with auto-type detection
- Comprehensive examples in examples/
- Enhanced test coverage
- Better type detection and handling
- New logo and badges

### Changed
- Removed requirement for total in Cluster initialization
- Improved cluster construction methods
- Enhanced documentation with more examples
- Restructured project layout
- Updated README with clearer examples

### Fixed
- Total calculation in nested clusters
- Parent reference handling in node deletion
- Type detection for edge cases
- Documentation broken links

## [0.1.2] - 2024-10-21

### Added
- Initial release
- Basic protobuf decoding/encoding
- Tree visualization
- Support for various data types:
  - String, Int, Float, Bool
  - Enum, Bytes, Base64
  - Fixed32/64, SFixed32/64
- Basic documentation
- Simple examples

### Fixed
- String encoding for special characters
- Tree visualization formatting
