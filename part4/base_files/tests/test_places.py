import unittest
from app import create_app

class TestPlaceEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        
        # Create a user for testing places
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "Owner",
            "email": "owner@example.com"
        })
        self.user_id = json.loads(user_response.data)['id']

    def test_create_place(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A beautiful place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['title'], 'Cozy Apartment')

    def test_create_place_invalid_data(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "price": -50,
            "latitude": 200,  # Invalid latitude
            "longitude": -200  # Invalid longitude
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_places(self):
        # Create a place
        self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "Test description",
            "price": 80.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": self.user_id
        })
        
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_place(self):
        # Create place first
        create_response = self.client.post('/api/v1/places/', json={
            "title": "Beach House",
            "description": "Ocean view property",
            "price": 200.0,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "owner_id": self.user_id
        })
        place_id = json.loads(create_response.data)['id']
        
        # Get place
        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Beach House')

    def test_get_nonexistent_place(self):
        response = self.client.get('/api/v1/places/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_update_place(self):
        # Create place first
        create_response = self.client.post('/api/v1/places/', json={
            "title": "Old Title",
            "description": "Old description",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })
        place_id = json.loads(create_response.data)['id']
        
        # Update place
        response = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "Updated Title",
            "price": 150.0
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Updated Title')
        self.assertEqual(data['price'], 150.0)

