from django.test import TestCase


def add(a: int, b: int):
    return a + b


# Create your tests here.
class AddTestCase(TestCase):
    def test_add(self):
        self.assertEqual(add(3, 4), 7)
        self.assertEqual(add(4, 4), 10)
