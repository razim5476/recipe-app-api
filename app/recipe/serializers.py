"""
serializer for the recipe app.
"""

from rest_framework import serializers
from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """serializer for recipes."""

    class Meta:
        model = Recipe
        fields = [
            "id", "title", "time_minutes", "price", "link"
        ]
        read_only_fields = ["id"]


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for the recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ["description"]
