from deproto import Protobuf
from deproto.cluster import Cluster
from deproto.node import Node
from deproto.types import DataTypeFactory, StringType


def demonstrate_cluster_manipulation():
    print("Cluster Manipulation Example:")
    print("----------------------------")

    # Create a new cluster
    cluster = Cluster(1)

    # Add nodes
    cluster.append(Node(1, "value1", StringType()))
    cluster.append(Node(3, "value2", StringType()))

    # Insert at specific position
    cluster.insert(2, Node(2, "inserted", StringType()))

    # Print the cluster structure
    print(f"Cluster: {cluster}")
    print(f"Total nodes: {len(cluster)}")


def demonstrate_data_types():
    print("\nData Types Example:")
    print("------------------")

    # Get different type handlers
    string_type = DataTypeFactory.get_type("s")
    int_type = DataTypeFactory.get_type("i")
    float_type = DataTypeFactory.get_type("f")

    # Create nodes with different types
    string_node = Node(1, "test", string_type())
    int_node = Node(2, "42", int_type())
    float_node = Node(3, "3.14", float_type())

    print(f"String node: {string_node}")
    print(f"Integer node: {int_node}")
    print(f"Float node: {float_node}")

    # Auto-detect type
    value_type = DataTypeFactory.get_type_by_value("some string")
    print(f"Auto-detected type for string: {value_type.type}")


def demonstrate_state_management():
    print("\nState Management Example:")
    print("-----------------------")

    pb_string = "!1m3!1s2024!2i42!3stest"
    decoder = Protobuf(pb_string)

    # Initial decode
    cluster = decoder.decode()
    print("Original structure:")
    decoder.print_tree()

    # Make some changes
    cluster[1][1].change("2025")
    print("\nModified structure:")
    decoder.print_tree()

    # Reset to original state
    decoder.reset()
    print("\nReset structure:")
    decoder.print_tree()


def main():
    demonstrate_cluster_manipulation()
    demonstrate_data_types()
    demonstrate_state_management()


if __name__ == "__main__":
    main()
