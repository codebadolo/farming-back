from django.shortcuts import render
from rest_framework import viewsets
from .models import MethodePaiement, Paiement
from .serializers import MethodePaiementSerializer, PaiementSerializer

# Ma vue pour les paiements.
class MethodePaiementViewSet(viewsets.ModelViewSet):
     queryset = MethodePaiement.objects.all()
     serializer_class = MethodePaiementSerializer
     
class PaiementViewSet(viewsets.ModelViewSet):
     queryset = Paiement.objects.all().select_related("commande",
     "nom_methode")
     serializer_class = PaiementSerializer