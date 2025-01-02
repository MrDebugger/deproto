from deproto import Cluster, Node, Protobuf
from deproto.types import IntType, StringType


def demonstrate_node_operations():
    print("Node Finding and Replacement Operations")
    print("====================================")

    # Create a sample cluster
    cluster = Cluster(
        1,
        [
            Node(1, "hello", StringType()),
            Node(2, 42, IntType()),
            Node(3, "world", StringType()),
        ],
    )

    # Find a node
    try:
        node = cluster.find(2)
        # Should print node with value 42
        print(f"\nFound node at index 2: {node}")
    except IndexError as e:
        print(f"Error: {e}")

    # Replace a node
    new_node = Node(2, 100, IntType())
    old_node = cluster.replace(2, new_node)
    print("\nReplaced node:")
    print(f"Old: {old_node}")
    print(f"New: {new_node}")

    # Demonstrate tree visualization
    print("\nTree Structure:")
    pb = Protobuf("")
    pb.print_tree(cluster)


def demonstrate_tree_serialization():
    print("\nTree Serialization Examples")
    print("=========================")

    # Create a nested structure
    root = Cluster(
        1,
        [
            Node(1, "metadata", StringType()),
            Cluster(
                2,
                [Node(1, 42, IntType()), Node(2, "nested", StringType())],
            ),
            Node(3, "end", StringType()),
        ],
    )

    # Show JSON representation
    json_data = root.to_json()
    print("\nJSON representation:")
    print(json_data)

    # Show tree visualization as string
    pb = Protobuf("")
    tree_str = pb.print_tree(root, stdout=False)
    print("\nTree visualization:")
    print(tree_str)


def main():
    demonstrate_node_operations()
    demonstrate_tree_serialization()


if __name__ == "__main__":
    main()
