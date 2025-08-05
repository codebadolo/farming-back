
from rest_framework import serializers
from .models import APIConfiguration, APIAccessToken, APIRequestLog, APIVersion

class APIConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIConfiguration
        fields = '__all__'
        read_only_fields = ['last_updated']

class APIAccessTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIAccessToken
        fields = ['token', 'created_at', 'expires_at', 'is_active']
        extra_kwargs = {
            'token': {'read_only': True},
            'created_at': {'read_only': True}
        }

class APIRequestLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIRequestLog
        fields = '__all__'

class APIVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIVersion
        fields = '__all__'