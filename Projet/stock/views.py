from django.shortcuts import render
from rest_framework import viewsets
from .models import Stock, MouvementStock
from .serializers import StockSerializer, MouvementStockSerializer

# Ma vue pour les stocks.

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all().select_related("produit")
serializer_class = StockSerializer
class MouvementStockViewSet(viewsets.ModelViewSet):
     queryset = MouvementStock.objects.all().select_related("produit")
serializer_class = MouvementStockSerializer
