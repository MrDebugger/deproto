import io
import unittest
from unittest import mock

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


class TestPrintTreeConsoleEncoding(unittest.TestCase):
    """print_tree() must not crash on consoles that lack box-drawing glyphs.

    Default Windows consoles (PowerShell/cmd) use cp1252 for stdout, which
    cannot encode the Unicode connectors used in the tree.
    """

    PB_STRING = "!1m4!1stest!2m1!1i42!3send"
    EXPECTED_TREE = (
        "1m5\n"
        "└── 1m4\n"
        "    ├── 1stest\n"
        "    ├── 2m1\n"
        "    │   └── 1i42\n"
        "    └── 3send"
    )

    def setUp(self):
        self.pb = Protobuf(self.PB_STRING)
        self.pb.decode()

    @staticmethod
    def _make_stdout(encoding):
        buffer = io.BytesIO()
        stream = io.TextIOWrapper(buffer, encoding=encoding, newline="\n")
        return buffer, stream

    def _print_to(self, encoding, pb=None):
        pb = pb or self.pb
        buffer, stream = self._make_stdout(encoding)
        with mock.patch("sys.stdout", stream):
            returned = pb.print_tree()
        stream.flush()
        return returned, buffer.getvalue().decode(encoding)

    def test_cp1252_stdout_does_not_crash(self):
        returned, printed = self._print_to("cp1252")

        # Returned value keeps the Unicode box-drawing characters.
        self.assertEqual(returned, self.EXPECTED_TREE)
        # Printed output falls back to ASCII connectors.
        self.assertEqual(
            printed,
            "1m5\n"
            "`-- 1m4\n"
            "    |-- 1stest\n"
            "    |-- 2m1\n"
            "    |   `-- 1i42\n"
            "    `-- 3send\n",
        )

    def test_utf8_stdout_prints_unicode_tree(self):
        returned, printed = self._print_to("utf-8")

        self.assertEqual(returned, self.EXPECTED_TREE)
        self.assertEqual(printed, self.EXPECTED_TREE + "\n")

    def test_stdout_without_encoding_prints_unicode_tree(self):
        stream = io.StringIO()  # ``encoding`` is None
        self.assertIsNone(stream.encoding)
        with mock.patch("sys.stdout", stream):
            returned = self.pb.print_tree()

        self.assertEqual(returned, self.EXPECTED_TREE)
        self.assertEqual(stream.getvalue(), self.EXPECTED_TREE + "\n")

    def test_unencodable_values_are_replaced_not_raised(self):
        pb = Protobuf("!1m1!1s日本")
        pb.decode()

        returned, printed = self._print_to("cp1252", pb)

        self.assertEqual(returned, "1m2\n└── 1m1\n    └── 1s日本")
        self.assertEqual(printed, "1m2\n`-- 1m1\n    `-- 1s??\n")

    def test_stdout_false_does_not_print(self):
        buffer, stream = self._make_stdout("cp1252")
        with mock.patch("sys.stdout", stream):
            returned = self.pb.print_tree(stdout=False)
        stream.flush()

        self.assertEqual(returned, self.EXPECTED_TREE)
        self.assertEqual(buffer.getvalue(), b"")


if __name__ == "__main__":
    unittest.main()
