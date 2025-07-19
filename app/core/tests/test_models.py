"""
Test for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Tag


def create_user(email='user@eample.com', password="test123"):
    """create and return a new user."""
    return get_user_model().objects.create_user(email, password)


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
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Tets taht creatung a auser without an email raises an valuerror"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test for creatig super user"""
        email = 'testemailsuperuser'
        password = 'password123'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_tag(self):
        """Test creating a tag is successful"""

        user = create_user()

        tag = Tag.objects.create(user=user, name='Tag1')
        self.assertEqual(str(tag), tag.name)
