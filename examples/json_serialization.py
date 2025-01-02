from deproto import Cluster, Node, Protobuf
from deproto.types import BoolType, IntType, StringType


def demonstrate_json_serialization():
    print("JSON Serialization Examples")
    print("=========================")

    # Create a complex nested structure
    root = Cluster(
        1,
        [
            Node(1, "config", StringType()),
            Cluster(
                2,
                [
                    Node(1, 42, IntType()),
                    Node(2, True, BoolType()),
                    Cluster(
                        3,
                        [
                            Node(1, "nested", StringType()),
                            Node(2, 100, IntType()),
                        ],
                    ),
                ],
            ),
            Node(3, "end", StringType()),
        ],
    )

    # Convert to JSON and show the structure
    json_data = root.to_json()
    print("\nFull structure as JSON:")
    print(json_data)

    # Access nested values
    print("\nAccessing nested values:")
    print(f"First value: {json_data[0]}")  # "config"
    print(f"Nested boolean: {json_data[1][1]}")  # True
    print(f"Deeply nested string: {json_data[1][2][0]}")  # "nested"

    # Create from protobuf string and convert to JSON
    print("\nFrom protobuf string to JSON:")
    pb_string = "!1m5!1sstart!2m2!1i42!2b1!3send"
    decoder = Protobuf(pb_string)
    cluster = decoder.decode()
    print(cluster.to_json())


if __name__ == "__main__":
    demonstrate_json_serialization()
