from django.shortcuts import render
from rest_framework import viewsets
from .models import Commande, ProduitCommande
from .serializers import CommandeSerializer, ProduitCommandeSerializer

# Vue pour les commandes.
class CommandeViewSet(viewsets.ModelViewSet):
     queryset = Commande.objects.all().select_related("client",
     "adresse_livraison")
serializer_class = CommandeSerializer
filterset_fields = ["client", "statut"]
class ProduitCommandeViewSet(viewsets.ModelViewSet):
     queryset = ProduitCommande.objects.all().select_related("commande",
     "produit")
serializer_class = ProduitCommandeSerializer