from rest_framework import serializers
from .models import Livraison

class LivraisonSerializer(serializers.ModelSerializer):
    class Meta:
      model = Livraison
      fields = "__all__"