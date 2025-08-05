
from django.shortcuts import render
from rest_framework import generics, permissions
from .models import APIConfiguration, APIAccessToken, APIRequestLog, APIVersion
from .serializers import (APIConfigurationSerializer, APIAccessTokenSerializer, APIRequestLogSerializer, APIVersionSerializer)

class APIConfigurationView(generics.RetrieveUpdateAPIView):
    queryset = APIConfiguration.objects.all()
    serializer_class = APIConfigurationSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_object(self):
        return APIConfiguration.objects.first()

class APIAccessTokenListCreateView(generics.ListCreateAPIView):
    serializer_class = APIAccessTokenSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return APIAccessToken.objects.filter(user=self.request.user)

class APIRequestLogListView(generics.ListAPIView):
    serializer_class = APIRequestLogSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = APIRequestLog.objects.all()

class APIVersionListView(generics.ListAPIView):
    serializer_class = APIVersionSerializer
    permission_classes = [permissions.AllowAny]
    queryset = APIVersion.objects.all()