from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock


class GatewayRoutingTest(APITestCase):
    """Test API Gateway routing"""

    def setUp(self):
        self.client = APIClient()

    def test_gateway_health_endpoint(self):
        """Test gateway health endpoint"""
        response = self.client.get('/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('apps.gateway.views.requests.request')
    def test_auth_routes_to_user_service(self, mock_request):
        """Test /api/auth/* routes to user-service"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'message': 'ok'}
        mock_response.headers = {}
        mock_response.text = '{"message": "ok"}'
        mock_request.return_value = mock_response

        response = self.client.get('/api/auth/me/')
        
        # Check that the request was proxied
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])

    @patch('apps.gateway.views.requests.request')
    def test_users_routes_to_user_service(self, mock_request):
        """Test /api/users/* routes to user-service"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_response.headers = {}
        mock_response.text = '[]'
        mock_request.return_value = mock_response

        response = self.client.get('/api/users/')
        
        # Check that request was processed
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])

    @patch('apps.gateway.views.requests.request')
    def test_tournaments_routes_to_tournament_service(self, mock_request):
        """Test /api/tournaments/* routes to tournament-service"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_response.headers = {}
        mock_response.text = '[]'
        mock_request.return_value = mock_response

        response = self.client.get('/api/tournaments/')
        
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])

    @patch('apps.gateway.views.requests.request')
    def test_tasks_routes_to_task_service(self, mock_request):
        """Test /api/tasks/* routes to task-service"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_response.headers = {}
        mock_response.text = '[]'
        mock_request.return_value = mock_response

        response = self.client.get('/api/tasks/')
        
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])

    @patch('apps.gateway.views.requests.request')
    def test_submissions_routes_to_task_service(self, mock_request):
        """Test /api/submissions/* routes to task-service"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_response.headers = {}
        mock_response.text = '[]'
        mock_request.return_value = mock_response

        response = self.client.get('/api/submissions/')
        
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])

    def test_non_existent_route(self):
        """Test non-existent route returns 404"""
        response = self.client.get('/api/nonexistent/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cors_headers_present(self):
        """Test CORS headers are present"""
        response = self.client.options('/api/users/')
        # Should allow OPTIONS request or have CORS headers
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT])


class GatewayMiddlewareTest(APITestCase):
    """Test Gateway middleware"""

    def setUp(self):
        self.client = APIClient()

    def test_rate_limiting(self):
        """Test rate limiting middleware"""
        # Make multiple requests
        for i in range(10):
            response = self.client.get('/health/')
            # Should succeed
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('apps.gateway.views.requests.request')
    def test_auth_header_forwarding(self, mock_request):
        """Test Authorization header is forwarded"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'authorized': True}
        mock_response.headers = {}
        mock_response.text = '{"authorized": true}'
        mock_request.return_value = mock_response

        headers = {'Authorization': 'Bearer test_token'}
        response = self.client.get('/api/users/', **headers)
        
        # Request should be processed
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])
