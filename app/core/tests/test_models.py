"""
Test for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models"""


    def test_create_user_email_success(self):
        """Test code for the user login with email"""
        email = "test1@example.com"
        password = "testpassword"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.check_password(password), True)

    def test_new_user_email_normalize(self):
        """Test email is normalized for new users."""
        sample_email = [
                ["TESTING@EXAMPLE.com", "TESTING@example.com"],
        ]
        for email, expected in sample_email:
            user  = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)
        
    def test_new_user_without_email_raises_error(self):
        """Tets taht creatung a auser without an email raises an valuerror"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test for creatig super user"""
        user = get_user_model().objects.create_superuser(
            'testemailsuperuser',
            'password123'
        )

