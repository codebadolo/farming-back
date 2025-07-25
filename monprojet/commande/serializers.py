from rest_framework import serializers
from .models import Commande, ProduitCommande

class ProduitCommandeSerializer(serializers.ModelSerializer):
    class Meta:
      model = ProduitCommande
      fields = "__all__"
class CommandeSerializer(serializers.ModelSerializer):
   lignes = ProduitCommandeSerializer(many=True, read_only=True)
class Meta:
        model = Commande
fields = "__all__"