from rest_framework import serializers

from account.models import User


class AccountsMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        ro = {'read_only': True}
        extra_kwargs = {
            'username': ro, 'first_name': {}, 'last_name': {}, 'email': {}
        }
        fields = list(extra_kwargs.keys())
