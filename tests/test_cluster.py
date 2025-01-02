import unittest

from deproto.cluster import Cluster
from deproto.node import Node
from deproto.types import BoolType, IntType, StringType


class TestCluster(unittest.TestCase):
    def setUp(self):
        self.cluster = Cluster(1)
        self.node1 = Node(1, "test", StringType())
        self.node2 = Node(2, 42, IntType())

    def test_append(self):
        self.cluster.append(self.node1)
        self.assertEqual(len(self.cluster), 1)
        self.assertEqual(self.cluster.total, 1)

    def test_nested_cluster(self):
        nested = Cluster(2, [Node(1, True, BoolType())])
        self.cluster.append(nested)
        self.assertEqual(self.cluster.total, 2)  # nested cluster + its node

    def test_delete(self):
        self.cluster.append(self.node1)
        self.cluster.append(self.node2)
        deleted = self.cluster.delete(1)
        self.assertEqual(deleted, self.node1)
        self.assertEqual(self.cluster.total, 1)

    def test_parent_child_relationship(self):
        nested = Cluster(2, [Node(1, True, BoolType())])
        self.cluster.append(nested)
        self.assertEqual(nested.parent, self.cluster)
        self.assertEqual(nested[1].parent, nested)

    def test_add_method_variations(self):
        # Test tuple format cluster[node]
        self.cluster.add(1, [(1, "test")])
        self.assertEqual(self.cluster.total, 2)

        # Test direct node
        self.cluster.add(2, Node(1, 42, IntType()))
        self.assertEqual(self.cluster.total, 3)

        # Test nested structure cluster[node, node]
        nodes = [(1, True, BoolType()), (2, "nested", StringType())]
        self.cluster.add(3, nodes)
        self.assertEqual(self.cluster.total, 6)

    def test_encode(self):
        self.cluster.append(self.node1)
        nested = Cluster(2, [Node(1, 42, IntType())])
        self.cluster.append(nested)
        encoded = self.cluster.encode()
        self.assertIn("!1stest", encoded)
        self.assertIn("!2m1!1i42", encoded)


if __name__ == "__main__":
    unittest.main()
