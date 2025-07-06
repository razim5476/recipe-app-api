"""
Tests for the user API.
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME = reverse('user:me')


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserAPITestCase(TestCase):
    """Test the public fetaures of the API."""

    def setUp(self):
        self.client = APIClient()

    def test_user_create(self):
        """Test case for creating the user."""
        payload = {
            'email': 'example@gmail.com',
            'password': 'razim123',
            'name': 'TestName'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))

    def test_user_email_exiats_error(self):
        """test email already exist."""
        payload = {
            'email': 'example@gmail.com',
            'password': 'razim123',
            'name': 'TestName'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_count(self):
        """test for the password count"""
        payload = {
            'email': 'example@gmail.com',
            'password': 'ra',
            'name': 'TestName'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        userr_email = get_user_model().objects.filter(
            email=payload["email"]
        ).exists()
        self.assertFalse(userr_email)

    def test_token_create_user(self):
        """check for token when user created."""
        user_detaisl = {
            'email': 'test@example.com',
            'password': 'razim123',
            'name': 'Test'
        }
        create_user(**user_detaisl)

        payload = {
            'email': 'test@example.com',
            'password': 'razim123',
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_no_email(self):
        """test case for no email"""
        payload = {
            'email': '',
            'password': 'razim123',
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_password(self):
        payload = {
            'email': 'test@example.com',
            'password': '',
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class PrivateUserAPITestCase(TestCase):
    """Tes the private or authenticated user."""

    def setUp(self):
        self.user = create_user(
            email="test@example.com",
            password="razim123",
            name="Test Name"
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retreive_profile_success(self):
        """test retrieveing profile success"""
        res = self.client.get(ME)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data, {
                'email': self.user.email,
                'name': self.user.name
            }
        )

    def test_post_me_not_allowed(self):
        """no post request allowed"""
        res = self.client.post(ME, {})

        self.assertTrue(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user(self):
        """test updating the user profile for the authenticated user."""
        payload = {
            'name': 'updated_name',
            'password': 'password123'
        }

        res = self.client.patch(ME, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
