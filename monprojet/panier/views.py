from django.shortcuts import render
from rest_framework import viewsets
from .models import Panier, PanierItem
from .serializers import PanierSerializer, PanierItemSerializer

# Ma vue pour le panier.
class PanierViewSet(viewsets.ModelViewSet):
    queryset = Panier.objects.all().select_related("user")
    serializer_class = PanierSerializer
class PanierItemViewSet(viewsets.ModelViewSet):
    queryset = PanierItem.objects.all().select_related("panier", "produit")
    serializer_class = PanierItemSerializer