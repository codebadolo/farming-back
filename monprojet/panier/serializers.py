from rest_framework import serializers
from .models import Panier, PanierItem

class PanierItemSerializer(serializers.ModelSerializer):
    prix_unitaire = serializers.ReadOnlyField()
    sous_total = serializers.ReadOnlyField()
    
    class Meta:
      model = PanierItem
      fields = "__all__"
class PanierSerializer(serializers.ModelSerializer):
    items = PanierItemSerializer(many=True, read_only=True)
    total = serializers.ReadOnlyField()
class Meta:
    model = Panier
    fields = "__all__"