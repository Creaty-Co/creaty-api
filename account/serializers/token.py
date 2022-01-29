from django.contrib.auth import authenticate
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers, status

from account.models import User
from account.services.auth import AuthService
from base.exceptions import APIWarning
from base.schemas.mixins import SerializerSchemaMixin


class AccountsTokenSerializer(SerializerSchemaMixin, serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    
    WARNINGS = {
        401: APIWarning(
            'Неверный пароль', codes=['invalid_password'],
            status=status.HTTP_401_UNAUTHORIZED
        ),
        404: APIWarning(
            'Пользователя с таким email не существует',
            codes=['email_not_found'], status=status.HTTP_404_NOT_FOUND
        ),
        406: APIWarning(
            'Пользователь не верифицирован', codes=['not_verified'],
            status=status.HTTP_406_NOT_ACCEPTABLE
        )
    }
    
    class Meta:
        model = User
        extra_kwargs = {
            'email': {'write_only': True, 'validators': []},
            'password': {'write_only': True}
        }
        fields = list(extra_kwargs.keys()) + ['token']
    
    @extend_schema_field(OpenApiTypes.STR)
    def get_token(self, user):
        return AuthService(self.context['request'], user).login()
    
    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']
        
        user: User = authenticate(
            request=self.context.get('request'), email=email, password=password
        )
        if user is None:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise self.WARNINGS[404]
            if not user.check_password(password):
                raise self.WARNINGS[401]
            if not user.is_active:
                raise self.WARNINGS[406]
        self.instance = user
        return attrs
