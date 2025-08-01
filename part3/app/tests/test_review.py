import unittest
from app.models.review import Review

class TestReview(unittest.TestCase):
    def test_creation(self):
        r = Review("Super séjour", 5, "place_1", "user_1")
        self.assertEqual(r.text, "Super séjour")
        self.assertEqual(r.rating, 5)
        self.assertEqual(r.place_id, "place_1")
        self.assertEqual(r.user_id, "user_1")

    def test_to_dict(self):
        r = Review("Bien", 4, "place_2", "user_2")
        d = r.to_dict()
        self.assertEqual(d['rating'], 4)
        self.assertEqual(d['place_id'], "place_2")

if __name__ == '__main__':
    unittest.main()

