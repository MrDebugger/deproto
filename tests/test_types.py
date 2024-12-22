import unittest
from deproto.types import (
    DataTypeFactory, StringType, IntType, FloatType,
    BoolType, Base64StringType
)


class TestDataTypes(unittest.TestCase):
    def test_string_type(self):
        string_type = StringType()
        test_value = "Hello!*World"
        encoded_type, encoded_value = string_type.encode(test_value)
        self.assertEqual(encoded_type, 's')
        self.assertEqual(string_type.decode(encoded_value), test_value)

    def test_int_type(self):
        int_type = IntType()
        test_value = 42
        encoded_type, encoded_value = int_type.encode(test_value)
        self.assertEqual(encoded_type, 'i')
        self.assertEqual(int_type.decode(encoded_value), test_value)

    def test_bool_type(self):
        bool_type = BoolType()
        test_value = True
        encoded_type, encoded_value = bool_type.encode(test_value)
        self.assertEqual(encoded_type, 'b')
        self.assertEqual(bool_type.decode(encoded_value), test_value)

    def test_type_factory(self):
        self.assertIsInstance(DataTypeFactory.get_type('s')(), StringType)
        self.assertIsInstance(DataTypeFactory.get_type('i')(), IntType)
        self.assertIsInstance(DataTypeFactory.get_type('f')(), FloatType)

    def test_type_detection(self):
        self.assertIsInstance(
            DataTypeFactory.get_type_by_value("test")(), StringType
        )
        self.assertIsInstance(
            DataTypeFactory.get_type_by_value(42)(), IntType
        )
        self.assertIsInstance(
            DataTypeFactory.get_type_by_value("测试")(), Base64StringType
        )


if __name__ == '__main__':
    unittest.main()