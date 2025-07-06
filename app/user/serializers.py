"""
Serializer s for the api view.
"""

from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _
from core.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serilizer for the user objects."""

    class Meta:
        model = User
        fields = [
            "email", "password", "name"
        ]
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 6,
            }
        }

    def create(self, validated_data):
        """Create the user with hashed password."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """updated and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthenticationToken(serializers.Serializer):
    """Serializer for the authentication token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={
            'input': 'password',
        },
        trim_whitespace=False
    )

    def validate(self, attrs):
        """validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _("Unable to authenticate provided credentials.")
            raise serializers.ValidationError(msg, code='authenticate')

        attrs['user'] = user
        return attrs
