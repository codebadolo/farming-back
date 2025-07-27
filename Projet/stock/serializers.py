from rest_framework import serializers
from .models import Stock, MouvementStock

class StockSerializer(serializers.ModelSerializer):
  class Meta:
     model = Stock
     fields = "__all__"
class MouvementStockSerializer(serializers.ModelSerializer):
  class Meta:
    model = MouvementStock
    fields = "__all__"