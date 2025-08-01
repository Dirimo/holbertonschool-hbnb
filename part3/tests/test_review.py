import unittest
from app import create_app

class TestReviewEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        
        # Create a user
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com"
        })
        self.user_id = json.loads(user_response.data)['id']
        
        # Create another user as owner
        owner_response = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "User",
            "email": "owner@example.com"
        })
        self.owner_id = json.loads(owner_response.data)['id']
        
        # Create a place
        place_response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "Test description",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.owner_id
        })
        self.place_id = json.loads(place_response.data)['id']

    def test_create_review(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['text'], 'Great place to stay!')
        self.assertEqual(data['rating'], 5)

    def test_create_review_invalid_data(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 6,  # Invalid rating (should be 1-5)
            "user_id": "invalid-user-id",
            "place_id": "invalid-place-id"
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_reviews(self):
        # Create a review
        self.client.post('/api/v1/reviews/', json={
            "text": "Nice place",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_review(self):
        # Create review first
        create_response = self.client.post('/api/v1/reviews/', json={
            "text": "Excellent stay!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = json.loads(create_response.data)['id']
        
        # Get review
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['text'], 'Excellent stay!')

    def test_get_nonexistent_review(self):
        response = self.client.get('/api/v1/reviews/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_update_review(self):
        # Create review first
        create_response = self.client.post('/api/v1/reviews/', json={
            "text": "Original review",
            "rating": 3,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = json.loads(create_response.data)['id']
        
        # Update review
        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "Updated review text",
            "rating": 4
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['text'], 'Updated review text')
        self.assertEqual(data['rating'], 4)

    def test_delete_review(self):
        # Create review first
        create_response = self.client.post('/api/v1/reviews/', json={
            "text": "Review to delete",
            "rating": 3,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = json.loads(create_response.data)['id']
        
        # Delete review
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        
        # Verify deletion
        get_response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(get_response.status_code, 404)
