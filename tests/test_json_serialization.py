import unittest

from deproto import Cluster, Node, Protobuf
from deproto.types import BoolType, IntType, StringType


class TestJsonSerialization(unittest.TestCase):
    def setUp(self):
        # Create a complex nested structure for testing
        self.nested_cluster = Cluster(
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

    def test_complex_json_serialization(self):
        """Test JSON serialization of complex nested structures"""
        json_data = self.nested_cluster.to_json()

        # Test structure
        self.assertEqual(json_data[0], "config")
        self.assertEqual(json_data[1][0], 42)
        self.assertEqual(json_data[1][1], True)
        self.assertEqual(json_data[1][2][0], "nested")
        self.assertEqual(json_data[1][2][1], 100)
        self.assertEqual(json_data[2], "end")

    def test_protobuf_to_json(self):
        """Test converting protobuf string to JSON"""
        pb_string = "1sstart!2m2!1i42!2b1!3send"
        decoder = Protobuf(pb_string)
        cluster = decoder.decode()
        json_data = cluster.to_json()

        # Test structure from protobuf
        self.assertEqual(json_data[0], "start")
        self.assertEqual(json_data[1][0], 42)
        self.assertEqual(json_data[1][1], True)
        self.assertEqual(json_data[2], "end")

    def test_empty_cluster_json(self):
        """Test JSON serialization of empty cluster"""
        empty_cluster = Cluster(1, [])
        json_data = empty_cluster.to_json()
        self.assertEqual(json_data, [])

    def test_none_values_json(self):
        """Test JSON serialization handles None values correctly"""
        cluster = Cluster(
            1, [Node(1, "", StringType()), Node(2, 42, IntType())]
        )
        json_data = cluster.to_json()
        self.assertEqual(json_data[0], "")
        self.assertEqual(json_data[1], 42)


if __name__ == "__main__":
    unittest.main()
