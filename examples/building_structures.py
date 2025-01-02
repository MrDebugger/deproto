from deproto import Protobuf
from deproto.cluster import Cluster
from deproto.node import Node
from deproto.types import BoolType, FloatType, IntType, StringType


def demonstrate_building_methods():
    print("Different Ways to Build Protobuf Structures")
    print("=========================================")

    # Method 1: Direct Node/Cluster Construction
    print("\n1. Direct Construction:")
    root = Cluster(
        1,
        [
            Node(1, "hello", StringType()),
            Cluster(2, [Node(1, 42, IntType())]),
        ],
    )
    Protobuf("").print_tree(root)

    # Method 2: Using add() with tuples
    print("\n2. Using add() with tuples:")
    root = Cluster(1)
    root.add(1, [(1, "hello"), (2, 42)])
    Protobuf("").print_tree(root)

    # Method 3: Using add() with nodes
    print("\n3. Using add() with nodes:")
    root = Cluster(1)
    root.add(1, [Node(1, "hello", StringType()), Node(2, 42, IntType())])
    Protobuf("").print_tree(root)

    # Method 4: Mixed approach
    print("\n4. Mixed approach:")
    root = Cluster(1)
    root.add(1, Node(1, "hello", StringType()))
    root.add(2, [(1, 42)])
    Protobuf("").print_tree(root)


def demonstrate_complex_structure():
    print("\nBuilding Complex Structure")
    print("=========================")

    # Building a more complex structure
    root = Cluster(
        1,
        [
            Node(1, "metadata", StringType()),
            Cluster(
                2,
                [
                    Node(1, 42, IntType()),
                    Node(2, True, BoolType()),
                    Cluster(
                        3,
                        [
                            Node(1, "nested", StringType()),
                            Node(2, 3.14, FloatType()),
                        ],
                    ),
                ],
            ),
            Node(3, "end", StringType()),
        ],
    )

    Protobuf("").print_tree(root)
    print("\nEncoded:", root.encode())


def main():
    demonstrate_building_methods()
    demonstrate_complex_structure()


if __name__ == "__main__":
    main()
