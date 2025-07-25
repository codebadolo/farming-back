from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import User, Adresse, Client, Vendeur
from .serializers import (
    UserSerializer,
    AdresseSerializer,
    ClientSerializer,
    VendeurSerializer,
)
# Vue pour les utilisateurs.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class AdresseViewSet(viewsets.ModelViewSet):
    queryset = Adresse.objects.all()
    serializer_class = AdresseSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class VendeurViewSet(viewsets.ModelViewSet):
    queryset = Vendeur.objects.all()
    serializer_class = VendeurSerializer
