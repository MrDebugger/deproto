from deproto import Protobuf
from deproto.cluster import Cluster
from deproto.node import Node
from deproto.types import BoolType, EnumType, IntType, StringType

pb = """
!1m7!1szero_x!3s!6m4!4m1!1e1!4m1!1e1!2m2!1i10!2s!5m2!1sreference_id!7e81!8m5!1b1!2b1!3b1!5b1!7b1!11m6!1e3!2e1!3sen!4sUS!6m1!1i2!13m1!1e1
"""

decoder = Protobuf(pb.strip())
cluster = decoder.decode()
decoder.print_tree()

# Create root cluster
root = Cluster(1)

# Adding nodes automatically updates totals up the chain
root.add(
    1,
    [
        Node(1, "zero_x", StringType()),
        Cluster(6, [Cluster(4, [Node(1, 1, EnumType())])]),
    ],
)

root.add(
    2,
    [
        Node(1, 10, IntType()),
        Node(1, "", StringType()),  # cursor
    ],
)

root.add(
    5,
    [
        Node(1, "reference_id", StringType()),
        Node(7, 81, EnumType()),
    ],
)

root.add(
    8,
    [
        Node(1, True, BoolType()),
        Node(2, True, BoolType()),
        Node(3, True, BoolType()),
        Node(5, True, BoolType()),
        Node(7, True, BoolType()),
    ],
)

root.add(
    11,
    [
        Node(1, 3, EnumType()),
        Node(2, 1, EnumType()),
        Node(3, "en", StringType()),
        Node(4, "US", StringType()),
    ],
)

root.add(13, [Node(1, 1, EnumType())])

# Deleting nodes automatically updates totals
root.delete(11)  # Totals are automatically decremented

decoder.print_tree(root)
print(root.encode())
