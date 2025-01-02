import unittest

from deproto.cluster import Cluster
from deproto.node import Node
from deproto.types import BoolType, FloatType, IntType, StringType


class TestNode(unittest.TestCase):
    def setUp(self):
        self.string_node = Node(1, "test", StringType())
        self.int_node = Node(2, 42, IntType())
        self.bool_node = Node(3, True, BoolType())

    def test_value_encoding(self):
        self.assertEqual(self.string_node.value_raw, "test")
        self.assertEqual(self.int_node.value_raw, "42")
        self.assertEqual(self.bool_node.value_raw, "1")

    def test_value_change(self):
        self.string_node.change("new value")
        self.assertEqual(self.string_node.value, "new value")
        self.assertEqual(self.string_node.value_raw, "new value")

    def test_encode(self):
        self.assertEqual(self.string_node.encode(), "!1stest")
        self.assertEqual(self.int_node.encode(), "!2i42")
        self.assertEqual(self.bool_node.encode(), "!3b1")

    def test_parent_relationship(self):
        cluster = Cluster(1)
        self.string_node.set_parent(cluster)
        self.assertEqual(self.string_node.parent, cluster)

    def test_special_characters(self):
        node = Node(1, "test!*", StringType())
        self.assertIn("*21", node.value_raw)
        self.assertIn("*2A", node.value_raw)

    def test_type_conversion(self):
        float_node = Node(1, 3.14, FloatType())
        self.assertEqual(float_node.value, 3.14)
        float_node.change(2.718)
        self.assertEqual(float_node.value, 2.718)


if __name__ == "__main__":
    unittest.main()
