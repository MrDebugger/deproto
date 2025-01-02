import unittest

from deproto import Cluster, Node, Protobuf
from deproto.types import IntType, StringType


class TestTreeOperations(unittest.TestCase):
    def setUp(self):
        self.cluster = Cluster(
            1,
            [
                Node(1, "test", StringType()),
                Node(2, 42, IntType()),
                Node(3, "end", StringType()),
            ],
        )

    def test_node_finding(self):
        """Test node finding operations"""
        # Test successful find
        node = self.cluster.find(2)
        self.assertEqual(node.value, 42)

        # Test find with invalid index
        with self.assertRaises(IndexError):
            self.cluster[5]

        # Test find with invalid index
        with self.assertRaises(IndexError):
            self.cluster.find(5, _raise=True)

    def test_node_replacement(self):
        """Test node replacement operations"""
        new_node = Node(2, 100, IntType())
        old_node = self.cluster.replace(2, new_node)

        self.assertEqual(old_node.value, 42)
        self.assertEqual(self.cluster.find(2).value, 100)

    def test_node_indexing(self):
        """Test zero-based indexing operations"""
        node = self.cluster.at(1)  # Should get second node
        self.assertEqual(node.value, 42)


class TestTreeSerialization(unittest.TestCase):
    def setUp(self):
        self.nested_cluster = Cluster(
            1,
            [
                Node(1, "outer", StringType()),
                Cluster(2, [Node(1, "inner", StringType())]),
            ],
        )

    def test_json_serialization(self):
        """Test JSON serialization of tree structures"""
        # Test basic structure
        simple_cluster = Cluster(
            1, [Node(1, "test", StringType()), Node(2, 42, IntType())]
        )
        json_data = simple_cluster.to_json()
        self.assertEqual(json_data, ["test", 42])

        # Test nested structure
        nested_json = self.nested_cluster.to_json()
        self.assertEqual(nested_json, ["outer", ["inner"]])

    def test_tree_visualization(self):
        """Test tree visualization output"""
        pb = Protobuf("!1m2!1stest!2i42")
        pb.decode()

        # Test string output
        tree_str = pb.print_tree(stdout=False)
        self.assertIsInstance(tree_str, str)
        self.assertIn("1m2", tree_str)
        self.assertIn("stest", tree_str)
        self.assertIn("i42", tree_str)


if __name__ == "__main__":
    unittest.main()
