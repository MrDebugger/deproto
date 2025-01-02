import unittest

from deproto import Protobuf


class TestProtobuf(unittest.TestCase):
    def setUp(self):
        self.test_pb = "!1m3!1s2024!2i42!3stest"
        self.decoder = Protobuf(self.test_pb)

    def test_decode(self):
        cluster = self.decoder.decode()
        self.assertEqual(len(cluster[1]), 3)
        self.assertEqual(cluster[1][1].value, "2024")
        self.assertEqual(cluster[1][2].value, 42)
        self.assertEqual(cluster[1][3].value, "test")

    def test_encode(self):
        self.decoder.decode()
        encoded = self.decoder.encode()
        self.assertEqual(encoded, self.test_pb)

    def test_value_modification(self):
        cluster = self.decoder.decode()
        cluster[1][1].change("2025")
        self.assertEqual(cluster[1][1].value, "2025")

    def test_reset(self):
        self.decoder.decode()
        self.decoder.root[1][1].change("2025")
        self.decoder.reset()
        self.assertEqual(self.decoder.root[1][1].value, "2024")


if __name__ == "__main__":
    unittest.main()
