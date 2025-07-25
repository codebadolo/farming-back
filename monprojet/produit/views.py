from django.shortcuts import render
from rest_framework import viewsets
from .models import Categorie, Produit, Attribut, ListeSouhait
from .serializers import (
    CategorieSerializer,
    ProduitSerializer,
    AttributSerializer,
    ListeSouhaitSerializer,
)
# Vue pour les produits.

class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    filterset_fields = ["parent"]

class ProduitViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.all().select_related("categorie", "vendeur")
    serializer_class = ProduitSerializer
    filterset_fields = ["categorie", "vendeur"]
    search_fields = ["nom", "description"]
    ordering_fields = ["prix", "date_ajout"]

class AttributViewSet(viewsets.ModelViewSet):
    queryset = Attribut.objects.all()
    serializer_class = AttributSerializer

class ListeSouhaitViewSet(viewsets.ModelViewSet):
    queryset = ListeSouhait.objects.all()
    serializer_class = ListeSouhaitSerializer
