import unittest
from rcd.rcd_function import Function


class RcdFunctionTest(unittest.TestCase):
    def setUp(self):
        self.f1 = Function("1(2")

    def tearDown(self):
        del self.f1

    def test_name(self):
        self.assertEqual(self.f1.name, "1")

    def test_repr(self):
        self.assertTrue(repr(self.f1).startswith("Function<"))
        self.assertTrue(repr(self.f1).endswith(">"))
        self.assertTrue("declaration:" in repr(self.f1))
        self.assertTrue("name:" in repr(self.f1))
        self.assertTrue("body:" in repr(self.f1))




if __name__ == '__main__':
    unittest.main()
