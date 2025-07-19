from django.test import TestCase
from decimal import Decimal
from core.models import Recipe
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer


RECIPE_URL = reverse('recipe:recipe-list')


def recipe_detail_url(recipe_id):
    """function for the recipe url with id"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def create_recipe(user, **params):
    """create an test api recipe"""
    defaults = {
        'title': 'test name',
        'time_minutes': 22,
        'price': Decimal('5.20'),
        'description': 'Sample  description',
        'link': 'http://example.com/recipe.pdf',
    }
    defaults.update(params)

    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe


def create_user(**params):
    """creating user"""
    return get_user_model().objects.create_user(**params)


class PublicRecipeTests(TestCase):
    """Test for unauthicateed user."""

    def setUp(self):
        self.client = APIClient()

    def test_unauthenticated_user(self):
        """test fo unactticated user."""
        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateReipeAPITests(TestCase):
    """Test authorized API request."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@emaple.com', password='test123')
        self.client.force_authenticate(self.user)

    def test_retrive_reipe(self):
        """ test list the reipe."""
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeDetailSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrive_recipe_limited(self):
        """test for the unauthenticated users"""
        other_user = create_user(email='other@exmaple.com', password='test123')
        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeDetailSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_detail_recipe_with_id(self):
        """recipe detail test"""
        recipe = create_recipe(user=self.user)
        url = recipe_detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """test creatina recipe api."""
        patload = {
            "title": "sample itme",
            "time_minutes": 30,
            "price": Decimal('20.0'),
        }
        res = self.client.post(RECIPE_URL, patload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for k, v in patload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)

    def test_partial_update(self):
        """test for the partisla update."""

        original_link = "htttp://google.com"
        recipe_payload = create_recipe(
            user=self.user,
            title='Sample Title',
            link=original_link
        )

        payload = {'title': 'Partial Updated_title'}
        url = recipe_detail_url(recipe_payload.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe_payload.refresh_from_db()

        self.assertEqual(recipe_payload.title, payload['title'])
        self.assertEqual(recipe_payload.link, original_link)
        self.assertEqual(recipe_payload.user, self.user)

    def test_full_update(self):
        """test full update of recipre."""

        recipe = create_recipe(
            user=self.user,
            title='Sample recipe title.',
            description='new recipe descriptin',
            link='https://google.com/'
        )

        payload = {
            'title': 'New title',
            'link': 'https://recipe.com/recipe.pdf',
            'description': 'testing',
            'time_minutes': 10,
            'price': Decimal(20)
        }
        url = recipe_detail_url(recipe_id=recipe.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)

    def test_update_user_returns_error(self):
        """test for upfadting teh use gives error."""

        new_user = create_user(email='user2@gmail.com', password='password123')
        recipe = create_recipe(user=self.user)

        payload = {
            'user': new_user.id
        }
        url = recipe_detail_url(recipe_id=recipe.id)
        res = self.client.patch(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.user, self.user)

    def test_delete_recipe(self):
        """Test deleting a recipe."""

        recipe = create_recipe(user=self.user)
        url = recipe_detail_url(recipe_id=recipe.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())

    def test_recipe_other_user_erro(self):
        """test trying to delete another users recipe gives error."""

        new_user = create_user(email="newuser@gmail.com", password="123test")
        recipe = create_recipe(user=new_user)

        url = recipe_detail_url(recipe_id=recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Recipe.objects.filter(id=recipe.id).exists())
