import unittest
from app import create_app

class TestAmenityEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_create_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "WiFi"
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['name'], 'WiFi')

    def test_create_amenity_invalid_data(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": ""
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_amenities(self):
        # Create some amenities
        self.client.post('/api/v1/amenities/', json={"name": "WiFi"})
        self.client.post('/api/v1/amenities/', json={"name": "Pool"})

        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 2)

    def test_get_amenity(self):
        # Create amenity first
        create_response = self.client.post('/api/v1/amenities/', json={
            "name": "Parking"
        })
        amenity_id = json.loads(create_response.data)['id']

        # Get amenity
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Parking')

    def test_get_nonexistent_amenity(self):
        response = self.client.get('/api/v1/amenities/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_update_amenity(self):
        # Create amenity first
        create_response = self.client.post('/api/v1/amenities/', json={
            "name": "WiFi"
        })
        amenity_id = json.loads(create_response.data)['id']

        # Update amenity
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            "name": "High-Speed WiFi"
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'High-Speed WiFi')
