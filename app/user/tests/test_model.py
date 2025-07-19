"""
Test models
"""

from decimal import Decimal
from core import models
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):
    """model testcases"""

    def test_receipe_create(self):
        """teting a new creation of receipe model test."""

        user = get_user_model().objects.create_user(
            'test@example.com',
            'password123',
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title="Sample recipe name",
            time_minutes=5,
            price=Decimal('5.50'),
            description="Sample reipe description.",
        )

        self.assertEqual(str(recipe), recipe.title)
