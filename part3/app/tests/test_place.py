import unittest
from app.models.place import Place
from app.models.amenity import Amenity

class TestPlace(unittest.TestCase):
    def test_creation(self):
        p = Place("Chalet", "Belle vue", 120, 45.0, 3.0, "user_1")
        self.assertEqual(p.title, "Chalet")
        self.assertEqual(p.price, 120)
        self.assertEqual(p.owner_id, "user_1")
        self.assertEqual(p.amenities, [])

    def test_amenities(self):
        p = Place("Villa", "Piscine privée", 300, 40.0, 2.0, "user_2")
        wifi = Amenity("WiFi")
        p.amenities.append(wifi)
        self.assertEqual(len(p.amenities), 1)
        self.assertEqual(p.amenities[0].name, "WiFi")

    def test_to_dict(self):
        p = Place("Cabane", "Au calme", 80, 48.0, 4.0, "user_3")
        d = p.to_dict()
        self.assertEqual(d['title'], "Cabane")
        self.assertIn('amenities', d)
        self.assertIsInstance(d['amenities'], list)

if __name__ == '__main__':
    unittest.main()

