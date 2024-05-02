from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class APIDocumentationTests(APITestCase):
    def test_schema_endpoint(self):
        """
        Test the API schema endpoint returns a 200 status
        and correct content type.
        """
        url = reverse('api-schema')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response['Content-Type']
                        .startswith('application/vnd.oai.openapi'))

    def test_docs_endpoint(self):
        """
        Test the API docs endpoint returns a 200 status
        and the expected HTML content.
        """
        url = reverse('api-docs')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('text/html', response['Content-Type'])
