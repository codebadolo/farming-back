from django.shortcuts import render
from rest_framework import viewsets
from .models import Livraison
from .serializers import LivraisonSerializer

# Vue pour la livraison.
class LivraisonViewSet(viewsets.ModelViewSet):
    queryset = Livraison.objects.all().select_related("commande")
    serializer_class = LivraisonSerializer
