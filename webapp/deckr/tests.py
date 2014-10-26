from django.test import TestCase

class SimpleTestCase(TestCase):
    
    def test_addition(self):
        self.assertEqual(1 + 1, 2)