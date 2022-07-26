from django.contrib.auth import get_user_model
from rest_framework import serializers

__all__ = ['BaseSerializer', 'EmptySerializer']


class BaseSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class EmptySerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = []
