import unittest
from app.models.amenity import amenity

class TestAmenity(unittest.TestCase):
    def test_creation(self):
        a = Amenity("WiFi")
        self.assertIsNotNone(a.id)
        self.assertEqual(a.name, "WiFi")
        self.assertIsNotNone(a.created_at)
        self.assertIsNotNone(a.updated_at)

    def test_to_dict(self):
        a = Amenity("Pool")
        d = a.to_dict()
        self.assertEqual(d['name'], "Pool")
        self.assertEqual(d['id'], a.id)
        self.assertIn('created_at', d)
        self.assertIn('updated_at', d)

if __name__ == '__main__':
    unittest.main()

