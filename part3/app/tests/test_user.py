import unittest
from app.models.user import User

class TestUser(unittest.TestCase):
    def test_creation(self):
        u = User("Alice", "Dupont", "alice@mail.com", "mdp123", True)
        self.assertEqual(u.first_name, "Alice")
        self.assertEqual(u.last_name, "Dupont")
        self.assertEqual(u.email, "alice@mail.com")
        self.assertTrue(u.is_admin)

    def test_to_dict(self):
        u = User("Bob", "Martin", "bob@mail.com", "mdp456")
        d = u.to_dict()
        self.assertEqual(d['first_name'], "Bob")
        self.assertNotIn('password', d)  # on ne veut pas exposer le mot de passe

if __name__ == '__main__':
    unittest.main()

