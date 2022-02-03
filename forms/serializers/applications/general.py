from rest_framework import serializers

from forms.models import Application


class FormApplicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        wo = {'write_only': True}
        extra_kwargs = {
            'name': wo, 'email': wo, 'telegram': wo, 'facebook': wo, 'whats_app': wo,
            'viber': wo, 'about': wo
        }
        fields = list(extra_kwargs.keys())
